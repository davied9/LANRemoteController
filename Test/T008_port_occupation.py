from __future__ import print_function
from socket import *


if '__main__' == __name__ :
    # conclusion :
    #   all sockets must set REUSE to make port reuse available

    combinations = [
        ['o','o'],
        ['o','x'],
        ['x','o'],
        ['x','x'],
    ]

    print('situations (o means REUSE flag is set)')
    print('(1) (2)  result')
    address = ('127.0.0.1', 31557)

    for i in range(4):
        comb = combinations[i]

        a = socket(family=AF_INET, type=SOCK_DGRAM)
        if comb[0] == 'o':
            a.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # (1)
        a.bind(address)

        result = None
        try:
            b = socket(family=AF_INET, type=SOCK_DGRAM)
            if comb[1] == 'o':
                b.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # (2)
            b.bind(address)
        except Exception as err:
            result = err.args
        finally:
            a.shutdown(SHUT_RDWR)
            b.shutdown(SHUT_RDWR)
            del a, b

        result = 'normal' if result is None else result
        print(' {}   {}   {}'.format(comb[0], comb[1], result))

