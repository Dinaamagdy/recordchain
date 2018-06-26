## Create an app

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
