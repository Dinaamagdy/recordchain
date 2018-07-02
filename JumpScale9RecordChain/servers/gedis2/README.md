# Gedis

A framework that allows for creating applications that are `redis protocol` compatible
and have their own set of `custom redis commands`
Gedis exposes these commands automatically.

You create an `app/instance server` and you can get a `client` that can connect tpo your app
and execute the commands easily

Since `gedis` is a `TCP` level framework, it's very fast and efficient

A `Gedis` server uses [BCDB DB](/JumpScale9RecordChain/data/bcdb/README.md)
that saysm, you can add `schema` toml files to your generated server directory and 
DB tables will be created for each schema you have.
This is the `Model layer`


### installation

- Install libssl-dev `apt install libssl-dev`
- `pip3 install python-jose cryptocompare`
- Get recordchain `js9_code get --url="git@github.com:rivine/recordchain.git"`
- Install recordchain `cd $HOMEDIR/code/github/rivine/recordchain && sh install.sh`
- Get 0-db `js9_code get --url="git@github.com:rivine/0-db.git"`
- Install 0-db `cd $HOMEDIR/code/github/rivine/0-db && make && cp bin/zdb /opt/bin/`

### Tests
- `python3 apps/example/test.py`
- `j.clients.gedis2.test()`
- `j.servers.gedis2.test()`

### Running

**Hello world example**
Get the `example` app in [HERE](/JumpScale9RecordChain/apps/)

- Configure & Run server `j.servers.gedis2.get('example').start()`
- Configure & Get client `client = j.clients.gedis2.get('example')`
- execute system command `ping`
    ```
    client.system.ping()
    b'PONG'
    ```
- Instance name here refers to application name. In this case our app is called `example`
- During configuration phase for this helloworld example, leve `apps_dir` empty for both server & client
This ensures that apps dir will be set to `/JumpScale9RecordChain/apps/` and that the `helloworld` app called `example` will be loaded from there

### General Picture for how Server & client work and comunicate

**Server**

- Creates `apps_dir/{instance}/server` directory in the 1st time
- Copies `system.py` to `apps_dir/{instance}/server` which contains system redis commands like `ping`
- For each python file not starting with `model_` inside `apps_dir/{instance}/server`
    - take the file name as a namespace and register all functions inside it as custom redis commands in that namespace
    - example `system.py` will produce a name space called `system` with custom commands like `system.ping()` 
- collect schemas in toml file(s) that starts with `schema_` in `apps_dir/{instance}/server`
- Collect schemas defined in the doc string of custom redis commands / API in each file in `apps_dir/{instance}/server` that does not start with `model_`  
- For each schema collected 
    - create a schema file for that schema in `apps_dir/{instance}/schema`
    - load schema in memory
    - create db table with the same name as schema name
    - create model file names `model_{schema_name}.py` under `apps_dir/{instance}/server` and add it to dictionary
    `j.servers.gedis2.latest.db.tables`.
    - models allow for `CRUD` operations on a table

**Client**
- Creates `apps_dir/{instance}/client` directory in the 1st time
- Fetch server for all schemas loaded inside it
- Create `apps_dir/{instance}/schema`
- For each schema in loaded schemas
    - create a schema file for that schema in `apps_dir/{instance}/schema`
    - load schema in memory
    - create model file names `model_{schema_name}.py` under `apps_dir/{instance}/client` and add it to client instance
    in `models` property so it can be accessed through `client.models.{model_name}`
- Fetch server for each registered command
- For each namespace registered in server
    - create `apps_dir/{instance}/client/cmds_{instance}_{namespace}.py` file containign all commands in that name space
    - for each command, make sure if `schema_in` for a command is provided to expand its properties in the client command function arguments

**apps_dir**
- `apps_dir` of server and client if you run them in separate machines, need not to match
- `apps_dir` of server and client if run in same machine may match (for simplicity) in order to have one dir for code gen
but they don't have to

### Make your own app

- **Make your own app**
    ```
    app = j.servers.gedis2.get(instance='my_app')
    app.start()
    ```

    OR configure it directly like

    ```
    server = j.servers.gedis2.configure(
            instance="example",
            port=5000,
            host="127.0.0.1",
            secret="",
            apps_dir=''
        )

    server.start()
    ```

- **Gedis-client**

- You can use any redis library to connect to your app and execute commands
- or you use the client from jumpscale `j.clients.gedis2.get({instance})`

- **Adding models to your server** 
    - In your `{apps_dir}/{instance_name}/server` you can add some `toml` files MUST start with `schema`.
    - These schema files represent the `Model` layer in an `MVC` framework these are your models
    - example [HERE](https://github.com/rivine/recordchain/blob/master/JumpScale9RecordChain/apps/orderbook/schema.toml) 

- **Add custom redis commands / API**
    - In your `{apps_dir}/{instance_name}/server` add a python file MUST not start with `model_`
    - Example:
        - file `system.py`
            ```python
            from js9 import j
        
            JSBASE = j.application.jsbase_get_class()
            
            class system(JSBASE):
                
                def __init__(self):
                    JSBASE.__init__(self)
            
                def ping(self):
                    return "PONG"
            
                def ping_bool(self):
                    return True
            ```
         
        - each function is registered in client as a redis command under `client.system.{function name}`
        i.e `client.system.ping()` or  `client.system.ping_bool()`

    - How to define a custom redis command:
        - If you have simple function with no input and returning simple data type ay like boolean, list, string, .. in this case no need to do anything, just return directly as in `ping`
            ```python
              def ping(self):
                    return "PONG"
            
                def ping_bool(self):
                    return True
            ```
        - If you have inputs, you must define `in` schema in your docstring and if you have output schema, you must
        define `out` schema in docstring as well as a `schema_out` argument to the function
        ```python
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
