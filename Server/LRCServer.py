from __future__ import print_function

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer
except:
    print('can not import packages for UDPServer.')
finally:
    pass


class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, server_address, waiter_address, verify_code, message_encoding='utf-8' ):
        UDPServer.__init__( self, server_address, None )
        self.waiter_address = waiter_address
        self.message_encoding = message_encoding
        self.verify_code = verify_code

    def encode_message(self, message):
        return message.encode(self.message_encoding)

    def sendto(self, message, client_address):
        self.socket.sendto(self.encode_message(message), client_address)

    def finish_request(self, request, client_address):
        self.sendto( str(self.waiter_address) , client_address )

class KeyCombinationParseError(Exception):
    pass

from PyUserInput import PyKeyboard
import re

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, waiter_address, connect_server_address, message_encoding='utf-8' ):
        UDPServer.__init__( self, waiter_address, None )
        self.message_encoding = message_encoding
        self.connect_server_address = connect_server_address
        self.keyboard = PyKeyboard()
        self.key_matcher = re.compile(r'[a-zA-Z]+')
        self.__make_functional_key_dict()

    def __make_functional_key_dict(self):
        self._allowed_functional_key = ({
            'control':self.keyboard.control_l_key,
            'alt':self.keyboard.alt_l_key,
            'shift':self.keyboard.shift_l_key
        })

    def decode_message(self, message):
        return message.decode(self.message_encoding)

    def validate_key_combination(self, key_combination):
        # to lower
        for ix_key in range(len(key_combination)):
            key_combination[ix_key] = key_combination[ix_key].lower()
        # identify functional keys
        checked_combination = []
        for f_key in self._allowed_functional_key.keys():
            if f_key in key_combination:
                real_key = self._allowed_functional_key[ f_key ]
                checked_combination.append( real_key )
        # identify normal keys
        for key in key_combination:
            if len(key) == 1:
                checked_combination.append( key )
            else:
                if key not in self._allowed_functional_key.keys():
                    raise KeyCombinationParseError
        return checked_combination

    def parse_key_combination_message(self, key_combination_message):
        key_combination = self.key_matcher.findall(key_combination_message)
        try:
            key_combination = self.validate_key_combination(key_combination)
        except KeyCombinationParseError:
            key_combination = None
            print('LRCWaiter : parse key combination failed from message :', key_combination_message)
        except Exception as err:
            key_combination = None
        finally:
            pass
        return key_combination

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        message = self.decode_message(request[0])
        key_combination = self.parse_key_combination_message(message)
        try:
            self.keyboard.press_keys(key_combination)
            print('pressing keys from ', client_address, ' :', key_combination)
        except Exception as err:
            print('can\'t press key from ', client_address, key_combination, ':', err.args)
        finally:
            pass


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


if '__main__' == __name__:
    test000_async_server()

    pass
