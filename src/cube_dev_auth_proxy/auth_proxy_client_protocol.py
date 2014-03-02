import logging
import sys
import traceback

from twisted.internet import defer
from twisted.protocols.basic import LineReceiver

from cube_dev_auth_proxy.monitor_server import monitor_server
from cube_dev_auth_proxy.registry_manager import RegistryManager, register
from cube_dev_auth_proxy.validate_server_online import validate_server_online


logger = logging.getLogger(__name__)

class AuthProxyClientProtocol(LineReceiver):

    delimiter = '\n'

    def __init__(self):
        self._host = "unknown"
        self.command_handlers = {}
        for registration in RegistryManager.get_registrations('auth_command'):
            command = registration.args[0]
            handler = registration.registered_object
            self.command_handlers[command] = handler

    @property
    def host(self):
        return self._host

    def connectionMade(self):
        self._host = self.transport.getHost().host
        logger.debug("{} connected".format(self.host))
        LineReceiver.connectionMade(self)

    def lineReceived(self, line):
        logger.debug("{} request: {!r}".format(self.host, line))
        try:
            args = line.split(' ')

            command = args[0]
            handler = self.command_handlers[command]
            handler(self, args)
        except:
            traceback.print_exc()
            self.transport.loseConnection()

    def sendLine(self, line):
        logger.debug("{} sending: {!r}".format(self.host, line))
        return LineReceiver.sendLine(self, line)

@register('auth_command', 'list')
def list_handler(client_protocol, args):
    remote_master_server_list = client_protocol.factory.get_registered_server_list()

    if len(remote_master_server_list):
        client_protocol.sendLine(remote_master_server_list)

    client_protocol.transport.loseConnection()

@register('auth_command', 'regserv')
@defer.inlineCallbacks
def regserv_handler(client_protocol, args):
    try:
        host = client_protocol.transport.getHost().host
        port = int(args[1])

        yield validate_server_online(host, port + 1)
        client_protocol.factory.add_registered_server(client_protocol, host, port)
        client_protocol.sendLine('succreg')

        client_protocol.sendLine(client_protocol.factory.get_gban_list())

        monitor_server(client_protocol, host, port + 1)
    except:
        sys.stderr.write("Failure in registering server.\n")
        logger.debug(traceback.format_exc())
        client_protocol.sendLine('failreg')
        client_protocol.transport.loseConnection()

@register('auth_command', 'reqauth')
def reqauth_handler(client_protocol, args):
    reqid = args[1]
    auth_name = args[2]

    try:
        challenge = client_protocol.factory.request_auth(client_protocol, reqid, auth_name)
        client_protocol.sendLine('chalauth {} {}'.format(reqid, challenge))
    except:
        logger.debug(traceback.format_exc())
        client_protocol.sendLine('failauth {}'.format(reqid))

@register('auth_command', 'confauth')
def confauth_handler(client_protocol, args):
    reqid = args[1]
    answer = args[2]

    try:
        client_protocol.factory.confirm_auth(client_protocol, reqid, answer)
        client_protocol.sendLine('succauth {}'.format(reqid))
    except:
        logger.debug(traceback.format_exc())
        client_protocol.sendLine('failauth {}'.format(reqid))
