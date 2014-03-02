from twisted.internet import reactor, defer
from twisted.internet.protocol import connectionDone, ClientFactory
from twisted.protocols.basic import LineReceiver


class MasterServerListQueryProtocol(LineReceiver):

    delimiter = '\n'

    def __init__(self, connection_done_deferred):
        self.results_ready_deferred = connection_done_deferred
        self.results = []

    def connectionMade(self):
        LineReceiver.connectionMade(self)
        self.sendLine("list")

    def lineReceived(self, line):
        self.results.append(line)

    def connectionLost(self, reason=connectionDone):
        self.results_ready_deferred.callback(self.results)
        LineReceiver.connectionLost(self, reason=reason)

class MasterServerListQueryProtocolFactory(ClientFactory):
    def __init__(self, results_ready_deferred):
        self.results_ready_deferred = results_ready_deferred

    def buildProtocol(self, addr):
        return MasterServerListQueryProtocol(self.results_ready_deferred)

def get_master_server_list(address, port):
    results_ready_deferred = defer.Deferred()

    reactor.connectTCP(address, port, MasterServerListQueryProtocolFactory(results_ready_deferred))

    return results_ready_deferred
