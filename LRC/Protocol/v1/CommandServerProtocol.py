from LRC.Protocol.BaseProtocol import BaseProtocol


class CommandServerProtocol(BaseProtocol):

    def __init__(self, **kwargs):
        BaseProtocol.__init__(self, **kwargs)

    # interfaces
    def pack_message(self, respond):
        '''
        pack message from answer
        :param respond:     request respond
        :return message:    encoded message to send
        '''
        return self.encode(respond)

    def unpack_message(self, message):
        '''
        unpack message into command or controller
        :param message:     message received
        :return command:    command parsed from message
        '''
        return self.decode('')

    # functional


