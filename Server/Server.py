from socket import *
from socketserver import TCPServer
import threading

class LRCServer ( object ):
    def __init__(self):
        self.is_working = False
        self.serve_addr = ('localhost', 33520)
        self.serve_thread = None
        self.listener = None
        self.round = -1
    # interfaces
    def Start(self):
        self.serve_thread = threading.Thread(target=self.__respond_thread)
        self.is_working = True
        self.serve_thread.start()
        print('start serving on', self.serve_addr)
        pass
    def Stop(self):
        self.serve_thread._stop()
        pass
    # implementation
    def __respond_thread(self):

        self.listener = socket(AF_INET, SOCK_STREAM)
        self.listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.listener.bind(self.serve_addr)
        self.listener.listen(10)

        while True:
            self.round = self.round + 1
            hello_connection, client_addr = self.listener.accept()
            print('round ', self.round, 'accepted : ', hello_connection, ' - ', client_addr)
            print('from hello :', hello_connection.recv(1024).decode())
            hello_connection.close()
            

    def __serve_thread(self):


        pass

def test000():
    server = LRCServer()
    server.Start()
    pass


if '__main__' == __name__:
    test000()
    pass
