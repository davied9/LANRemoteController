

class LRCServerConfig(object):

    def __init__(self):
        self.config_file = None
        self.enable_ui = False
        self.command_ip = '127.0.0.1'
        self.command_port = 32781
        self.server_ip = '0.0.0.0'
        self.server_port = 35530
        self.waiter_ip = '0.0.0.0'
        self.waiter_port = 35527
        self.verify_code = None # for new client verification
        self.verbose = False

    @property
    def command_address(self):
        return (self.command_ip, self.command_port)

    @property
    def server_address(self):
        return (self.server_ip, self.server_port)

    @property
    def waiter_address(self):
        return (self.waiter_ip, self.waiter_port)

    def __str__(self):
        return '''
    config_file     : {},
    UI enabled      : {},
    command address : {},
    server address  : {},
    waiter address  : {},
    verify code     : {},
    verbose         : {},
'''.format(
            self.config_file,
            self.enable_ui,
            self.command_address,
            self.server_address,
            self.waiter_address,
            self.verify_code,
            self.verbose,
        )

