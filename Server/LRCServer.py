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

class LRCServer ( TCPServer, object ):

    allow_reuse_address = True

    def __init__(self):
        TCPServer.__init__( self, server_address=('localhost', 33520), RequestHandlerClass=LRCDoorGuy )
        self.socket.setblocking(False)
        #self.socket.settimeout(5) # timeout is for blocking socket
        self.round = -1

        
class LRCWaiter(object): # waiter serve you all the time 

    def __init__(self, client_address ):
        self.client_address = client_address

        
class LRCDoorGuy( BaseRequestHandler, object ): # door guy welcome you to the table

    def __init__(self, request, client_address, server):
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
    
    server = LRCServer()
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
