class AuthData(object):
    def __init__(self, data):
        self.data = data

    def get_pubkey(self, auth_name):
        return self.data[auth_name]
