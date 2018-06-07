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

    client = j.clients.gedis2.configure(
        instance="example",
        host="localhost",
        port=9900,
        secret="",
        apps_dir=apps_dir,
        ssl=True,
        ssl_cert_file=""
    )