import inspect
from js9 import j

from .protocol import CommandParser, ResponseWriter


class Handler(object):
    def __init__(self, server):
        self.server = server
        self.logger = server.logger

    def handle(
            self,
            socket,
            address
    ):
        self.logger.info('connection from {}'.format(address))
        parser = CommandParser(socket)
        response = ResponseWriter(socket)
        try:
            while True:
                request = parser.read_request()

                if not request:  # empty string request
                    response.error('Empty request body .. probably this is a (TCP port) checking query')
                    continue

                # Get CMD
                cmd = request[0]
                redis_cmd = cmd.decode("utf-8").lower()
                cmd, err = self.get_command(redis_cmd)
                params = None  # CMD params
                if err:
                    response.error(err)
                    continue

                if cmd.schema_in:
                    params = {}

                    if len(request) < 2:
                        response.error("need to have arguments, none given")
                        continue

                    if len(request) > 2:
                        response.error("more than 1 argument given, needs to be binary capnp message or json")
                        continue

                    cmd_vars =inspect.getargspec(cmd.method).args[1:] # remove self

                    if cmd.schema_out:
                        params["schema_out"] = cmd.schema_out
                        cmd_vars.pop(-1)

                    o = cmd.schema_in.get(capnpbin=request[1])
                    schema_dict = o.ddict
                    if "id" in schema_dict:
                        schema_dict.pop("id")

                    # arguments passed are same number as in_schema provided
                    if len(cmd_vars) == len(schema_dict):
                        params.update(schema_dict)
                    elif len(cmd_vars) == 1:
                        params[cmd_vars[0]] = o
                    else:
                        params.update(schema_dict)
                else:
                    if len(request) == 1:
                        if cmd.schema_out:
                            params = {"schema_out": cmd.schema_out}
                    elif len(request) > 1:
                        params = request[1:]

                # execute command callback
                self.logger.debug("execute command callback:%s:%s" % (cmd, params))
                result = None

                try:
                    if params is None:
                        result = cmd.method()
                    elif j.data.types.list.check(params):
                        result = cmd.method(*params)
                    else:
                        result = cmd.method(**params)
                except Exception as e:
                    eco = j.errorhandler.parsePythonExceptionObject(e)
                    msg = str(eco)
                    msg += "\nCODE:%s:%s\n" % (cmd.namespace, cmd.name)
                    self.logger.error(msg)
                    response.error(e.args[:100])
                    continue


                self.logger.debug("Callback done and result {} , type {}".format(result, type(result)))

                self.logger.debug(
                    "response:{}:{}:{}".format(address, cmd, result))

                if cmd.schema_out:
                    result = result.data

                response.encode(result)

        except ConnectionError as err:
            self.logger.error('connection error: {}'.format(str(err)))
        finally:
            parser.on_disconnect()
            self.logger.info('close connection from {}'.format(address))

    def get_command(self, cmd):
        if cmd in self.server.cmds:
            return self.server.cmds[cmd], ''

        self.logger.debug('(%s) command cache miss')

        if not '.' in cmd:
            return None, 'Invalid command (%s) : model is missing. proper format is {model}.{cmd}'

        pre, post = cmd.split(".", 1)

        namespace = self.server.instance + "." + pre

        if namespace not in self.server.classes:
            return None, "Cannot find namespace:%s " % (namespace)

        if namespace not in self.server.cmds_meta:
            return None, "Cannot find namespace:%s" % (namespace)

        meta = self.server.cmds_meta[namespace]

        if not post in meta.cmds:
            return None, "Cannot find method with name:%s in namespace:%s" % (post, namespace)

        cmd_obj = meta.cmds[post]

        try:
            cl = self.server.classes[namespace]
            m = eval("cl.%s" % (post))
        except Exception as e:
            return None, "Could not execute code of method '%s' in namespace '%s'\n%s" % (pre, namespace, e)

        cmd_obj.method = m

        self.server.cmds[cmd] = cmd_obj

        return self.server.cmds[cmd], ""
