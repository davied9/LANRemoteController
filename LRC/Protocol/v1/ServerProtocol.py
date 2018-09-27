from LRC.Protocol.BaseProtocol import BaseProtocol


class ServerProtocol(BaseProtocol): # how do server unpack message, how to pack message sent to server

    def __init__(self, **kwargs):
        BaseProtocol.__init__(self, **kwargs)

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack message from given information
        :param kwargs:      information from application
        :return message:    message to send
        '''
        return self.encode('')

    def unpack_message(self, message):
        '''
        unpack message into application information
        :param message:     message to parse from
        :return *args:      information unpacked
        '''
        return ''

    # functional


