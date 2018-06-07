from js9 import j

p = j.tools.prefab.local
p.runtimes.pip.install("dnslib,nltk,nameparser,gevent,unidecode")

j.servers.zdb.test(build=True)
j.data.indexfile.test()
j.data.schema.test()

j.data.bcdb.test()
j.data.indexdb.test()

j.data.types.date.test()
j.data.types.numeric.test()


if p.platformtype.isLinux:

    j.servers.dns.test()


    def test(self, dobenchmarks=True,reset=False):
        """
        js9 'j.servers.gedis2.test(dobenchmarks=False)'

        will start in tmux the server & then connect to it using redisclient

        """

        if reset:
            j.sal.fs.remove("%s/codegen/"%j.dirs.VARDIR)
            bcdb=j.data.bcdb.get("test")  #has been set on start.py, will delete it here
            bcdb.destroy()
            j.tools.tmux.killall()

        classpath = j.sal.fs.getDirName(os.path.abspath(__file__)) +"EXAMPLE"

        self.configure(
            instance="test",
            port=5000,
            addr="127.0.0.1",
            secret="1234",
            ssl=True,
            namespace = "jumpscale.gedis2.example",
            path=classpath,
            interactive=False,
            background=True,
            start=True)

        r = self.client_get('test')

        ping1value = r.system.ping()
        assert ping1value == b'PONG'
        ping1value = r.system.ping_bool()
        assert ping1value == True

        #LOW LEVEL AT THIS TIME BUT TO SHOW SOMETHING
        cmds_meta =r.system.api_meta()

        cmds_meta = j.data.serializer.msgpack.loads(cmds_meta)
        for namespace,capnpbin in cmds_meta["cmds"].items():
            cmds_meta[namespace] = GedisCmds(namespace=namespace,capnpbin=capnpbin)

        # j.clients.gedis2.test()

        s= j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.in')
        o = s.new()
        o.name = "aname"
        o.nr = 1

        res = r.system.test("aname", 1)

        s=j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.out')

        o2=s.get(capnpbin=res.data)

        assert o.name == o2.name

        res = r.system.test_nontyped("name",10)
        assert j.data.serializer.json.loads(res) == ['name', 10]



    def test(self, dobenchmarks=True):
        """
        js9 'j.clients.gedis2.test()'
        """
        schema_path = j.sal.fs.getDirName(
            j.sal.fs.getDirName(
                j.sal.fs.getDirName(
                    os.path.abspath(__file__)
                )
            )) + "servers/gedis2/EXAMPLE"

        j.servers.gedis2.configure(
            instance="test",
            port=5000,
            namespace='jumpscale.gedis2.example',
            ssl=True,
            start=True,
            background=True,
            path=schema_path
        )

        cl = j.clients.gedis2.configure(
            instance="test",
            ipaddr="localhost",
            port=5000,
            password="",
            unixsocket="",
            ssl=True,
            ssl_cert_file=None
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

        s = j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.in')
        o = s.new()
        o.name = "aname"
        o.nr = 1

        res = cl.system.test("aname", 1)

        s = j.data.schema.schema_from_url('jumpscale.gedis2.example.system.test.out')

        o2 = s.get(capnpbin=res.data)

        assert o.name == o2.name
        assert cl.system.ping() == b'PONG'
        assert cl.system.ping_bool() == 1