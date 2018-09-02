from Common.logger import logger
from socket import *
import re

class LRCClient(object):

    def __init__(self, message_encoding='utf-8'):
        self.server_address = None
        self.waiter_address = None
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.message_encoding = message_encoding

    # interfaces
    def connect(self, server_address):
        self.server_address = server_address
        self.socket.sendto(self.encode_message('hello'), server_address)
        msg, server_address = self.socket.recvfrom(1024)
        self.waiter_address = self.parse_address_from_message(msg)
        logger.info('Client: parse waiter address from : {0} with waiter address : {1}'.format(msg, self.waiter_address))

    def send_message(self, message):
        self.socket.sendto(self.encode_message(message), self.waiter_address)

    def send_combinations(self, *args):
        self.send_message(self.make_message_from_key_combinations(*args))

    def make_message_from_key_combinations(self, *args):
        msg = []
        if len(args):
            msg.append(args[0])
            for key in args[1:]:
                msg.append('+')
                msg.append(key)
        return ''.join(msg)

    def parse_address_from_message(self, message):
        """ parse_address_from_message

        :param message:
        :return address tuple parsed from message:
        """
        contents = message.decode('utf-8')
        # match ipv4 address
        ip = re.findall(r"'[\w\.]+'", contents)
        port = re.findall(r"\d+", contents)
        if len(ip) == 1 and ( len(port) == 1 or len(port) == 5 ):
            return (ip[0][1:-1], int(port[-1]))
        else:
            logger.info('Client: parse_address_from_message : can\'t parse address from message "%s"' % contents)

    def encode_message(self, message):
        return message.encode(self.message_encoding)

def __test000__():
    import time

    server_address = ('127.0.0.1',35530)
    client = LRCClient()
    client.connect(server_address)

    time.sleep(5)
    print('start tap keys now')

    client.send_combinations('j')
    client.send_combinations(' ')
    client.send_combinations('o', 'shift')
    client.send_combinations(' ')
    client.send_combinations('k', 'shift')
    client.send_combinations(' ')
    client.send_combinations('e', 'r')

    pass


if '__main__' == __name__:
    __test000__()
    pass

