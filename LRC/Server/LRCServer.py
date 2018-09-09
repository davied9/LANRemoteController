from __future__ import print_function
from functools import partial
from LRC.Controller.LRCController import Controller
from LRC.Common.logger import logger

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer
except:
    print('can not import packages for UDPServer.')



def start_LRCServer(server_address, waiter_address, verify_code, client_list, log_mailbox=None):
    LRCServer(server_address=server_address,
              waiter_address=waiter_address,
              verify_code=verify_code,
              client_list=client_list,
              log_mailbox=log_mailbox).serve_forever()


def start_LRCWaiter(waiter_address, server_address, client_list, log_mailbox=None):
    LRCWaiter(waiter_address=waiter_address,
              connect_server_address=server_address,
              client_list=client_list,
              log_mailbox=log_mailbox).serve_forever()


class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        UDPServer.__init__( self, kwargs["server_address"], None )
        self.waiter_address     = kwargs["waiter_address"]
        self.message_encoding   = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.verify_code        = kwargs["verify_code"] if "verify_code" in kwargs else None
        self.client_list        = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox        = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning

    def encode_message(self, message):
        return message.encode(self.message_encoding)

    def sendto(self, message, client_address):
        self.socket.sendto(self.encode_message(message), client_address)

    def finish_request(self, request, client_address):
        self.sendto( str(self.waiter_address) , client_address )
        if self.client_list is not None and client_address not in self.client_list:
            self.client_list.append(client_address)
            self.info('Server: add client {0} to client list.'.format(client_address))


class KeyCombinationParseError(Exception):
    pass

from pykeyboard import PyKeyboard
import re

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        UDPServer.__init__( self, kwargs["waiter_address"], None )
        self.message_encoding       = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.connect_server_address = kwargs["connect_server_address"]
        self.client_list            = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox            = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning
        self.keyboard = PyKeyboard()
        self.key_matcher = re.compile(r'[a-zA-Z ]+')
        self.key_settings = Controller.settings
        self.execute_delay = 3

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

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
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
