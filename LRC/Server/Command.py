from __future__ import print_function

class Command(object):

    def __init__(self, name, execute=None, args=None, **kwargs):
        self.name = name
        self.execute_handler = execute
        self.args = args

    def execute(self, args):
        if self.execute_handler is not None:
            if self.args is not None:
                self.execute_handler(self.args)
            else:
                self.execute_handler()


