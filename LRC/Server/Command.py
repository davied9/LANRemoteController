from __future__ import print_function

class Command(object):

    def __init__(self, name, execute=None, args=None, **kwargs):
        self.name = name
        self._execute_handler = execute
        self.args = args
        self.delayed_expansion = False if 'delayed_expansion' not in kwargs else kwargs['delayed_expansion']

    def __str__(self):
        return  '{} {} {}'.format(self.name, self._execute_handler, self.args)

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
