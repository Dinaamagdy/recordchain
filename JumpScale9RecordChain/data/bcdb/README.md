**Basic Idea**

- BCDB is a blockchain DB
- It uses tables as the basic storage unit
- Backend can be any DB (redis/zero-db)
- BCDB tables must have schemas (used to validate input)

- Schema
    - Registered at the time of creating a table
        - You can specify schema string in the time of table creation
        - or you can provide a schema file containing many schemas
        - or you can provide a directory with multiple schema files
    - schema file is  `toml` file starts with `schema`
    - unlike SQL, schema is not a physical thing, it's an application layer 
    - Simple and rich syntax that supports complex data types not supported in other languages like numeric data types that suports
    currencies and can allow changing from currency type to another without effort
    - Table data can be serialized/deserialzed to/from capnp or json
    
    - **Schema types:**
        * L: List
        * LS: List String
        * LI: List Integer
        * LF: List Float
        * D: Date
        * N: Numeric i.e "10 EUR"

    - **schema examples**
    - ```
        schema = """
        @url = despiegk.test
        @name = TestObj
        llist2 = "" (LS)    
        nme* = ""    
        email* = ""
        nr = 0
        date_start = 0 (D)
        description = ""
        token_price = "10 USD" (N)
        cost_estimate:hw_cost = 0.0 #this is a comment
        llist = []
        llist3 = "1,2,3" (LF)
        llist4 = "1,2,3" (L)
        llist5 = "1,2,3" (LI)
        U = 0.0
        #pool_type = "managed,unmanaged" (E)  #NOT DONE FOR NOW
      """
      ```
      
    - ```python
        schema = """
        @url = threefoldtoken.wallet
        @name = wallet
        jwt = "" (S)                # JWT Token
        addr = ""                   # Address
        ipaddr = (ipaddr)           # IP Address
        email = "" (S)              # Email address
        username = "" (S)           # User name
        """ 
        In [20]: schema = j.data.schema.schema_from_url("threefoldtoken.wallet")

        In [21]: schema
        Out[21]: 
        prop:jwt                       (string)
        prop:addr                      (string)
        prop:ipaddr                    (ipaddr)
        prop:email                     (string)
        prop:username                  (string)
        
        In [22]: obj = schema.new()
        
        In [23]: obj
        Out[23]: 
        {
         "addr": "",
         "email": "",
         "ipaddr": "",
         "jwt": "",
         "username": ""
        }
        
        In [24]: obj.jwt = "lovely-jwt"
        
        In [25]: obj.addr = "wallet-addr"
        
        In [26]: obj.ipaddr = '8.8.8.8'
        
        In [27]: obj.username = 'hamdy'
        
        In [28]: obj
        Out[28]: 
        {
         "addr": "wallet-addr",
         "email": "",
         "ipaddr": "8.8.8.8",
         "jwt": "lovely-jwt",
         "username": "hamdy"
        }
        
        In [29]: data = obj.data # serialize (capnp)
        
        In [30]: data
        Out[30]: b'\x10\x0c@\x05\x11\x11Z\x11\x15b\x11\x19B\x00\x00\x11\x152\xfflovely-j\x00\x03wt\xffwallet-a\x00\x07ddr\x7f8.8.8.8\x1fhamdy'
        
        In [31]: obj_from_data = s.get(capnpbin=data)
        
        In [32]: obj_from_data
        Out[32]: 
        {
         "addr": "wallet-addr",
         "email": "",
         "ipaddr": "8.8.8.8",
         "jwt": "lovely-jwt",
         "username": "hamdy"
        }

      ```
      
    - ```python
        @url = test.gedis2.cmd
        @name = any
        name = ""
        comment = ""
        schemacode = ""
        
        @url = test.gedis2.serverschema
        @name = cmds
        cmds = (LO) !test.gedis2.cmd
        
        @url = test.gedis2.cmd1
        @name = cmd
        cmd = (O) !test.gedis2.cmd
        cmd2 = (O) !test.gedis2.cmd
        ```

**Pre-requisites**

- Install zerodb
```bash
js9_code get --url="git@github.com:rivine/0-db.git"`
cd $HOMEDIR/code/github/rivine/0-db && make && cp bin/zdb /opt/bin/`
```

**Start BCDB**
```python
j.data.bcdb.db_start(instance='example',adminsecret='my_secret', reset=False)
```

**Get client**

```python
db = j.data.bcdb.get("example")
```

**Provide  a schema string**
```python
schema = """
        @url = despiegk.test
        @name = TestObj
        llist2 = "" (LS)    
        name* = ""    
        email* = ""
        nr = 0
        date_start = 0 (D)
        description = ""
        token_price = "10 USD" (N)
        cost_estimate:hw_cost = 0.0 #this is a comment
        llist = []
        llist3 = "1,2,3" (LF)
        llist4 = "1,2,3" (L)
        llist5 = "1,2,3" (LI)
        U = 0.0
        #pool_type = "managed,unmanaged" (E)  #NOT DONE FOR NOW
        """

schema2 = """
        @url = despiegk.test
        @name = TestObj2
        name* = ""    
        email* = ""
        nr = 0
        """

db = self.get("example")
t = db.table_get(name="t1", schema=schema)
t2 = db.table_get(name="t1", schema=schema2)
```

**Populate db with test data**

```python
for i in range(10):
    o = t.new() # new table
    o.llist.append(1)
    o.llist2.append("yes")
    o.llist2.append("no")
    o.llist3.append(1.2)
    o.U = 1.1
    o.nr = 1
    o.token_price = "10 EUR"
    o.description = "something"
    o.name = "name%s" % i
    o.email = "info%s@something.com" % i
    o2 = t.set(o)
    assert o2.id == i

o3 = t.get(o2.id)
assert o3.id == o2.id

assert o3.ddict == o2.ddict
assert o3.ddict == o.ddict
```


**Test client**
```python
res = t.find(name="name1", email="info2@something.com")
assert len(res) == 0

res = t.find(name="name2")
assert len(res) == 1
assert res[0].name == "name2"

res = t.find(name="name2", email="info2@something.com")
assert len(res) == 1
assert res[0].name == "name2"

o = res[0]

o.name = "name2"
assert o.changed_prop == False  # because data did not change, was already that data
o.name = "name3"
assert o.changed_prop == True  # now it really changed

assert o.ddict["name"] == "name3"
```

**Provide schema files**

```python
db.tables_get('Schema_file_path_or_schema_files_dir_path') # schemas will be loaded form provided path
```

