from __future__ import print_function
    
from socket import *
import threading

try:
    from SocketServer import TCPServer, StreamRequestHandler
except ImportError:
    from socketserver import TCPServer, StreamRequestHandler
except:
    print('can not import TCPServer, StreamRequestHandler.')
finally:
    pass


class LRCServer ( TCPServer, object ):

    allow_reuse_address = True

    def __init__(self, async=True):
        super(LRCServer, self).__init__(
            server_address=('localhost', 33520),
            RequestHandlerClass=LRCRequestHandlerClass
            )
        self.round = -1
        print('start LRCServer on', self.server_address)
        if async:
            threading.Thread(target=self.serve_forever).start()
        else:
            self.serve_forever()




class LRCRequestHandlerClass( StreamRequestHandler, object ):

    def __init__(self, request, client_address, server):
        super(LRCRequestHandlerClass, self).__init__(request, client_address, server)

    def handle(self):
        self.server.round += 1
        print('round ', self.server.round, 'accepted : ', self.request, ' from ', self.client_address)
        print('from hello :', self.request.recv(1024))
        self.request.close()


class Waiter(object):

    def __init__(self, client_address ):
        self.client_address = client_address


def test000():
    import time
    server = LRCServer(async=True)
    time.sleep(10)
    server.shutdown()
    print('close server from outside')
    pass


if '__main__' == __name__:
    test000()

    pass
