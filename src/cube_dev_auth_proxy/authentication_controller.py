import logging

import cube2crypto


logger = logging.getLogger(__name__)

class PendingChallenge(object):
    def __init__(self, reqid, auth_name, challenge, answer):
        self.reqid = reqid
        self.auth_name = auth_name
        self.challenge = challenge
        self.answer = answer

class AuthenticationController(object):
    def __init__(self, auth_data):
        self.auth_data = auth_data

        # {client_protocol: {reqid: PendingChallenge}}
        self.pending_challenges = {}

    def request(self, client_protocol, reqid, auth_name):
        pubkey = self.auth_data.get_pubkey(auth_name)
        challenge, answer = map(str, cube2crypto.generate_challenge(pubkey))

        if client_protocol not in self.pending_challenges:
            self.pending_challenges[client_protocol] = {}

        self.pending_challenges[client_protocol][reqid] = PendingChallenge(reqid, auth_name, challenge, answer)

        return challenge

    def confirm(self, client_protocol, reqid, answer):
        pending_challenge = self.pending_challenges[client_protocol].pop(reqid)
        logger.debug("comparing auth answer: {!r} {!r}".format(pending_challenge.answer, answer))
        assert(pending_challenge.answer == answer)
