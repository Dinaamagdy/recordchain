import os

from js9 import j

apps_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    server = j.servers.gedis2.configure(
        instance="orderbook",
        port=9900,
        host="localhost",
        secret="",
        apps_dir=apps_dir
    )

    server.start()

    cl = j.clients.gedis2.configure(
        instance="orderbook",
        host="localhost",
        port=9900,
        secret="",
        apps_dir=apps_dir,
        ssl=True,
        ssl_cert_file=""
    )

    res = cl.system.test_nontyped("name", 10)
    assert j.data.serializer.json.loads(res) == ['name', 10]

    s = j.data.schema.schema_from_url('orderbook.system.test.in')
    o = s.new()
    o.name = "aname"
    o.nr = 1

    res = cl.system.test("aname", 1)

    s = j.data.schema.schema_from_url('orderbook.system.test.out')

    o2 = s.get(capnpbin=res.data)

    assert o.name == o2.name
    assert cl.system.ping() == b'PONG'
    assert cl.system.ping_bool() == 1

    print('\n\n***************')
    print('    OK')
    print('***************\n\n')