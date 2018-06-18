### installation

- Install libssl-dev `apt install libssl-dev`
- `pip3 install python-jose cryptocompare`
- Get recordchain `js9_code get --url="git@github.com:rivine/recordchain.git"`
- Install recordchain `cd $HOMEDIR/code/github/rivine/recordchain && sh install.sh`
- Get 0-db `js9_code get --url="git@github.com:rivine/0-db.git"`
- Install 0-db `cd $HOMEDIR/code/github/rivine/0-db && make && cp bin/zdb /opt/bin/`

### Running

**example**

- Run server `j.servers.gedis2.get('example').run()`
- Get client `j.clients.gedis2.get('example')`
- execute command
    ```
    In [8]: x.system.ping()
    Out[8]: b'PONG'

    ```


**orderbook**
- Run server `j.servers.gedis2.get('orderbook').run()`
- Get client `j.clients.gedis2.get('orderbook')`
- execute command
    ```
    In [8]: x.system.ping()
    Out[8]: b'PONG'
    ```

**Tests**
- `python3 apps/example/test.py`
- `j.clients.gedis2.test()`
- `j.servers.gedis2.test()`

### Explanation

- **Gedis-server**:

    ```
    is a Redis-protocol compatible framework  allowing you to build apps/servers
    on top of it that exposes a Redis protocol interface
    That says, you can connect to your app using any redis client
    It allows you to register your own redis commands and logic, then expose it
    ```

- **Make your own app**
    ```
    app = j.servers.get(instance='my_app')
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

- **Server configuration**
    - `apps_dir` when empty, your app is created under `recordchain/apps/{app_name}`
    - This allows you to see all code generated in your IDE and debug code easily
    - change `apps_dir` to any other location if you want apps else where

- **Gedis-client**

- You can use any redis library to connect to your app and execute commands
- or you use the client from jumpscale
