import os
import sys

from js9 import j

JSConfigBase = j.tools.configmanager.base_class_configs
from .GedisClient import GedisClient


class GedisClientCmds():
    def __init__(self):
        pass


class GedisClientFactory(JSConfigBase):
    """
    is nothing more for now than the redis_config client
    """

    def __init__(self):
        self.__jslocation__ = "j.clients.gedis2"
        JSConfigBase.__init__(self, GedisClient)
        self._template_engine = None
        self._template_code_client = None
        self._code_model_template = None

        self.code_generation_dir = os.path.join(j.dirs.VARDIR, 'codegen', 'gedis')

        if not j.sal.fs.exists(self.code_generation_dir):
            j.sal.fs.createDir(self.code_generation_dir)

        if not self.code_generation_dir in sys.path:
            sys.path.append(self.code_generation_dir)

        j.sal.fs.touch(os.path.join(self.code_generation_dir, '/__init__.py'))
        self.logger.debug("codegendir:%s" % self.code_generation_dir)    
        
    def client_get(self,instance="main", data={}):
        client = self.get(instance=instance, data=data)
        cl=GedisClientCmds()
        cl._client = client
        cl.models = client.models
        cl.__dict__.update(cl._client.cmds.__dict__)
        return cl
        
    def configure(
        self,
        instance="main",
        ipaddr="localhost",
        port=5000,
        password="",
        unixsocket="",
        ssl=False,
        ssl_certfile=None
    ):

        """
        #TODO:*1 need to define well what this keyfile/certfile is
        """
        data = {}
        data["addr"] = ipaddr
        data["port"] = port
        data["password_"] = password
        data["unixsocket"] = unixsocket
        data["ssl"] = ssl
        if ssl_certfile:
            #check if its a path, if yes load
            data["ssl"] = True
            data['ssl_cert_file'] = ssl_certfile
        else:
            # SSL is true but no certificate provided
            # Use default location
            if ssl:
                path = os.path.join(
                    os.path.join(
                        j.dirs.VARDIR,
                        'codegen',
                        'gedis',
                        instance,
                        'ca.crt'
                    ))
                data['ssl_cert_file'] = path
        if ssl:
            self.logger.info('Gedis2 client : Using SSL certificate from %s' % data['ssl_cert_file'])

        # make sure instance is configured
        # self.get(instance=instance, data=data)
        return self.client_get(instance=instance, data=data)

    @property
    def _path(self):
        return j.sal.fs.getDirName(os.path.abspath(__file__))


    @property
    def template_engine(self):
        if self._template_engine is None:
            from jinja2 import Environment, PackageLoader

            self._template_engine = Environment(
                loader=PackageLoader('JumpScale9RecordChain.clients.gedis2', 'templates'),
                trim_blocks=True,
                lstrip_blocks=True,
            )
        return self._template_engine

    @property
    def code_client_template(self):
        if self._template_code_client == None:
            self._template_code_client = self.template_engine.get_template("template.py")
        return self._template_code_client

    @property
    def code_model_template(self):
        if self._code_model_template == None:
            self._code_model_template = self.template_engine.get_template("ModelBase.py")
        return self._code_model_template


    def test(self, dobenchmarks=True):
        """
        js9 'j.clients.gedis2.test()'

        """
        schema_path = j.sal.fs.getDirName(
            j.sal.fs.getDirName(
                j.sal.fs.getDirName(
                    os.path.abspath(__file__)
                )
            )) + "servers/gedis2/EXAMPLE"


        j.servers.gedis2.configure(
            instance="test",
            port=5000,
            namespace='jumpscale.gedis2.example',
            ssl=True,
            start=True,
            background=True,
            path=schema_path
        )

        cl = j.clients.gedis2.configure(
            instance="test",
            ipaddr="localhost",
            port=5000,
            password="",
            unixsocket="",
            ssl=True,
            ssl_certfile=None
        )

        o=cl.models.test_gedis2_cmd1.new()
        o.cmd.name="aname"
        o.cmd2.name="aname2"
        o2=cl.models.test_gedis2_cmd1.set(o)
        o3=cl.models.test_gedis2_cmd1.set(o2) #make sure id stays same, id should be 1 & stay 1

        assert o2.id==o3.id

        o4=cl.models.test_gedis2_cmd1.get(o3.id)

        assert o3.ddict==o4.ddict

        res = cl.system.test_nontyped("name", 10)
        assert j.data.serializer.json.loads(res) == ['name', 10]

        s = j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.in')
        o = s.new()
        o.name = "aname"
        o.nr = 1

        res = cl.system.test("aname", 1)

        s = j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.out')

        o2 = s.get(capnpbin=res.data)

        assert o.name == o2.name
        assert cl.system.ping() == b'PONG'
        assert cl.system.ping_bool() == 1
        
        