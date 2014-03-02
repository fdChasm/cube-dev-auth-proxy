import logging

from twisted.internet.protocol import Factory

from cube_dev_auth_proxy.auth_proxy_client_protocol import AuthProxyClientProtocol
from cube_dev_auth_proxy.authentication_controller import AuthenticationController
from cube_dev_auth_proxy.server_list_model import ServerListModel


logger = logging.getLogger(__name__)

class AuthProxyClientProtocolFactory(Factory):

    protocol = AuthProxyClientProtocol

    def __init__(self, server, auth_data, gban_list):
        self.server = server
        self.local_master_server_list = ServerListModel()
        self.authentication_controller = AuthenticationController(auth_data)
        self.gban_list = gban_list

    def get_registered_server_list(self):
        return self.server.remote_master_server_list + self.local_master_server_list.to_response_string()

    def add_registered_server(self, client_protocol, host, port):
        self.local_master_server_list.add(client_protocol, host, port)

    def get_gban_list(self):
        return self.gban_list.to_response_string()

    def remove_registered_server(self, client_protocol):
        self.local_master_server_list.remove(client_protocol)

    def request_auth(self, client_protocol, reqid, auth_name):
        return self.authentication_controller.request(client_protocol, reqid, auth_name)

    def confirm_auth(self, client_protocol, reqid, answer):
        return self.authentication_controller.confirm(client_protocol, reqid, answer)
