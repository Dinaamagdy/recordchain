**Basic Idea**

- BCDB is a blockchain DB
- It uses tables as the basic storage unit
- Backend can be any DB (redis/zero-db)
- BCDB tables must have schemas (used to validate input)

- Schema
    - More info on schemas can be found [HERE](/JumpScale9RecordChain/data/schema/README.md)
    - Registered at the time of creating a table
        - You can specify schema string in the time of table creation
        - or you can provide a schema file containing many schemas
        - or you can provide a directory with multiple schema files
    - schema file is  `toml` file starts with `schema`
    - unlike SQL, schema is not a physical thing, it's an application layer
 
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

