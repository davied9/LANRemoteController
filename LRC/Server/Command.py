from __future__ import print_function

class BaseCommand(object):

    def execute(self, **_kwargs):
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
        return  '<{} :: {} :: {}>'.format(self.name, self._execute_handler, self.kwargs)

    def execute(self, **kwargs):
        kwargs.update(self.kwargs)
        self._execute_handler(**kwargs)


def _get_simple_interface(interface, module):
    if interface.startswith(module):
        return interface[len(module):]
    else:
        return interface


def parse_command(**_kwargs):
    '''
    parse one command from settings
    :param **kwargs:    setting for command
    :return command:    command parsed from settings
    available settings :
        import      -- the module will import
        kwargs      -- parameters for command execution
        execute     -- attribute of module, used as execute handler for common command (LRC.Server.Command.Command)
        command     -- command class
    '''
    if 'import' in _kwargs:
        module = _kwargs['import']
        exec('import ' + module)
        del _kwargs['import']
    else:
        module = ''

    if 'kwargs' in _kwargs:
        kwargs = eval(_kwargs['kwargs'])
        del _kwargs['kwargs']
    else:
        kwargs = dict()

    if 'interface' in _kwargs: # interface to get command instance
        interface = _get_simple_interface(_kwargs['interface'], module)
        del _kwargs['interface']
        return getattr(eval(module), interface)(kwargs=kwargs, **_kwargs)

    if 'command' in _kwargs: # command class
        command_class = _get_simple_interface(_kwargs['command'], module)
        del _kwargs['command']
        return getattr(eval(module), command_class)(kwargs=kwargs, **_kwargs)

    if 'execute_interface' in _kwargs: # interface to get execute handler for a common command (LRC.Server.Command.Command)
        execute_interface = _get_simple_interface(_kwargs['execute_interface'], module)
        del _kwargs['execute_interface']
        return Command(name="parsed from string", execute=getattr(eval(module), execute_interface)(), kwargs=kwargs, **_kwargs)

    if 'execute' in _kwargs: # execute handler for a common command (LRC.Server.Command.Command)
        execute = _get_simple_interface(_kwargs['execute'], module)
        del _kwargs['execute']
        return Command(name="parsed from string", execute=getattr(eval(module), execute), kwargs=kwargs, **_kwargs)

    raise ValueError('parse_command : one of the following should be specified : {}'.format(
            {'interface','command','execute_interface','execute'}))


if '__main__' == __name__:
    command_config={'import':'LRC.Server.Commands.Start'}
    command = parse_command(**command_config)
    print(command)
    command.execute()
