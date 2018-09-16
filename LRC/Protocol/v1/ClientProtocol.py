from LRC.Protocol.BaseProtocol import BaseProtocol

class ClientProtocol(BaseProtocol):

    def __init__(self, **kwargs):
        BaseProtocol.__init__(self, **kwargs)

    def pack_message(self, *args, **kwargs):
        '''
        pack message from given information
        :param args:        information from application
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