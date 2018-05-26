
class BaseProtocol:

    """Base class for protocol

     Methods for the caller:

    - __init__()
    - validate() -> is_available

    Methods that may be overridden:

    - next()
        next move for request, main part of protocol

    Methods for derived classes:

    - next()

    Class variables that may be overridden by derived classes or
    instances:

    - necessary_attributes

    Instance variables:

    -

    """

    necessary_attributes = []

    def __init__(self):
        pass

    @classmethod
    def validate(cls, server_or_client_class):
        """validate server or client class is available for this protocol

        before using protocol, make sure this server/client is available for protocol

        :param server_or_client_class:
        :return is_available:
        """
        # mostly 'if !hasattr(server_or_client_class)' is writen here
        avail = True
        for attr in cls.necessary_attributes:
            if not hasattr(server_or_client_class, attr):
                avail = False
                print(server_or_client_class.__name__, 'do not have necessary attribute', attr, 'for protocol', cls.__name__)
        return avail

    def next(self):
        """next step as expected
        :return:
        """
        pass

