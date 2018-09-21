from __future__ import print_function

class BaseCommand(object):

    def execute(self, **kwargs):
        pass

class Command(BaseCommand):

    def __init__(self, name, execute, kwargs=None, **_kwargs):
        self.name = name
        self._execute_handler = execute
        if not kwargs:
            self.kwargs = dict()
        else:
            self.kwargs = kwargs

    def __str__(self):
        return  '{} {} {}'.format(self.name, self._execute_handler, self.kwargs)

    def execute(self, **kwargs):
        kwargs.update(self.kwargs)
        self._execute_handler(**kwargs)


def parse_command(**kwargs):
    if 'import' not in kwargs or 'interface' not in kwargs:
        raise ValueError('"import" and "interface" should be specified for command')

    module = kwargs['import']
    interface = kwargs['interface']

    exec('import ' + module)
    return getattr(eval(module), interface)()


if '__main__' == __name__:
    command_config={'import':'LRC.Server.Commands.Start'}
    command = parse_command(**command_config)
    print(command)
    command.execute()
