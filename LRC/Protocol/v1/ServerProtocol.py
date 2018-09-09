from LRC.Protocol import BaseServerProtocol


class ServerProtocol(BaseServerProtocol):

    necessary_attributes = []

    def __init__(self, request, client_address, server):
        BaseServerProtocol.__init__(self, request, client_address, server)

    def handle(self): # given clent the waiter address
        print('SeverProtocol : handling request from', self.client_address)
        print('      message :', self.request[0])
        self.server.socket.sendto( str(self.server.waiter_address).encode('utf-8'), self.client_address )


class WaiterProtocol(BaseServerProtocol):

    necessary_attributes = []

    def __init__(self, request, client_address, server):
        BaseServerProtocol.__init__(self, request, client_address, server)

    def handle(self): # respond to short_cut_key
        print('WaiterProtocol : handling request from', self.client_address)
        print('      message :', self.request[0])
        pass

