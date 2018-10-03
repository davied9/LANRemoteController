

class LRCServerConfig(object):

    def __init__(self, **kwargs):
        self.config_file = None if 'config_file' not in kwargs else kwargs['config_file']
        self.enable_ui = False if 'enable_ui' not in kwargs else kwargs['enable_ui']

        self.command_ip = '127.0.0.1'
        self.command_port = 32781
        self._update_command_server_config(**kwargs)

        self.server_ip = '0.0.0.0'
        self.server_port = 35530
        self._update_server_config(**kwargs)

        self.waiter_ip = '0.0.0.0'
        self.waiter_port = 35527
        self._update_waiter_config(**kwargs)
        
        self.verify_code = None # for new client verification
        self.verbose = False

    def _update_command_server_config(self, **kwargs):
        if 'command_server_address' in kwargs:
            self.command_ip = kwargs['command_server_address'][0]
            self.command_port = kwargs['command_server_address'][1]
        if 'command_server_ip' in kwargs:
            self.command_ip = kwargs['command_server_ip']
        if 'command_server_port' in kwargs:
            self.command_port = kwargs['command_server_port']

    def _update_server_config(self, **kwargs):
        if 'server_address' in kwargs:
            self.server_ip = kwargs['server_address'][0]
            self.server_port = kwargs['server_address'][1]
        if 'server_ip' in kwargs:
            self.server_ip = kwargs['server_ip']
        if 'server_port' in kwargs:
            self.server_port = kwargs['server_port']

    def _update_waiter_config(self, **kwargs):
        if 'waiter_address' in kwargs:
            self.waiter_ip = kwargs['waiter_address'][0]
            self.waiter_port = kwargs['waiter_address'][1]
        if 'waiter_ip' in kwargs:
            self.waiter_ip = kwargs['waiter_ip']
        if 'waiter_port' in kwargs:
            self.waiter_port = kwargs['waiter_port']

    @property
    def command_server_address(self):
        return (self.command_ip, self.command_port)

    @property
    def server_address(self):
        return (self.server_ip, self.server_port)

    @property
    def waiter_address(self):
        return (self.waiter_ip, self.waiter_port)

    @property
    def command_server_config(self):
        return {
            'server_address' : self.command_server_address,
            'verbose'         : self.verbose,
        }

    @property
    def server_config(self):
        return {
            'server_address' : self.server_address,
            'waiter_address' : self.waiter_address,
            'verify_code'    : self.verify_code,
            'verbose'         : self.verbose,
        }

    @property
    def waiter_config(self):
        return {
            'server_address'  : self.server_address,
            'waiter_address'  : self.waiter_address,
            'verbose'         : self.verbose,
        }

    def __str__(self):
        return '''
    config_file             : {},
    UI enabled              : {},
    command server address  : {},
    server address          : {},
    waiter address          : {},
    verify code             : {},
    verbose                 : {},
'''.format(
            self.config_file,
            self.enable_ui,
            self.command_server_address,
            self.server_address,
            self.waiter_address,
            self.verify_code,
            self.verbose,
        )

