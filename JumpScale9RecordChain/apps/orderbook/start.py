import os

from js9 import j

apps_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

server = j.servers.gedis2.configure(
    instance="orderbook",
    port=9900,
    host="localhost",
    secret="",
    apps_dir=apps_dir
)

server.start()

client = j.clients.gedis2.configure(
    instance="orderbook",
    host="localhost",
    port=9900,
    secret="",
    apps_dir=apps_dir,
    ssl=True,
    ssl_cert_file=""
)