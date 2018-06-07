import os

from js9 import j

apps_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    server = j.servers.gedis2.configure(
        instance="{{instance}}",
        port={{config.port}},
        host="{{config.host}}",
        secret="{{config.secret_}}",
        apps_dir=apps_dir
    )

    server.start()

    client = j.clients.gedis2.configure(
        instance="{{instance}}",
        host="{{config.host}}",
        port={{config.port}},
        secret="{{config.secret_}}",
        apps_dir=apps_dir,
        ssl=True,
        ssl_cert_file=""
    )
