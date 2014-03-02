def format_addserver(address):
    return "addserver {} {}\n".format(*address)

class ServerListModel(object):
    def __init__(self):
        self.servers = {}

    def add(self, client_protocol, host, port):
        self.servers[client_protocol] = (host, port)

    def remove(self, client_protocol):
        del self.servers[client_protocol]

    def to_response_string(self):
        return "".join(map(format_addserver, self.servers.values()))
