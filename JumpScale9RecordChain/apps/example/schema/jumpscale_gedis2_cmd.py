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
 
 
 
 
 
 


    @property 
    def name(self):
 
 
        if self.changed_prop and "name" in self.changed_items:
            return self.changed_items["name"]
        else:
            return self._cobj.name
 
        
    @name.setter
    def name(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.name = val        
        if self.name != val:
            self.changed_prop = True
            self.changed_items["name"] = val
 


    @property 
    def comment(self):
 
 
        if self.changed_prop and "comment" in self.changed_items:
            return self.changed_items["comment"]
        else:
            return self._cobj.comment
 
        
    @comment.setter
    def comment(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.comment = val        
        if self.comment != val:
            self.changed_prop = True
            self.changed_items["comment"] = val
 


    @property 
    def code(self):
 
 
        if self.changed_prop and "code" in self.changed_items:
            return self.changed_items["code"]
        else:
            return self._cobj.code
 
        
    @code.setter
    def code(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.code = val        
        if self.code != val:
            self.changed_prop = True
            self.changed_items["code"] = val
 


    @property 
    def schema_in(self):
 
 
        if self.changed_prop and "schemaIn" in self.changed_items:
            return self.changed_items["schemaIn"]
        else:
            return self._cobj.schemaIn
 
        
    @schema_in.setter
    def schema_in(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.schemaIn = val        
        if self.schema_in != val:
            self.changed_prop = True
            self.changed_items["schemaIn"] = val
 


    @property 
    def schema_out(self):
 
 
        if self.changed_prop and "schemaOut" in self.changed_items:
            return self.changed_items["schemaOut"]
        else:
            return self._cobj.schemaOut
 
        
    @schema_out.setter
    def schema_out(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.schemaOut = val        
        if self.schema_out != val:
            self.changed_prop = True
            self.changed_items["schemaOut"] = val
 


    @property 
    def args(self):
 
 
        if self.changed_prop and "args" in self.changed_items:
            return self.changed_items["args"]
        else:
            return self._cobj.args
 
        
    @args.setter
    def args(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.args = val        
        if self.args != val:
            self.changed_prop = True
            self.changed_items["args"] = val
 



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
                if "name" in self.changed_items:
                    ddict["name"] = self.changed_items["name"]
        
                #convert jsobjects to capnpbin data
                if "comment" in self.changed_items:
                    ddict["comment"] = self.changed_items["comment"]
        
                #convert jsobjects to capnpbin data
                if "code" in self.changed_items:
                    ddict["code"] = self.changed_items["code"]
        
                #convert jsobjects to capnpbin data
                if "schemaIn" in self.changed_items:
                    ddict["schemaIn"] = self.changed_items["schemaIn"]
        
                #convert jsobjects to capnpbin data
                if "schemaOut" in self.changed_items:
                    ddict["schemaOut"] = self.changed_items["schemaOut"]
        
                #convert jsobjects to capnpbin data
                if "args" in self.changed_items:
                    ddict["args"] = self.changed_items["args"]
                

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
        d["name"] = self.name
    
        d["comment"] = self.comment
    
        d["code"] = self.code
    
        d["schema_in"] = self.schema_in
    
        d["schema_out"] = self.schema_out
    
        d["args"] = self.args
    

        if self.id is not None:
            d["id"]=self.id
        return d

    @property
    def ddict_hr(self):
        """
        human readable dict
        """
        d={}
        d["name"] = j.data.types.string.toHR(self.name)
        d["comment"] = j.data.types.string.toHR(self.comment)
        d["code"] = j.data.types.string.toHR(self.code)
        d["schema_in"] = j.data.types.string.toHR(self.schema_in)
        d["schema_out"] = j.data.types.string.toHR(self.schema_out)
        d["args"] = j.data.types.string.toHR(self.args)
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