from Protocol import BaseServerProtocol


class ServerProtocol(BaseServerProtocol):

    necessary_attributes = []

    def __init__(self, request, client_address, server):
        BaseServerProtocol.__init__(self, request, client_address, server)

    def handle(self):

        pass

    def next(self):

        pass

    pass


class WaiterProtocol(BaseServerProtocol):

    necessary_attributes = []

    def __init__(self, request, client_address, server):
        BaseServerProtocol.__init__(self, request, client_address, server)


    pass


def ValidateServer(server_class):
    ServerProtocol.validate(server_class)
    WaiterProtocol.validate(server_class)