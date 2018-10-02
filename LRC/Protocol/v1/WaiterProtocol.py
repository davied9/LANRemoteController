from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol
from LRC.Controller.LRCController import Controller


class UnableToPackMessage(ValueError):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return 'Unable to pack message from {}'.format(self.kwargs)


class WaiterServerProtocol(V1BaseProtocol): # how do waiter unpack message, how to pack message sent to waiter
    '''
    waiter protocol defines how do waiter unpack message, how to pack message sent to waiter
    process several kinds of message:
        controller          -- receive a controller to execute keyboard combination locally

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        if 'controller' in kwargs:
            raw_message = self._pack_controller_message(**kwargs)
        else:
            raise UnableToPackMessage(kwargs)
        return self.encode(raw_message)

    def unpack_message(self, message):
        raw_message = self.decode(message)
        tag = self._unpack_tag(raw_message)
        args_message = raw_message[len(tag)+1:]
        if 'controller' == tag:
            kwargs=dict()
            kwargs['controller'] = Controller('waiter protocol', from_str=args_message)
        else:
            kwargs = self._unpack_args(args_message)
        return tag, kwargs

    # functional
    def _pack_controller_message(self, **kwargs):
        raw_message = 'controller='
        raw_message += str(kwargs['controller'])
        return raw_message

