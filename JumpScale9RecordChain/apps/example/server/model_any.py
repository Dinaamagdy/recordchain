

from js9 import j

JSBASE = j.application.jsbase_get_class()

SCHEMA="""
@url = test.gedis2.cmd
@name = any
name = ""
comment = ""
schemacode = ""


"""

class model_any(JSBASE):
    
    def __init__(self):
        JSBASE.__init__(self)        
        self.namespace = "any"
        self.url = "test.gedis2.cmd"
        self.db = j.servers.gedis2.latest.db
        self.table = self.db.tables["any"]
        self.schema = self.table.schema

    def set(self,data_in):
        if j.servers.gedis2.latest.serializer:
            #e.g. for json
            ddict = j.servers.gedis2.latest.return_serializer.loads(data_in)
            obj = self.schema.get(data=ddict)
            data = obj.data
        else:
            id,data = j.data.serializer.msgpack.loads(data_in)

        res=self.table.set(data=data, id=id, hook=self.hook_set)
        if res.id == None:
            raise RuntimeError("cannot be None")

        if j.servers.gedis2.latest.serializer:
            return j.servers.gedis2.latest.return_serializer.dumps(res.ddict)
        else:
            return j.data.serializer.msgpack.dumps([res.id,res.data])

    def get(self, id):
        id=int(id.decode())
        obj = self.table.get(id=id, hook=self.hook_get)
        print("get")
        if j.servers.gedis2.latest.serializer:
            return j.servers.gedis2.latest.return_serializer.dumps(obj.ddict)
        else:
            return j.data.serializer.msgpack.dumps([obj.id,obj.data])

    def find(self,**args):
        return self.table.find(hook=self.hook_get,**args)
        
    def new(self):
        return self.table.new()

    def hook_set(self,obj,index=None):
        """
        before an object is set in the DB it will pass through this function, 
        this allows addional manipulation of object or security checks
        """
        return obj

    def hook_get(self,obj):
        """
        after an object is retreived from DB but before send to the consumer
        it will pass through this function, 
        this allows addional manipulation of object or security checks
        """
        return obj

