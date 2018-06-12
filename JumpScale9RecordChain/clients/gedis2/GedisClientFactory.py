from js9 import j

JSConfigBase = j.tools.configmanager.base_class_configs
from .GedisClient import GedisClient


class GedisClientCmds():
    def __init__(self):
        pass

    def __str__(self):
        if self._client.config.data["ssl"]:
            return "Gedis Client: (instance=%s) (address=%s:%-4s)\n(ssl=True, certificate:%s)" % (
                self._client.instance,
                self._client.config.data["host"],
                self._client.config.data["port"],
                self._client.config.data["ssl_cert_file"]
            )

        return "Gedis Client: (instance=%s) (address=%s:%-4s)" % (
            self._client.instance,
            self._client.config.data["addr"],
            self._client.config.data["port"]
        )

    __repr__ = __str__


class GedisClientFactory(JSConfigBase):
    def __init__(self):
        self.__jslocation__ = "j.clients.gedis2"
        JSConfigBase.__init__(self, GedisClient)
        self._template_engine = None
        self._template_code_client = None
        self._code_model_template = None

    def get(
        self,
        instance='main',
        data={}
    ):
        client = super(GedisClientFactory, self).get(instance=instance, data=data)
        if client._connected:
            cl = GedisClientCmds()
            cl._client = client
            cl.models = client.models
            cl.__dict__.update(cl._client.cmds.__dict__)
            return cl

    def configure(
        self,
        instance="main",
        host="localhost",
        port=5000,
        secret="",
        apps_dir="",
        ssl=True,
        ssl_cert_file=""
    ):

        data = {}

        data["host"] = host
        data["port"] = port
        data["secret_"] = secret
        data["ssl"] = ssl
        data['apps_dir'] = apps_dir
        data['ssl_cert_file'] = ssl_cert_file

        return self.get(instance=instance, data=data)

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
        if self._template_code_client is None:
            self._template_code_client = self.template_engine.get_template("template.py")
        return self._template_code_client

    @property
    def code_model_template(self):
        if self._code_model_template is None:
            self._code_model_template = self.template_engine.get_template("ModelBase.py")
        return self._code_model_template
