import os

from js9 import j

apps_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    server = j.servers.gedis2.configure(
        instance="example",
        port=9900,
        host="localhost",
        secret="",
        apps_dir=apps_dir
    )

    server.start()

    cl = j.clients.gedis2.configure(
        instance="example",
        host="localhost",
        port=9900,
        secret="",
        apps_dir=apps_dir,
        ssl=True,
        ssl_cert_file=""
    )


    o=cl.models.test_gedis2_cmd1.new()
    o.cmd.name="aname"
    o.cmd2.name="aname2"
    o2=cl.models.test_gedis2_cmd1.set(o)
    o3=cl.models.test_gedis2_cmd1.set(o2) #make sure id stays same, id should be 1 & stay 1

    assert o2.id==o3.id

    o4=cl.models.test_gedis2_cmd1.get(o3.id)

    assert o3.ddict==o4.ddict

    res = cl.system.test_nontyped("name", 10)
    assert j.data.serializer.json.loads(res) == ['name', 10]

    s = j.data.schema.schema_from_url('example.system.test.in')
    o = s.new()
    o.name = "aname"
    o.nr = 1

    res = cl.system.test("aname", 1)

    s = j.data.schema.schema_from_url('example.system.test.out')

    o2 = s.get(capnpbin=res.data)

    assert o.name == o2.name
    assert cl.system.ping() == b'PONG'
    assert cl.system.ping_bool() == 1

    print('\n\n***************')
    print('    OK')
    print('***************\n\n')