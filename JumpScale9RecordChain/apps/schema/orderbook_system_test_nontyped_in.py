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
    def nr(self):
 
 
        if self.changed_prop and "nr" in self.changed_items:
            return self.changed_items["nr"]
        else:
            return self._cobj.nr
 
        
    @nr.setter
    def nr(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.integer.clean(val)
        # self._cobj.nr = val        
        if self.nr != val:
            self.changed_prop = True
            self.changed_items["nr"] = val
 



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
                if "nr" in self.changed_items:
                    ddict["nr"] = self.changed_items["nr"]
                

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
    
        d["nr"] = self.nr
    

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
        d["nr"] = j.data.types.integer.toHR(self.nr)
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