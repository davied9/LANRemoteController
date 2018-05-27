from __future__ import print_function

from socket import *
from multiprocessing import Process
from threading import Thread

try: # python 2
    from SocketServer import UDPServer, BaseRequestHandler
except ImportError:  # python 3
    from socketserver import UDPServer, BaseRequestHandler
except:
    print('can not import packages for Server.')
finally:
    pass

from Protocol import v1

class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, server_address, waiter_address ):
        UDPServer.__init__( self, server_address, v1.ServerProtocol )
        # self.socket.setblocking(False)
        self.waiter_address = waiter_address

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, server_address ):
        UDPServer.__init__( self, server_address, v1.WaiterProtocol )

        
def test000_async_server():
    import time

    waiter_address = ('127.0.0.1',33555)
    server_address = ('127.0.0.1',33520)

    waiter = LRCWaiter(server_address=waiter_address)
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
    print('close server from outside', server._BaseServer__is_shut_down.is_set(), waiter._BaseServer__is_shut_down.is_set())
    print('serve thread  :', st)
    print('waiter thread  :', wt)
    pass


if '__main__' == __name__:
    test000_async_server()

    pass
