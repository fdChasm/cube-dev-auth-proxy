import logging

from twisted.internet import reactor

from cube_dev_auth_proxy.auth_data import AuthData
from cube_dev_auth_proxy.server import Server
from cube_dev_auth_proxy.gban_list import GBanList


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = Server(
        AuthData({'user': '+c4357a14af0c19e3a9fa900cdf9cc5116feeee412376ea7e'}),
        GBanList(['127.0.0.1']))
    server.run("sauerbraten.org", 28787)
    reactor.run()
