from LRC.Protocol.BaseProtocol import BaseProtocol


class WaiterServerProtocol(BaseProtocol): # how do waiter unpack message, how to pack message sent to waiter

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


