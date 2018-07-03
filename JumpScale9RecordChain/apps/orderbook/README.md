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
    - **Add/Update orders**
    - Set `approved` field to `True` if you want your order to be final and eligible for matching
    - **`Warning`** : `approved` order can no more be editable
    - add:
       - for buy orders:
        ```python
        client.order_book.add_buy_order(price_max='10 ETH', currency_to_buy='BTC', currency_mine=['USD'], amount=100, expiration=j.data.time.epoch + 1000, approved=True, secret="1")
        ```
        - for sell orders you use: `client.order_book.add_sell_order`
    - In update, you can provide `id` field for order, you want to deal with
    

**Important**

schema files orders is important
if you make 2 similar schemas (one of which have more fields than the other)
you need to maintain same order of fileds across both of them
in order to be able to convert from one of them to the other

**copy objets**
```python
new = j.data.schema.schema_from_url('threefoldtoken.order.sell').get(capnpbin=old_obj.data)
```


**Add data to db**

j.servers.gedis2.latest.db.tablesp['ordersell'].set(id=id, data=order.data)

        # You can add data to db also using
        # data = j.data.serializer.msgpack.dumps([id, order.data])
        # j.servers.gedis2.latest.models.threefoldtoken_order_sell.set(data)




