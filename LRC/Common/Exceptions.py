
__all__ = ['ArgumentError', 'NotFoundError']

class ArgumentError(Exception):

    def __str__(self):
        msg = 'Argument(s) not available : '
        for arg in self.args:
            msg += ' {},'.format(arg)
        return msg[:-1]


class NotFoundError(Exception):

    def __str__(self):
        msg = 'Not found :'
        for arg in self.args:
            msg += ' {},'.format(arg)
        return msg[:-1]
