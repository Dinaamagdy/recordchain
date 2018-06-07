from JumpScale9 import j

List0=j.data.schema.list_base_class_get()

class ModelOBJ():
    
    def __init__(self,schema,data={}, capnpbin=None):
        self.schema = schema
        self.capnp = schema.capnp

        self.changed_list = False
        self.changed_prop = False
        self.changed_items = {}

        if capnpbin != None:
            self._cobj = self.capnp.from_bytes_packed(capnpbin)
        else:
            self._cobj = self.capnp.new_message()

        for key,val in data.items():
            self.__dict__[key] = val


        self._JSOBJ = True

        self.id = None
        self.changed_prop_permanent = False
        self.schema_cmd = j.data.schema.schema_from_url("test.gedis2.cmd")
        self.changed_prop = True
        self.changed_prop_permanent = True
        if self._cobj.cmd:
            self.changed_items["cmd"] = self.schema_cmd.get(capnpbin=self._cobj.cmd)
        else:
            self.changed_items["cmd"] = self.schema_cmd.new()         
 
        self.schema_cmd2 = j.data.schema.schema_from_url("test.gedis2.cmd")
        self.changed_prop = True
        self.changed_prop_permanent = True
        if self._cobj.cmd2:
            self.changed_items["cmd2"] = self.schema_cmd2.get(capnpbin=self._cobj.cmd2)
        else:
            self.changed_items["cmd2"] = self.schema_cmd2.new()         
 


    @property 
    def cmd(self):
 
        return self.changed_items["cmd"]
 
        
    @cmd.setter
    def cmd(self,val):
        self.changed_items["cmd"] = val
 


    @property 
    def cmd2(self):
 
        return self.changed_items["cmd2"]
 
        
    @cmd2.setter
    def cmd2(self,val):
        self.changed_items["cmd2"] = val
 



    def check(self):
        #checks are done while creating ddict, so can reuse that
        self.ddict
        return True

    @property
    def cobj(self):
        if self.changed_list or self.changed_prop:
            ddict = self._cobj.to_dict()

            if self.changed_list:
                # print("cobj")
                pass

        
            if self.changed_prop:
                pass
        
                #convert jsobjects to capnpbin data
                if "cmd" in self.changed_items:
                    ddict["cmd"] = self.changed_items["cmd"].data
        
                #convert jsobjects to capnpbin data
                if "cmd2" in self.changed_items:
                    ddict["cmd2"] = self.changed_items["cmd2"].data
                

            try:
                self._cobj = self.capnp.new_message(**ddict)
            except Exception as e:
                msg="\nERROR: could not create capnp message\n"
                try:
                    msg+=j.data.text.indent(j.data.serializer.json.dumps(ddict,sort_keys=True,indent=True),4)+"\n"
                except:
                    msg+=j.data.text.indent(str(ddict),4)+"\n"
                msg+="schema:\n"
                msg+=j.data.text.indent(str(self.schema.capnp_schema),4)+"\n"
                msg+="error was:\n%s\n"%e
                raise RuntimeError(msg)

            self.changed_reset()

        return self._cobj

    @property
    def data(self):        
        try:
            self.cobj.clear_write_flag()
            return self.cobj.to_bytes_packed()
        except:
            self._cobj=self.cobj.as_builder()
            return self.cobj.to_bytes_packed()

    def changed_reset(self):
        if self.changed_prop_permanent:
            return
        self.changed_list = False
        self.changed_prop = False
        self.changed_items = {}
        
        
    @property
    def ddict(self):
        d={}
        d["cmd"] = self.cmd.ddict
    
        d["cmd2"] = self.cmd2.ddict
    

        if self.id is not None:
            d["id"]=self.id
        return d

    @property
    def ddict_hr(self):
        """
        human readable dict
        """
        d={}
        d["cmd"] = self.cmd.ddict
        d["cmd2"] = self.cmd2.ddict
        if self.id is not None:
            d["id"]=self.id
        return d

    @property
    def json(self):
        return j.data.serializer.json.dumps(self.ddict)

    @property
    def msgpack(self):
        return j.data.serializer.msgpack.dumps(self.ddict)

    def __str__(self):
        return j.data.serializer.json.dumps(self.ddict_hr,sort_keys=True, indent=True)

    __repr__ = __str__