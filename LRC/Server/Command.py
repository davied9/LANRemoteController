from __future__ import print_function

class Command(object):

    def __init__(self, name, execute=None, args=None, **kwargs):
        self.name = name
        self._execute_handler = execute
        self.args = args

    def execute(self):
        if self._execute_handler is not None:
            if self.args is not None:
                self._execute_handler(*self.args)
            else:
                self._execute_handler()

    def execute_external(self, *args):
        if self._execute_handler is not None:
            self._execute_handler(*args)

    @classmethod
    def parse_from_string(cls, string):
        return Command(name='default', execute=print, args=('default command called.'))
