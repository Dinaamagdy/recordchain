
from js9 import j
import signal
import gevent
import gevent.signal
from gevent.pool import Pool
from gevent.server import StreamServer
from .protocol import CommandParser, ResponseWriter
import inspect
import imp
import sys
from .GedisCmds import GedisCmds
from .GedisServerBase import GedisServerBase
from redis.connection import ConnectionError

TEMPLATE = """
addr = "localhost"
port = "9900"
ssl = false
adminsecret_ = ""
dbclient_instance = ""
"""
JSConfigBase = j.tools.configmanager.base_class_config


class GedisServer(StreamServer, JSConfigBase):

    def __init__(self, instance, data={}, parent=None, interactive=False, template=None):
        """
        """
        self._code_server_template = None
        self._code_client_template = None
        self._template_engine = None
        self.dbclient = None
        if not template:
            template = TEMPLATE
        JSConfigBase.__init__(self, instance=instance, data=data,
                              parent=parent, template=template, interactive=interactive)
        self.host = self.config.data["addr"]
        self.port = int(self.config.data["port"])

        if self.config.data['dbclient_instance']:
            self.dbclient = j.clients.gedis_backend.get(self.config.data['dbclient_instance'])

        self.address = '{}:{}'.format(self.host, self.port)

        self._sig_handler = []
        self.cmds = {}
        self._cmds_path = j.sal.fs.getParent(self.config.path) + "/" + instance + "/"
        j.sal.fs.createDir(self._cmds_path)

        # PREPARE FOR CODE GENERATION
        self._template_engine = None
        self.code_generation_dir = j.dirs.VARDIR+"/codegen/gedis/"
        j.sal.fs.createDir(self.code_generation_dir)
        if self.code_generation_dir not in sys.path:
            sys.path.append(self.code_generation_dir)
        j.sal.fs.touch(self.code_generation_dir+"/__init__.py")
        self.logger.debug("codegendir:%s" % self.code_generation_dir)

        self.cmds_add(namespace="system", class_=GedisServerBase)

    @property
    def template_engine(self):
        if self._template_engine is None:
            from jinja2 import Environment, PackageLoader

            self._template_engine = Environment(
                loader=PackageLoader(
                    'JumpScale9RecordChain.servers.gedis', 'templates'),
                trim_blocks=True,
                lstrip_blocks=True,
            )
        return self._template_engine

    @property
    def code_server_template(self):
        if self._code_server_template is None:
            self._code_server_template = self.template_engine.get_template("template_server.py")
        return self._code_server_template

    @property
    def code_client_template(self):
        if self._code_client_template is None:
            self._code_client_template = self.template_engine.get_template("template_client.py")
        return self._code_client_template

    def sslkeys_generate(self):

        res = j.sal.ssl.ca_cert_generate(j.sal.fs.getDirName(self.config.path))
        if res:
            self.logger.info("generated sslkeys for gedis in %s" %
                             self.config.path)

    @property
    def ssl_priv_key_path(self):
        p = j.sal.fs.getDirName(self.config.path) + "ca.key"
        if self.config.data["ssl"]:
            return p

    @property
    def ssl_cert_path(self):
        p = j.sal.fs.getDirName(self.config.path) + "ca.crt"
        if self.config.data["ssl"]:
            return p

    # def register_command(self, cmd, callback):

    #     self.logger.info("add cmd %s" % cmd)
    #     content = inspect.getsource(callback)

    #     #remove the self. if written as class style
    #     lines = content.splitlines()
    #     content = ""
    #     for line in lines:
    #         line = line.replace("self,", "")
    #         content = content + line[4:] + "\n"

    #     if not j.sal.fs.exists(path=self._cmds_path):
    #         j.sal.fs.writeFile(self._cmds_path, contents=content)
    #     else:
    #         __cmds = imp.load_source(name="cmds.py", pathname=self._cmds_path)
    #         if cmd+"_cmd" not in __cmds.__dir__():
    #             j.sal.fs.writeFile(self._cmds_path, contents='\n' + content, append=True)

    def __handle_connection(self, socket, address):
        self.logger.info('connection from {}'.format(address))
        parser = CommandParser(socket)
        response = ResponseWriter(socket)
        # self._cmds = imp.load_source(name="cmds.py", pathname=self._cmds_path)

        try:
            while True:
                request = parser.read_request()
                cmd = request[0]
                cmd = cmd.decode("utf-8")
                ns, cmd = cmd.split('.')
                available_cmds = {cmd['name'].lower(): cmd for cmd in self.cmds[ns].data.cmds.pylist}
                if cmd.lower() not in available_cmds:
                    response.error('command not supported')
                    continue

                # execute command callback
                result = ""
                try:
                    cmds = imp.load_source(ns, self._cmds_path + ns + '.py')
                    result = getattr(cmds, cmd.lower())(request, ns, self.dbclient)
                    self.logger.debug(
                        "Callback done and result {} , type {}".format(result, type(result)))
                except Exception as e:
                    print("exception in redis server")
                    eco = j.errorhandler.parsePythonExceptionObject(e)
                    response.error(str(eco))
                    continue
                self.logger.debug(
                    "response:{}:{}:{}".format(address, cmd, result))
                response.encode(result)

        except ConnectionError as err:
            self.logger.info('connection error: {}'.format(str(err)))
        finally:
            parser.on_disconnect()
            self.logger.info('close connection from {}'.format(address))

    def _init_server(self):
        if self.config.data['ssl']:
            self.logger.info("ssl enabled, keys in %s" %
                             self.ssl_priv_key_path)
            self.sslkeys_generate()

            self.server = StreamServer(
                (self.host, self.port), spawn=Pool(), handle=self.__handle_connection, keyfile=self.ssl_priv_key_path, certfile=self.ssl_cert_path)
        else:
            self.server = StreamServer(
                (self.host, self.port), spawn=Pool(), handle=self.__handle_connection)


    def start(self):
        self.logger.info("init server")
        j.logger.enabled = False
        self._logger = None

        self._init_server()

        self._sig_handler.append(gevent.signal(signal.SIGINT, self.stop))

        self.logger.info("start server")
        # SHOULD NOT IMPLEMENT BACKGROUND HERE HAS BEEN DONE AT FACTORY LEVEL
        # if background:
        #     from multiprocessing import Process
        #     p = Process(target=self.server.serve_forever)
        #     p.start()
        # else:
        self.server.serve_forever()

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
        if path is not None:
            classname = j.sal.fs.getBaseName(path).split(".", 1)[0]
            dname = j.sal.fs.getDirName(path)
            if dname not in sys.path:
                sys.path.append(dname)

            exec("from .%s import %s" % (classname, classname))
            class_ = eval(classname)

        cmds = GedisCmds(self, namespace=namespace, class_=class_)
        self.cmds[namespace] = cmds

        j.sal.fs.writeFile(self._cmds_path + namespace + '.py', contents=cmds.code)
        self.logger.info("add cmd namespace %s" % namespace)
