import sys
import os
import imp
from js9 import j
import signal
import gevent
import gevent.signal
from gevent.pool import Pool
from gevent.server import StreamServer

from .handler import Handler
from .GedisCmds import GedisCmds


JSConfigBase = j.tools.configmanager.base_class_config

TEMPLATE = """
    host = "localhost"
    port = "9900"
    secret_ = ""
    apps_dir = ""
    """

class Models():
    def __init__(self):
        pass

class GedisServer(StreamServer, JSConfigBase):
    def __init__(
        self,
        instance,
        data={},
        parent=None,
        interactive=False,
        template=None
    ):

        JSConfigBase.__init__(
            self,
            instance=instance,
            data=data,
            parent=parent,
            template=template or TEMPLATE, # default config if template is None
            interactive=interactive
        )

        # Set proper instance for j.data.schema

        # Cache holds all global variables that needs
        # i,e in orderbook 'orders'
        self.globals = {}
        self.models = Models()
        self.db = None
        self._sig_handler = []
        self.cmds_meta = {}
        self.classes = {}
        self.cmds = {}
        self.schema_urls = []
        self.serializer = None
        self._inited = False
        self.ssl_priv_key_path = None
        self.ssl_cert_path = None

        self.host = self.config.data["host"]
        self.port = int(self.config.data["port"])
        self.address = '{}:{}'.format(self.host, self.port)

        j.servers.gedis2.latest = self

        self.server_path = self.scaffold(
            self.config.data['apps_dir'],
            instance)

        self.ssl_priv_key_path, self.ssl_cert_path = self.sslkeys_generate()

        # Server always supports SSL
        # client can use to talk to it in SSL or not
        self.server = StreamServer(
            (self.host, self.port),
            spawn=Pool(),
            handle=Handler(self).handle,
            keyfile=self.ssl_priv_key_path,
            certfile=self.ssl_cert_path
        )

    def scaffold(self, apps_dir, instance, reset=False):
        # Apps directory is gedis2/apps if empty
        if not apps_dir:
            apps_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'apps'
            )

        if not j.sal.fs.exists(apps_dir):
            j.sal.fs.createDir(apps_dir)

        if not apps_dir in sys.path:
            sys.path.append(apps_dir)

        # application directory
        # apps_dir/{instance}
        self.app_dir = os.path.join(
            apps_dir,
            instance
        )

        j.sal.fs.touch(os.path.join(self.app_dir, '/__init__.py'))

        if not j.sal.fs.exists(self.app_dir):
            j.sal.fs.createDir(self.app_dir)

        # Create server dir
        # apps_dir/{instance}/server
        server_path = os.path.join(self.app_dir, 'server')
        if not j.sal.fs.exists(server_path):
            j.sal.fs.createDir(server_path)

        if not server_path in sys.path:
            sys.path.append(server_path)

        j.sal.fs.touch(os.path.join(server_path, '/__init__.py'))

        # copy the templates in the local server dir
        for item in ["system"]:
            dest = os.path.join(server_path, "%s.py" % item)
            if reset or not j.sal.fs.exists(dest):
                src = os.path.join(j.servers.gedis2._path, "templates", '%s.py' % item)
                j.sal.fs.copyFile(src, dest)
        return server_path

    def sslkeys_generate(self):
        res = j.sal.ssl.ca_cert_generate(self.app_dir)
        if res:
            self.logger.info("generated sslkeys for gedis in %s" % self.app_dir)
        else:
            self.logger.info('using existing key and cerificate for gedis @ %s' % self.app_dir)
        key = os.path.join(self.app_dir, 'ca.key')
        cert = os.path.join(self.app_dir, 'ca.crt')
        return key, cert

    def init(self):
        self.logger.info("init server")
        self._sig_handler.append(gevent.signal(signal.SIGINT, self.stop))
        self.logger.info("start server")

        # add the cmds to the server (from generated modules)
        namespace_base = self.instance
        for item in j.sal.fs.listFilesInDir(self.server_path,filter="*.py",exclude=["__*"]):
            namespace = namespace_base + '.' + j.sal.fs.getBaseName(item)[:-3].lower()
            self.cmds_add(namespace, path=item)
        self._inited = True

    def _start(self, db=None, reset=False):

        if not db:
            j.data.bcdb.db_start(
                self.instance,
                adminsecret=self.config.data["secret_"],
                reset=reset
            )
            db = j.data.bcdb.get(self.instance)
            db.tables_get(
                os.path.dirname(self.server_path)
            )

        self.db = db

        self.scaffold(self.config.data['apps_dir'], self.instance, reset)

        # tables are now in db.tables as dict

        # Generate & models (name spaces) from schema

        for namespace, table in db.tables.items():
            # url = table.schema.url.replace(".","_")
            dest = os.path.join(self.server_path, "model_%s.py" % namespace)
            if reset or not j.sal.fs.exists(dest):
                code = j.servers.gedis2.code_model_template.render(obj=table.schema)
                j.sal.fs.writeFile(dest, code)
            self.schema_urls.append(table.schema.url)
            schema_name = table.schema.url.replace(".", "_")
            fname = "model_%s" % schema_name
            m = imp.load_source(name=fname, pathname=dest)
            self.models.__dict__[schema_name] = getattr(m, "model_%s" % namespace)()
            # Generate schema
            table.schema.objclass

        if reset:
            # Copy start.py
            code = j.servers.gedis2.code_start_template.render(config=self.config.data, instance=self.instance)
            dest = os.path.join(os.path.dirname(self.server_path), 'start.py')
            j.sal.fs.writeFile(dest, code)

            # Copy test.py
            code = j.servers.gedis2.code_test_template.render(config=self.config.data, instance=self.instance)
            dest = os.path.join(os.path.dirname(self.server_path), 'test.py')
            if not j.sal.fs.exists(dest):
                j.sal.fs.writeFile(dest, code)

        if self._inited is False:
            self.init()


        self.server.serve_forever()

    def start(self, db=None, reset=False):
        cmd = "js9 'x=j.servers.gedis2.get(instance=\"%s\");x._start(reset=%s)'" % (self.instance, reset)
        j.tools.tmux.execute(
            cmd,
            session='main',
            window='gedis_%s' % self.instance,
            pane='main',
            session_reset=False,
            window_reset=True
        )

        res = j.sal.nettools.waitConnectionTest("localhost", int(self.config.data["port"]), timeoutTotal=1000)
        if res == False:
            raise RuntimeError("Could not start gedis server on port:%s" % int(self.config.data["port"]))
        self.logger.info("gedis server '%s' started" % self.instance)

    def stop(self):
        """
        stop receiving requests and close the server
        """
        # prevent the signal handler to be called again if
        # more signal are received
        for h in self._sig_handler:
            h.cancel()

        self.logger.info('stopping server')
        self.server.stop()

    def cmds_add(self, namespace, path=None, class_=None):
        self.logger.debug("cmds_add:%s:%s"%(namespace , path))
        if path is not None:
            classname = j.sal.fs.getBaseName(path).split(".", 1)[0]
            dname = j.sal.fs.getDirName(path)
            old_paths = sys.path
            if dname not in sys.path:
                sys.path.append(dname)
            exec("from %s import %s" % (classname, classname))
            class_ = eval(classname)

        self.cmds_meta[namespace] = GedisCmds(self, namespace=namespace, class_=class_)
        self.classes[namespace] =class_()

    def __repr__(self):
        return '<Gedis Server address=%s  app_dir=%s)' % (self.address, self.app_dir)

    __str__ = __repr__
