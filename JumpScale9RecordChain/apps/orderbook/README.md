## Orderbook

Orderbook is a Gedis app, that says you need to be familiar with
these topics before you can work with orderbook

- [Schemas](JumpScale9RecordChain/data/schema/README.md)
- [BCDB database](JumpScale9RecordChain/data/bcdb/README.md)
- [GEDIS2 Framework](JumpScale9RecordChain/servers/gedis2/README.md)

# Specs

- Read about specs [HERE](JumpScale9RecordChain/apps/orderbook/specs.md)


# Orderbook

- #### Start server
    - Make sure in config to leave `apps_dir` empty to load ordrbook from `JumpScale9RecordChain/apps/orderbook`
    - Orderbook is an instance of gedis and you can start server using
        ```python
        server = j.servers.gedis2.get('orderbook')
        server.start()
        ```

- #### Start client
    ```python
    client = j.clients.gedis2.get('orderbook')
    ```
- ####  USing client
    
    - **Test client working**
        - Issue the command
            ```python
            client.system.ping()
            ```
        - Result shoule be `PONG`

    - **Get a valid Itsyouonline JWT Token**

        ```python
        iyo_client = j.clients.itsyouonline.get()
        jwt = iyo_client.jwt
        ```
    
    -  **Client Login/Register client wallet**
        ```python
          client.order_book.login(jwt=jwt, ipaddr='my-wallet-ip', addr='my-wallet-addr')

        ```
    - **Operations on orders with default values** `client.{operation}`
        - **`WARNING`** : 
            - when adding/updating an order, if `approved` field is set to `True`, then order is final
            and can no more be edited and will start to be eligible for matching against other
            orders.
            - Non `approved` orders will not be matched
        - **API**
            - `login(jwt='', addr='', ipaddr='', email='', username='')`
            - `add_buy_order(comment='', currency_to_buy='', price_max='0.0', amount=0.0, expiration=0, secret='', approved=False, currency_mine=[  ], buy_from=[  ])`
            - `update_sell_order(comment='', currency_to_sell='', price_min='0.0', amount=0.0, expiration=0, approved=False, id=0, currency_accept=[  ], sell_to=[  ], secret=[  ])`
            - `update_buy_order(self,comment='', currency_to_buy='', price_max='0.0', amount=0.0, expiration=0, secret='', approved=False, id=0, currency_mine=[  ], buy_from=[  ])`
            - `add_sell_order(comment='', currency_to_sell='', price_min='0.0', amount=0.0, expiration=0, approved=False, currency_accept=[  ], sell_to=[  ], secret=[  ])`
            - `get_buy_order(order_id=0)`
            - `get_sell_order(order_id=0)`
            - `list_all_buy_orders(sortby='id', desc=False)`
            - `list_all_sell_orders(sortby='id', desc=False)`
            - `list_my_buy_orders(sortby='id', desc=False)`
            - `list_my_sell_orders(sortby='id', desc=False)`
            - `remove_buy_order(order_id=0)`
            - `remove_sell_order(order_id=0)`
            - `list_all_transactions(state='*', desc=False) # * means all - change to 'pending', 'success', or 'failure' if you want`
            - `list_my_transactions(state='*', desc=False) # * means all - change to 'pending', 'success', or 'failure' if you want`       
        

####  General overview on code structure

- **Structure**

    ```
        server
            |
            |__ order_book.py # Exposed CMDs through server & client
            |__ system.py # system CMDs like ping
            
        lib # SAL layer
        
        schema.toml # General schemas
        schema_crud.toml # schemas for crud operations like create/update
    ```
- **Why do We have 2 schema files?**
    - `schema.toml` contains general schemas like `wallet`, `sellorder`, `buyorder`, and `transaction`
    - `schema_crud.toml` contains schemas used in `order_book.py` API which is meant for better code generation forexample:
        - `add_sell_order` we use `threefoldtoken.order.sell.create` from `schema_crud.toml` because it doesn't contain some fields in `threefoldtoken.order.sell` like email address of user
        - `update_sell_order` must contain `id` field that is why we use `threefoldtoken.order.sell.update` 
    - That says ussing multi schema files can be helpful if you want to customize code generation
    for client by hiding or adding certain fields

    - **`WARNING`**
        - Moving data between 2 similar but not identical schemas can be challenging
        that is why we use special technique for this. consider the following example
        ```python
          # obj of type : threefoldtoken.order.buy.create
          obj = j.data.schema.schema_from_url('threefoldtoken.order.buy.create').new()
          
          buy = j.data.schema.schema_from_url('threefoldtoken.order.buy').new()
          buy.copy(obj=obj)
        ```
 
- **Add data to db**
    ```python
      j.servers.gedis2.latest.db.tablesp['ordersell'].set(id=id, data=order.data)

        # You can add data to db also using
        # data = j.data.serializer.msgpack.dumps([id, order.data])
        # j.servers.gedis2.latest.models.threefoldtoken_order_sell.set(data)

    ```
