


from js9 import j

# JSBASE = j.application.jsbase_get_class()

class CMDS():
    
    def __init__(self,client,cmds):
        # JSBASE.__init__(self)   
        self._client = client
        self._redis = client.redis   
        self._cmds = cmds
        self._name = "system"



    def api_meta(self):
        '''
        return the api meta information
        '''

  
        return self._redis.execute_command("system.api_meta")
        
        
        return res






    def core_schemas_get(self):
        '''
        return all core schemas as understood by the server, is as text, can be processed by j.data.schema
        '''

  
        return self._redis.execute_command("system.core_schemas_get")
        
        
        return res






    def ping(self):
        '''

        '''

  
        return self._redis.execute_command("system.ping")
        
        
        return res






    def ping_bool(self):
        '''

        '''

  
        return self._redis.execute_command("system.ping_bool")
        
        
        return res






    def schema_urls(self):
        '''
        return the api meta information
        '''

  
        return self._redis.execute_command("system.schema_urls")
        
        
        return res






    def test(self,name='', nr=0):
        '''
        some test method, which returns something easy
        '''

        #schema in exists
        schema_in = self._cmds["test"].schema_in
        args = schema_in.new()
        args.name = name
        args.nr = nr

        res = self._redis.execute_command("system.test",args.data)

        
        
        schema_out = self._cmds["test"].schema_out
        obj = schema_out.get(capnpbin=res)
        return obj






    def test_nontyped(self,name='', nr=0):
        '''
        some test method, which returns something easy
        '''

        #schema in exists
        schema_in = self._cmds["test_nontyped"].schema_in
        args = schema_in.new()
        args.name = name
        args.nr = nr

        res = self._redis.execute_command("system.test_nontyped",args.data)

        
        
        return res




