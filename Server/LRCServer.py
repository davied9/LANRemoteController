from __future__ import print_function

from socket import *
import threading

try: # python 2
    from SocketServer import TCPServer, BaseRequestHandler
except ImportError:  # python 3
    from socketserver import TCPServer, BaseRequestHandler
except:
    print('can not import packages for Server.')
finally:
    pass

from Protocol import v1

class LRCServer ( TCPServer, object ):

    allow_reuse_address = True

    def __init__(self, server_address ):
        TCPServer.__init__( self, server_address=server_address, RequestHandlerClass=LRCDoorGuy )
        self.socket.setblocking(False)
        self.round = -1

class LRCWaiter( TCPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, server_address ):
        TCPServer.__init__( self, server_address=server_address, RequestHandlerClass=LRCDoorGuy )


class LRCDoorGuy( BaseRequestHandler, object ): # door guy welcome you to the table

    def __init__(self, request, client_address, server):
        self.table = 0 # the table number of guest, if 0, then guest can not stay
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.server.round += 1
        print('round ', self.server.round, 'accepted : ', self.request, ' from ', self.client_address)
        try:
            print('from hello :', self.request.recv(1024))
        except Exception as err:
            print('network blocked, message not got')
        finally:
            self.server.close_request(self.request)
        
def test000_async_server():
    import time

    if hasattr(LRCServer, 'handle_request'):
        print('LRCServer has operator handle_request')

    server = LRCServer(server_address=('localhost',33520))
    st = threading.Thread(target=server.serve_forever)
    print('serve thread created :', st)
    st.start()
    print('start server at', server.server_address)

    time.sleep(5)
    server.shutdown()
    print('close server from outside')
    pass


if '__main__' == __name__:
    test000_async_server()

    pass
