from twisted.internet import defer, reactor

from cube_dev_auth_proxy.validate_server_online import validate_server_online


PING_TIME = 10
PING_RETRIES = 5

def sleep(sec):
    d = defer.Deferred()
    reactor.callLater(sec, d.callback, True)
    return d

@defer.inlineCallbacks
def monitor_server(client_protocol, host, port):
    failed_tries = 0
    while True:
        yield sleep(PING_TIME)
        try:
            yield validate_server_online(host, port)
            failed_tries = 0
        except:
            failed_tries += 1
            if failed_tries > PING_RETRIES:
                client_protocol.factory.remove_registered_server(client_protocol)
                client_protocol.transport.loseConnection()
                break
