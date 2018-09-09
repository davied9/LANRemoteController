from LRC.Protocol.BaseCommunicationProtocol import BaseCommunicationProtocol

class CommunicationProtocol(BaseCommunicationProtocol):

    def __init__(self):
        BaseCommunicationProtocol.__init__(self)
        self.encoding = 'utf-8'

    def parse_message(self, message):
        # decode
        # get controller
        return

    def pack_message(self, *args):
        # pack controller
        # encode
        return

