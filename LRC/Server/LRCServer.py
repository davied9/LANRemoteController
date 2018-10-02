from __future__ import print_function
from LRC.Controller.LRCController import Controller
from LRC.Common.logger import logger
from multiprocessing import Process, Manager

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


def _empty(*args, **kwargs): pass # a black hole


class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        if 'verbose' in kwargs and kwargs['verbose'] is True:
            from functools import partial
            self._verbose_info = partial(print, 'LRC server [verbose] :')
        else:
            self._verbose_info = _empty
        super(LRCServer, self).__init__(kwargs["server_address"], None )
        self.waiter_address     = kwargs["waiter_address"]
        self.message_encoding   = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.verify_code        = kwargs["verify_code"] if "verify_code" in kwargs else None
        self.client_list        = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox        = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning
        self._verbose_info('server {}, waiter {}'.format( self.server_address, self.waiter_address))

    # interfaces
    def finish_request(self, request, client_address):
        self._verbose_info('receive request {} from {}'.format(request, client_address))
        self.sendto( str(self.waiter_address) , client_address )
        if self.client_list is not None and client_address not in self.client_list:
            self.client_list.append(client_address)
            self.info('Server: add client {0} to client list.'.format(client_address))

    # functional
    def encode_message(self, message):
        return message.encode(self.message_encoding)

    def sendto(self, message, client_address):
        self.socket.sendto(self.encode_message(message), client_address)


class KeyCombinationParseError(Exception):
    pass

from pykeyboard import PyKeyboard
import re

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        if 'verbose' in kwargs and kwargs['verbose'] is True:
            from functools import partial
            self._verbose_info = partial(print, 'LRC waiter [verbose] :')
        else:
            self._verbose_info = _empty
        super(LRCWaiter, self).__init__(kwargs["waiter_address"], None )
        self.message_encoding       = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.connect_server_address = kwargs["server_address"]
        self.client_list            = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox            = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning
        self.keyboard = PyKeyboard()
        self.key_matcher = re.compile(r'[a-zA-Z ]+')
        self.key_settings = Controller.settings
        self.execute_delay = 0
        self._verbose_info('server {}, waiter {}'.format( self.connect_server_address, self.server_address))

    # interfaces
    def finish_request(self, request, client_address):
        self._verbose_info('receive request {} from {}'.format(request, client_address))
        if self.client_list is not None and client_address not in self.client_list:
            self.warning('Waiter: unknown client request : {0}'.format(client_address))
            return
        message = self.decode_message(request[0])
        key_combination = self.parse_key_combination_message(message)
        try:
            if self.execute_delay > 0:
                from threading import Timer
                Timer( self.execute_delay, self.keyboard.press_keys, args=(key_combination,)).start()
                self.info('Waiter: schedule pressing keys in {2} seconds from {0} : {1}'.format(client_address, key_combination, self.execute_delay))
            else:
                self.keyboard.press_keys(key_combination)
                self.info('Waiter: pressing keys from {0} : {1}'.format(client_address, key_combination))
        except Exception as err:
            self.info('Waiter: can\'t press key from {0} {1} : {2}'.format(client_address, key_combination, err.args))

    # functional
    def decode_message(self, message):
        return message.decode(self.message_encoding)

    def parse_key_combination_str(self, key_str_list):
        # to lower
        str_list_to_check = []
        for key_str in key_str_list:
            str_list_to_check.append(key_str.lower())
        # identify functional keys
        checked_combination = []
        for f_key in self.key_settings.ctrl_keys:
            if f_key in str_list_to_check:
                checked_combination.append( self.key_settings.key_map[ f_key ] )
                str_list_to_check.remove(f_key)
        for f_key in self.key_settings.shift_keys:
            if f_key in str_list_to_check:
                checked_combination.append( self.key_settings.key_map[ f_key ] )
                str_list_to_check.remove(f_key)
        for f_key in self.key_settings.alt_keys:
            if f_key in str_list_to_check:
                checked_combination.append( self.key_settings.key_map[ f_key ] )
                str_list_to_check.remove(f_key)
        # special keys
        for s_key in self.key_settings.allowed_special_keys:
            if s_key in str_list_to_check:
                checked_combination.append( self.key_settings.key_map[ s_key ] )
                str_list_to_check.remove(s_key)
        # identify normal keys
        for key in str_list_to_check:
            if len(key) == 1:
                checked_combination.append( key )
            else:
                raise KeyCombinationParseError()
        return checked_combination

    def parse_key_combination_message(self, key_combination_message):
        key_combination = self.key_matcher.findall(key_combination_message)
        try:
            key_combination = self.parse_key_combination_str(key_combination)
        except KeyCombinationParseError:
            key_combination = None
            self.info('Waiter: parse key combination failed from message : {0}'.format(key_combination_message) )
        except Exception as err:
            key_combination = None
        return key_combination


def start_server(**kwargs):
    '''
    start LRC server with given parameters
    :param kwargs:
        required :
            server_address      -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address      -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding    -- 'utf-8'(default)
            verify_code         -- None
            client_list         -- None
            log_mailbox         -- None
    :return:
    '''
    LRCServer(**kwargs).serve_forever()


def start_waiter(**kwargs):
    '''
    start LRC waiter with given parameters
    :param kwargs:
        required :
            connect_server_address  -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address          -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding        -- 'utf-8'(default)
            verify_code             -- None
            client_list             -- None
            log_mailbox             -- None
    :return:
    '''
    LRCWaiter(**kwargs).serve_forever()


class LRCServerManager(object):

    def __init__(self):
        try:
            self.communication_manager = Manager()
            self.client_list = self.communication_manager.list()
            self.log_mailbox = self.communication_manager.Queue()
            self.mode = 'full'
        except Exception as err:
            logger.error('LRC : Manager start failed, only basic function started')
            self.communication_manager = None
            self.client_list = None
            self.log_mailbox = None
            self.mode = 'basic'

        self._server_process = None
        self.server_config = dict()

        self._waiter_process = None
        self.waiter_config = dict()

    # commands interfaces
    def start_server(self, **kwargs):
        kwargs = self._update_server_config(kwargs)
        self._start_server(**kwargs)

    def stop_server(self):
        if self._server_process:
            if self._server_process.is_alive():
                logger.info('LRC : stop server')
                self._server_process.terminate()
            self._server_process = None

    def start_waiter(self, **kwargs):
        kwargs = self._update_waiter_config(kwargs)
        self._start_waiter(**kwargs)

    def stop_waiter(self):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                logger.info('LRC : stop waiter')
                self._waiter_process.terminate()
            self._waiter_process = None

    def quit(self):
        self.stop_server()
        self.stop_waiter()

    # functional
    def _update_server_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox
        return config

    def _start_server(self, **kwargs):
        if self._server_process:
            if self._server_process.is_alive():
                if kwargs == self.server_config:
                    logger.info('LRC : server already running')
                    return
                else:
                    logger.info('LRC : terminate server process for restart')
                    self._server_process.terminate()
            self._server_process = None
        try:
            self._server_process = Process(target=start_server, kwargs=kwargs)
            self._server_process.start()
            self.server_config = kwargs
            logger.info('LRC : start server process at {}'.format(kwargs['server_address']))
        except Exception as err:
            logger.error('LRC : start server process failed : {}'.format(err.args))

    def _update_waiter_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox
        return config

    def _start_waiter(self, **kwargs):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                if kwargs == self.waiter_config:
                    logger.info('LRC : waiter already running')
                    return
                else:
                    logger.info('LRC : terminate waiter process for restart')
                    self._waiter_process.terminate()
            self._waiter_process = None
        try:
            self._waiter_process = Process(target=start_waiter, kwargs=kwargs)
            self._waiter_process.start()
            self.waiter_config = kwargs
            logger.info('LRC : start waiter process at {}'.format(kwargs['waiter_address']))
        except Exception as err:
            logger.error('LRC : start waiter process failed : {}'.format(err.args))



if '__main__' == __name__:

    def test000_async_server():
        import time
        from multiprocessing import Process
        from threading import Thread

        waiter_address = ('127.0.0.1',35527)
        server_address = ('127.0.0.1',35530)

        waiter = LRCWaiter(waiter_address=waiter_address, connect_server_address=server_address)
        server = LRCServer(server_address=server_address, waiter_address=waiter_address)

        st = Thread(target=server.serve_forever)
        print('serve thread created :', st)
        st.start()
        print('start server at', server.server_address)

        wt = Thread(target=waiter.serve_forever)
        print('waiter thread created :', wt)
        wt.start()
        print('start wait at', waiter.server_address)


        time.sleep(15)
        server.shutdown()
        waiter.shutdown()
        print('force to close servers ')
        print('server :', st, '-- closed :', server._BaseServer__is_shut_down.is_set())
        print('waiter :', wt, '-- closed :', waiter._BaseServer__is_shut_down.is_set())
        pass

    test000_async_server()

    pass
