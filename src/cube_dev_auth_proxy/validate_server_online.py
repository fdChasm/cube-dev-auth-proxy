from twisted.internet import defer, reactor
from twisted.internet.protocol import DatagramProtocol
from cube2protocol.cube_data_stream import CubeDataStream


class LanInfoClientDatagramProtocol(DatagramProtocol):
    def __init__(self, host, port, response_received_deferred):
        self.host = host
        self.port = port
        self.response_received_deferred = response_received_deferred

    def startProtocol(self):
        self.transport.connect(self.host, self.port)

        cds = CubeDataStream()
        cds.putint(1)

        self.transport.write(str(cds))

    def datagramReceived(self, datagram, host):
        if not self.response_received_deferred.called:
            self.response_received_deferred.callback(True)

def validate_server_online(host, port, timeout=5):
    deferred = defer.Deferred()

    protocol = LanInfoClientDatagramProtocol(host, port, deferred)
    transport = reactor.listenUDP(0, protocol)

    def on_timeout():
        transport.stopListening()
        if not deferred.called:
            defer.timeout(deferred)

    reactor.callLater(timeout, on_timeout)

    return deferred

if __name__ == "__main__":
    deferred = validate_server_online('127.0.0.1', 28786)

    def callback(result):
        print "callback", result

    def errback(error):
        print "error", error

    deferred.addCallbacks(callback, errback)

    reactor.run()
