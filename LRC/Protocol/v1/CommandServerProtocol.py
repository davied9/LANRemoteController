from LRC.Common.logger import logger
from LRC.Protocol.BaseProtocol import BaseProtocol
import re


class CommandServerProtocol(BaseProtocol):

    __tag_exp = re.compile(r'(\w+)\=')
    __arg_exp = re.compile(r'([\w\.\-]+)\=([\w\.\-]+)')

    def __init__(self, **kwargs):
        BaseProtocol.__init__(self, **kwargs)

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack message from answer
        :param respond:     request respond
        :return message:    encoded message to send
        '''
        if 'request' in kwargs:
            raw_message = self._pack_message('request',**kwargs)
        elif 'command' in kwargs:
            raw_message = self._pack_message('command',**kwargs)
        elif 'respond' in kwargs:
            raw_message = self._pack_message('respond',**kwargs)
        else:
            logger.info('unknown operation "{}" for LRC command server'.format(kwargs))
            raw_message = ''
        return self.encode(raw_message)

    def unpack_message(self, message):
        '''
        unpack message into command or controller
        :param message:     message received
        :return command:    command parsed from message
        '''
        raw_message = self.decode(message)
        tag = self._unpack_tag(raw_message)
        args = self._unpack_args(raw_message[len(tag)+1:])
        return tag, args
        # logger.info('LRC command server cannot parse operation from message "{}"'.format(raw_message))

    # functional
    def _unpack_tag(self, message):
        try:
            tag = self.__tag_exp.match(message).group()[:-1]
            return tag
        except:
            return ''

    def _unpack_args(self, message):
        args=dict()
        for pair in self.__arg_exp.findall(message):
            args[pair[0]] = pair[1]
        return args

    def _pack_message(self, tag, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        # raw message format : request=name,arg0,arg1,arg2,...
        raw_message = tag + '='
        raw_message += 'name=' + kwargs[tag] + ','
        del kwargs[tag]
        for k, v in kwargs:
            raw_message += k + '=' + v + ','
        return raw_message

