from socket import *
from socketserver import TCPServer, StreamRequestHandler
import threading



class LRCServer ( TCPServer ):

    allow_reuse_address = True

    def __init__(self, *argv, async=False):
        super(LRCServer, self).__init__(
            server_address=('localhost', 33520),
            RequestHandlerClass=LRCRequestHandlerClass
            )
        self.round = -1
        print('start LRCServer on', self.server_address)
        if async:
            self.serve_thread = threading.Thread(target=self.serve_forever)
            self.serve_thread.start()
        else:
            self.serve_thread = None
            self.serve_forever()


class LRCRequestHandlerClass(StreamRequestHandler):

    def __init__(self, *argv, **kwargs):
        super(LRCRequestHandlerClass, self).__init__(*argv, **kwargs)

    def handle(self):
        self.server.round += 1
        print('round ', self.server.round, 'accepted : ', self.request, ' from ', self.client_address)
        print('from hello :', self.request.recv(1024))


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
