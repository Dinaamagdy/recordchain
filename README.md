## recordchain for python

- gevent redis server
- blockchain logic
- zerodb client


### installation

```bash
js9_code get --url="git@github.com:rivine/recordchain.git"
cd $HOMEDIR/code/github/rivine/recordchain
sh install.sh
```

### Code Generations Path


### Server

- *Generated server code is by default in : `gedis2/apps/{instance}/server`*

**Configuration**
- Sample config

    ```
    host = "localhost"
    port = 9900
    secret_ = ""
    apps_dir = ""
    ```

- `apps_dir`
    - the directory containing all gedis2 apps
    - if left empty, default is `gedis2/apps/{instance}`


**Start** *(In Tmux)*

    ```
    x = j.servers.gedis2.get('example')
    x.start()
    ```

    OR

    ```
    server = j.servers.gedis2.configure(
        instance="example",
        port=5000,
        host="127.0.0.1",
        secret="",
        apps_dir=apps_dir
    )

    server.start()
    ```


## client

*Generated client code is by default in : `gedis2/apps/{instance}/client`*

**Configuration**

- Sample config

    ```
    addr = 'localhost'
    password_ = ''
    port = 5000
    ssl = true
    ssl_cert_file = ''
    ```

- SSL support
    - Gedis2 Server by default generates cert file in `/opt/var/codegen/{namespace}/ca.crt`
    - Enable SSL for client by setting `ssl = true`
    - Certificate file is taken from `ssl_cert_file` if not empty, otherwise `/opt/var/codegen/{namespace}/ca.crt`

**Get Gedis2 client**

  - *Use configuration from config file*
    ```
    In [6]: cl = j.clients.gedis2.get(instance='test')
    In [7]: cl.redis.execute_command('system.ping')
    Out[7]: b'PONG'
    ```
  - *Provide your own configuration on the fly*
    ```
    cl = j.clients.gedis2.configure(
        instance="test",
        ipaddr="localhost",
        port=5000,
        password="",
        ssl=True,
        ssl_cert_file=None
    )

    In [7]: cl.system.ping()
    Out[7]: b'PONG'
    ```

**Tests**

- *Run client tests using*
    ```
    j.clients.gedis2.test()
    ```
