## Orderbook

For better understanding of how order book you MUST be familiar with
- [Schemas](JumpScale9RecordChain/data/schema/README.md)
- [BCDB database](JumpScale9RecordChain/data/bcdb/README.md)
- [GEDIS2](JumpScale9RecordChain/servers/gedis2/README.md)

**Specs**

- [HERE](JumpScale9RecordChain/apps/orderbook/specs.md)


**Start Server**
```python
s = j.servers.gedis2.get('orderbook')
s.start()
```

**Get client**
```python
x = j.clients.gedis2.get('orderbook')
```

**Login/Register client wallet**

```python
iyo_client = j.clients.itsyouonline.get()
jwt = iyo_client.jwt
x.order_book.login(jwt, ipaddr='my-wallet-ip', addr='my-wallet-addr')
```

**Sell Orders**

```python
In [2]: x.order_book.add_buy_order(price_max='10 ETH', currency_to_buy='BTC', currency_mine=['USD'], amount=100, expiration=j.data.time.epoch + 1000, approved=True, secret="1")

Out[2]: 1

In [3]: x.order_book.get_buy_order(1)
@0xf5e73fb9827153b0;

struct Schema {

    orderId @0 :UInt32;



}
@0xf6c6005cada3994d;

struct Schema {

    comment @0 :Text;
    currencyToBuy @1 :Text;
    priceMax @2 :Data;
    amount @3 :Float64;
    expiration @4 :UInt32;
    secret @5 :Text;
    approved @6 :Bool;
    ownerEmailAddr @7 :Text;
    walletAddr @8 :Text;

    currencyMine @9 :List(Text);
    buyFrom @10 :List(Text);


}
Out[3]: 
{
 "amount": 100.0,
 "approved": true,
 "buy_from": [],
 "comment": "",
 "currency_mine": [
  "USD"
 ],
 "currency_to_buy": "BTC",
 "expiration": "2018/06/28 09:00:00",
 "owner_email_addr": "ayouba@greenitglobe.com",
 "price_max": "10.0 ETH",
 "secret": "1",
 "wallet_addr": "addr"
}

In [4]: x.order_book.list_sell_orders(sortby='price_min')
@0xf20a81180788ff89;

struct Schema {

    sortby @0 :Text;
    desc @1 :Bool;



}
Out[4]: b'[\n{\n"comment": "",\n"currency_to_sell": "",\n"price_min": "1,381,319,968 EUR",\n"expiration": "1970/01/01 00:00:00",\n"currency_accept": [],\n"sell_to": [],\n"secret": []\n}\n]'

In [5]: x.order_book.remove_sell_order(1)
@0xf5e73fb9827153b0;

struct Schema {

    orderId @0 :UInt32;



}
Out[5]: 1

In [6]: x.order_book.list_sell_orders(sortby='price_min')
Out[6]: b'[]'

```

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




