from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol


class ClientProtocol(V1BaseProtocol): # how do client unpack message, how to pack message sent to client
    '''
    client protocol defines how do client unpack message, how to pack message sent to client
    process several kinds of message :
        connection request respond          -- contains info about success or not, and how to connect to waiter

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack message from given information
        :param kwargs:      information from application
        :return message:    message to send
        '''
        raw_message = 'respond='
        raw_message += 'content=' + kwargs['respond'] + ','
        for k, v in kwargs.items():
            raw_message += k + '=' + v + ','
        return self.encode(raw_message)
