from socket import *
import time
import re

class LRCClient(object):

    def __init__(self):
        self.is_working = False
        self.server_address = ('localhost', 33520)
        self.round = -1

    # interfaces
    def start(self):
        self.round += 1
        s = socket(AF_INET, SOCK_DGRAM)

        s.sendto(('hello from %d' % self.round).encode('utf-8'), self.server_address)
        msg, server_address = s.recvfrom(1024)
        print('got hello back :', msg)
        print('       address :', server_address)

        waiter_address = self.parse_address_from_message(msg)
        print('got waiter address :', waiter_address)

        s.sendto('a'.encode('utf-8'), waiter_address)
        s.sendto('d'.encode('utf-8'), waiter_address)

        pass

    def stop(self):
        pass

    def parse_address_from_message(self, message):
        """ parse_address_from_message

        :param message:
        :return address tuple parsed from message:
        """
        contents = message.decode('utf-8')
        # match ipv4 address
        ip = re.findall(r"'[\w\.]+'", contents)
        port = re.findall(r"\d+", contents)
        if len(ip) == 1 and ( len(port) == 1 or len(port) == 5):
            return (ip[0][1:-1], int(port[-1]))
        else:
            print('parse_address_from_message : can\'t parse address from message "%s"' % contents)


def __test000__():
    client = LRCClient()
    for round in range(10):
        client.round = round - 1
        client.start()
    
    pass


if '__main__' == __name__:
    __test000__()
    pass

