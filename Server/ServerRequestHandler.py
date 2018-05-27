
try: # python 2
    from SocketServer import UDPServer, BaseRequestHandler
except ImportError:  # python 3
    from socketserver import UDPServer, BaseRequestHandler
except:
    print('can not import packages for Server.')
finally:
    pass


class ServerRequestHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self): # given clent the waiter address
        print('SeverProtocol : handling request from', self.client_address)
        print('      message :', self.request[0])
        self.server.sendto( str(self.server.waiter_address) , self.client_address )



class WaiterRequestHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self): # respond to short_cut_key
        print('WaiterProtocol : handling request from', self.client_address)
        print('      message :', self.request[0])
        pass

