from LRC.Protocol.BaseProtocol import BaseProtocol
import re

class V1BaseProtocol(BaseProtocol):
    '''
    V1BaseProtocol defines common protocol for v1 of LRC protocol
    '''

    _tag_exp = re.compile(r'^(\w+)\=')
    _arg_exp = re.compile(r'([\w\.\-]+)\=([\w\.\-]+)')

    def __init__(self, **kwargs):
        super(V1BaseProtocol, self).__init__(**kwargs)

    # interface
    def unpack_message(self, message):
        '''
        unpack message into command or controller
        :param message:     message received
        :return command:    command parsed from message
        '''
        raw_message = self.decode(message)
        tag = self._unpack_tag(raw_message)
        args_message = raw_message[len(tag)+1:]
        kwargs = self._unpack_args(args_message)
        return tag, kwargs

    # functional
    def _unpack_tag(self, message):
        try:
            tag = self._tag_exp.findall(message)[0]
            return tag
        except:
            return ''

    def _unpack_args(self, message):
        args=dict()
        for pair in self._arg_exp.findall(message):
            args[pair[0]] = pair[1]
        return args