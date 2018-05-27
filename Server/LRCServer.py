from __future__ import print_function

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer
except:
    print('can not import packages for UDPServer.')
finally:
    pass

from ServerRequestHandler import ServerRequestHandler, WaiterRequestHandler


class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, server_address, waiter_address ):
        UDPServer.__init__( self, server_address, ServerRequestHandler )
        # self.socket.setblocking(False)
        self.waiter_address = waiter_address

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, server_address ):
        UDPServer.__init__( self, server_address, WaiterRequestHandler )

        
def test000_async_server():
    import time
    from multiprocessing import Process
    from threading import Thread

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
    print('force to close server ')
    print('serve thread  :', st, '-- closed :', server._BaseServer__is_shut_down.is_set())
    print('waiter thread  :', wt, '-- closed :', waiter._BaseServer__is_shut_down.is_set())
    pass


if '__main__' == __name__:
    test000_async_server()

    pass
