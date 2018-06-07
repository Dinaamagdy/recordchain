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

    
        self.cmds = List0(self,self._cobj.cmds, self.schema.property_cmds)

        self._JSOBJ = True

        self.id = None
        self.changed_prop_permanent = False
 


    @property 
    def namespace(self):
 
 
        if self.changed_prop and "namespace" in self.changed_items:
            return self.changed_items["namespace"]
        else:
            return self._cobj.namespace
 
        
    @namespace.setter
    def namespace(self,val):
 
        #will make sure that the input args are put in right format
        # val = j.data.types.string.clean(val)
        # self._cobj.namespace = val        
        if self.namespace != val:
            self.changed_prop = True
            self.changed_items["namespace"] = val
 



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
                if self.cmds._copied:
                    #means the list was modified
                    if "cmds" in ddict:
                        ddict.pop("cmds")
                    ddict["cmds"]=[]
                    for item in self.cmds._inner_list:
                        if self.cmds.schema_property.pointer_type is not None:
                            #use data in stead of rich object
                            item = item.data
                        ddict["cmds"].append(item)

        
            if self.changed_prop:
                pass
        
                #convert jsobjects to capnpbin data
                if "namespace" in self.changed_items:
                    ddict["namespace"] = self.changed_items["namespace"]
                

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
    
        self.cmds = List0(self,self._cobj.cmds, self.schema.property_cmds)
        
        
    @property
    def ddict(self):
        d={}
        d["namespace"] = self.namespace
    

        #check if the list has the right type
        d["cmds"] = self.cmds.pylist
        if self.id is not None:
            d["id"]=self.id
        return d

    @property
    def ddict_hr(self):
        """
        human readable dict
        """
        d={}
        d["namespace"] = j.data.types.string.toHR(self.namespace)
        #check if the list has the right type
        if isinstance(self.cmds, list):
            d["cmds"] = self.cmds
        else:
            d["cmds"] = self.cmds.pylist
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