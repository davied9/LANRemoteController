
try: # python 2
    from SocketServer import BaseRequestHandler
except ImportError:  # python 3
    from socketserver import BaseRequestHandler
except:
    print('can not import package for BaseRequestHandler.')
finally:
    pass

from BaseProtocol import BaseProtocol


class BaseServerProtocol( BaseRequestHandler, BaseProtocol ):

    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)
        BaseProtocol.__init__(self)


