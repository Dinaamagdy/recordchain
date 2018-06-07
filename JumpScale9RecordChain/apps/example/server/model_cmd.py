import os

from js9 import j

apps_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

server = j.servers.gedis2.configure(
    instance="instance",
    port=5000,
    host="127.0.0.1",
    secret="",
    apps_dir=apps_dir
)

server.start()

client = j.clients.gedis2.configure(
    instance="instance",
    host="127.0.0.1",
    port=5000,
    secret="",
    apps_dir=apps_dir,
    ssl=True,
    ssl_cert_file=""
)