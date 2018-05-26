
class BaseProtocol:

    def __init__(self):
        pass

    # before using protocol, make sure this server/client is available for protocol
    @classmethod
    def validate(self, server_or_client):
        # mostly 'if !hasattr(server_or_client)' is writen here
        return True

    # next step as expected
    def next(self):
        pass

