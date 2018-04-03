
from js9 import j
import signal
import gevent
import gevent.signal
from gevent.pool import Pool
from gevent.server import StreamServer
from .protocol import CommandParser, ResponseWriter
import inspect
import imp

TEMPLATE = """
addr = "localhost"
port = "9900"
# ssl = false
adminsecret_ = ""
"""
JSConfigBase = j.tools.configmanager.base_class_config


class GedisServer(StreamServer, JSConfigBase):

    def __init__(self,instance, data={}, parent=None, interactive=False,template=None):
        """
        """        
        if not template:
            template = TEMPLATE
        JSConfigBase.__init__(self, instance=instance, data=data,
                              parent=parent, template=template, interactive=interactive)
        host = self.config.data["addr"]
        port = int(self.config.data["port"])

        self.address = '{}:{}'.format(host, port)
        # import ipdb; ipdb.set_trace()
        if self.config.data['ssl']:
            self.logger.info("ssl enabled, keys in %s"%self.ssl_priv_key_path)
            self.sslkeys_generate()

            #############7ossam
            # there was no session here on tmux, happened first, come here again call it three
            #4 this appeared on tmux, again on tmux call it 5
            # outside of tmux after failure this appeared
            self.server = StreamServer(
                (host, port), spawn=Pool(), handle=self.__handle_connection, keyfile=self.ssl_priv_key_path, certfile=self.ssl_cert_path)
        else:
            self.server = StreamServer(
                (host, port), spawn=Pool(), handle=self.__handle_connection)

        self._sig_handler = []
        # commands callbacks
        self._cmds_path = j.sal.fs.getParent(self.config.path) + 'cmds.py'
        self._cmds = {}

    def sslkeys_generate(self):
        
        res=j.sal.ssl.ca_cert_generate(j.sal.fs.getDirName(self.config.path))
        if res:
            self.logger.info("generated sslkeys for gedis in %s"%self.config.path)
        

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


    def register_command(self, cmd, callback):
        # import ipdb;ipdb.set_trace()
        self.logger.info("add cmd %s" % cmd)
        content = inspect.getsource(callback)
        j.sal.fs.writeFile(self._cmds_path, contents='\n'+content, append=True)


    def __handle_connection(self, socket, address):
        # import ipdb; ipdb.set_trace()
        self.logger.info('connection from {}'.format(address))
        parser = CommandParser(socket)
        response = ResponseWriter(socket)

        self._cmds = imp.load_source(pathname=self._cmds_path)

        try:
            while True:
                request = parser.read_request()
                cmd = request[0]
                if cmd not in self._cmds.__dir__():
                    response.error('command not supported')
                    continue

                # execute command callback
                result = ""
                try:
                    result = getattr(self._cmds, cmd)(request)
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

    #DEFAULT COMMAND ALWAYS THERE
    def ping_cmd(self,request):
        return "PONG"

    def start(self):
        self.logger.info("init server")
        j.logger.enabled = False
        self._logger = None

        for item in self.__dir__():
            # self.logger.debug("method:%s"%item)
            if item.endswith("_cmd"):
                # import ipdb;ipdb.set_trace()
                item2 = item[:-4]
                # found a method which is a command
                cmd = eval("self.%s" % item)
                self.register_command(item2, cmd)

        self._sig_handler.append(gevent.signal(signal.SIGINT, self.stop))

        self.logger.info("start server")
        #SHOULD NOT IMPLEMENT BACKGROUND HERE HAS BEEN DONE AT FACTORY LEVEL
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
