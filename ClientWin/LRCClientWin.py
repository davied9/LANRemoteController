from socket import *
import time


class LRCClient(object):
    def __init__(self):
        self.is_working = False
        self.serve_addr = ('localhost', 33520)
        self.round = -1
    # interfaces
    def Start(self):
        self.round += 1

        s = socket(AF_INET, SOCK_STREAM)

        hello_connection = s.connect(self.serve_addr)
        # if 1 == self.round%2:
            # time.sleep(1)
        s.send(('hello from %d' % self.round).encode('utf-8'))
        s.close()

        pass
    def Stop(self):
        pass

def __test000__():
    client = LRCClient()
    for round in range(10):
        client.round = round - 1
        client.Start()
    
    pass


if '__main__' == __name__:
    __test000__()
    pass

