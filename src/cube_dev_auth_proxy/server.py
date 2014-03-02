import logging

from twisted.internet import reactor, defer

from cube_dev_auth_proxy.auth_proxy_client_protocol_factory import AuthProxyClientProtocolFactory
from cube_dev_auth_proxy.get_master_server_list import get_master_server_list
from resolve_domain_name_to_addresses import resolve_domain_name_to_addresses


logger = logging.getLogger(__name__)

class Server(object):
    """A protocol level proxy server which sits between the official master server and proxies the
    master server list but handles auth and server registration locally."""
    def __init__(self, auth_pubkeys):
        self.remote_master_server_list = ""
        self.auth_pubkeys = auth_pubkeys

    @defer.inlineCallbacks
    def run(self, master_server_domain, master_server_port):
        master_server_addresses = yield resolve_domain_name_to_addresses(master_server_domain)

        master_server_address = master_server_addresses[0]

        logger.info("Proxying master server: {!r} at {}:{}".format(master_server_domain, master_server_address, master_server_port))

        self._update_cached_server_list(master_server_address, master_server_port)

        self._setup_proxy()

    def _setup_proxy(self):
        self.proxy_client_protocol_factory = AuthProxyClientProtocolFactory(self, self.auth_pubkeys)
        self.listen = reactor.listenTCP(port=28787, factory=self.proxy_client_protocol_factory, backlog=5, interface='127.0.0.1')

    @defer.inlineCallbacks
    def _update_cached_server_list(self, address, port):
        reactor.callLater(60, self._update_cached_server_list, address, port)
        logger.debug("Attempting to get server list from: {}:{}".format(address, port))
        data = yield get_master_server_list(address, port)
        self.remote_master_server_list = '\n'.join(data)
