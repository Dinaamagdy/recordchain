

from js9 import j

JSBASE = j.application.jsbase_get_class()

class system(JSBASE):
    
    def __init__(self):
        JSBASE.__init__(self)

    def ping(self):
        return "PONG"

    def ping_bool(self):
        return True

    def core_schemas_get(self):
        """
        return all core schemas as understood by the server, is as text, can be processed by j.data.schema

        """
        res = {}        
        for key,item in j.data.schema.schemas.items():
            res[key] = item.text
        return j.data.serializer.msgpack.dumps(res)

    def api_meta(self):
        """
        return the api meta information

        """  
        s=j.servers.gedis2.latest.cmds_meta
        res={}
        res["namespace"]=j.servers.gedis2.latest.namespace
        res["cmds"]={}
        for key,item in s.items():
            res["cmds"][key] = item.data.data
        return j.data.serializer.msgpack.dumps(res)

    def schema_urls(self):
        """
        return the api meta information

        """  
        s=j.servers.gedis2.latest.schema_urls
        return j.data.serializer.msgpack.dumps(s)

    def test(self,name,nr,schema_out):      
        """
        some test method, which returns something easy

        ```in
        name = "" (S)
        nr = 0 (I)
        ```

        ```out
        name = "" (S)
        nr = 0 (I)
        ```
        """
        o=schema_out.new()
        o.name = name
        o.nr = nr
        return o

    def test_nontyped(self,name,nr):
        """
        some test method, which returns something easy

        ```in
        name = "" (S)
        nr = 0 (I)
        ```

        """
        return [name, nr]