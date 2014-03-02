class GBanList(object):
    def __init__(self, gban_data):
        self.gban_data = gban_data

    def to_response_string(self):
        response = ['cleargbans']
        response.extend(map(lambda b: "addgban {}".format(b), self.gban_data))
        return '\n'.join(response)
