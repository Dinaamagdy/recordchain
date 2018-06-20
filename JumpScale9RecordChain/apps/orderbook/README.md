## Orderbook

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
jwt = 'blah'
x.order_book.login(jwt, ipaddr='my-wallet-ip', addr='my-wallet-addr')
```

**Sell Orders**

```python
In [2]: x.order_book.add_sell_order(price_min='10 EUR')
@0xfa3e7566b269d6b5;

struct Schema {

    comment @0 :Text;
    currencyToSell @1 :Text;
    priceMin @2 :Data;
    expiration @3 :UInt32;

    currencyAccept @4 :List(Text);
    sellTo @5 :List(Text);
    secret @6 :List(Text);


}
Out[2]: 1

In [3]: x.order_book.get_sell_order(1)
@0xf5e73fb9827153b0;

struct Schema {

    orderId @0 :UInt32;



}
@0xfb48ef812ec7b22c;

struct Schema {

    comment @0 :Text;
    currencyToSell @1 :Text;
    priceMin @2 :Data;
    expiration @3 :UInt32;
    ownerEmailAddr @4 :Text;
    walletAddr @5 :Text;

    currencyAccept @6 :List(Text);
    sellTo @7 :List(Text);
    secret @8 :List(Text);


}
Out[3]: 
{
 "comment": "",
 "currency_accept": [],
 "currency_to_sell": "",
 "expiration": "1970/01/01 00:00:00",
 "owner_email_addr": "",
 "price_min": "1,381,319,968 EUR",
 "secret": [],
 "sell_to": [],
 "wallet_addr": ""
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



