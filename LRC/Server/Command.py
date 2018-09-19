from __future__ import print_function

class Command(object):

    def __init__(self, name, execute, args=(), kwargs={},
                 *, delayed_expansion=False):
        self.name = name
        self._execute_handler = execute
        self.args = args
        self.kwargs = kwargs
        self.delayed_expansion = delayed_expansion


    def __str__(self):
        return  '{} {} {} {}'.format(self.name, self._execute_handler, self.args, self.kwargs)

    def execute(self, **kwargs):
        kwargs.update(self.kwargs)
        self._execute_handler(*self.args, **kwargs)

    @classmethod
    def parse_from_string(cls, string):
        return Command(name='default', execute=print, args=('default command called.'))
