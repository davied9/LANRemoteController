

class LRCServerConfig(object):

    def __init__(self):
        self.enable_ui = True
        self.server_ip = '0.0.0.0'
        self.server_port = 35530
        self.waiter_ip = '0.0.0.0'
        self.waiter_port = 35527
        self.verify_code = None # for new client verification

    @property
    def server_address(self):
        return (self.server_ip, self.server_port)

    @property
    def waiter_address(self):
        return (self.waiter_ip, self.waiter_port)

    def __str__(self):
        return '''
    server_address = {},
    waiter_address = {},
    verify_code    = {},
'''.format(
                self.server_address,
                self.waiter_address,
                self.verify_code
        )

