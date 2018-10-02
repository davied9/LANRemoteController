from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol


class ServerProtocol(V1BaseProtocol): # how do server unpack message, how to pack message sent to server
    '''
    server protocol defines how do server unpack message, how to pack message sent to server
    process several kinds of message :
        connection request          -- ask for permission for connection to waiter

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        # raw message format : request=name,arg0,arg1,arg2,...
        raw_message = 'request='
        raw_message += 'name=' + kwargs['request'] + ','
        del kwargs['request']
        for k, v in kwargs.items():
            raw_message += k + '=' + v + ','
        return self.encode(raw_message)

    # functional


