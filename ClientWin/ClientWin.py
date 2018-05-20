from socket import *


class LRCClient(object):
    def __init__(self):
        self.is_working = False
        self.serve_addr = ('localhost', 33520)
        self.round = 0
    # interfaces
    def Start(self):

        s = socket(AF_INET, SOCK_STREAM)

        hello_connection = s.connct(self.serve_addr)
        s.connected


        pass
    def Stop(self):
        pass

def test000():
    client = LRCClient()
    client.Start()
    pass


if '__main__' == __name__:
    test000()
    pass

