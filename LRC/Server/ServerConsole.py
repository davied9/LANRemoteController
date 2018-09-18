from __future__ import print_function
from LRC.Server.Config import LRCServerConfig
from LRC.Server.Command import Command
from LRC.Server.LRCServer import start_LRCWaiter, start_LRCServer
from LRC.Common.logger import logger
from LRC.Protocol.v1.CommandServerProtocol import CommandServerProtocol
from multiprocessing import Process, Manager
from threading import Thread

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


class CommandServer(UDPServer):

    commands = {
        'quit'              :   Command(name='quit', execute=None, args=None),
    }

    # interfaces
    def __init__(self, **kwargs):
        # initial configuration
        self.verbose = True if 'verbose' in kwargs else False
        # initialize command server
        self.server_address = kwargs["server_address"] if 'server_address' in kwargs else ('127.0.0.1', 35589)
        if 'port' in kwargs:
            self.port = kwargs["port"]
        if 'ip' in kwargs:
            self.ip = kwargs["ip"]
        UDPServer.__init__(self, server_address=self.server_address, RequestHandlerClass=None, bind_and_activate=False)
        # initialize protocol
        self.protocol = CommandServerProtocol()
        # initialize commands
        self._init_commands()
        # initialize communication components
        self.comm_manager = None
        self.log_mailbox = None
        self.client_list = None

    def finish_request(self, request, client_address):
        self._verbose_info('CommandServer : got request {} from client {}'.format(request, client_address))
        # parse command from request
        tag, args = self.protocol.unpack_message(request[0])
        self._verbose_info('CommandServer : unpack result : {}, {}'.format(tag, args))
        # execute command
        if 'command' == tag:
            self._execute_command(args['name'])
        elif 'request' == tag:
            self._respond_request(client_address, args['name'], **args)

    def start(self):
        '''
        start lrc command server
        :return:
        '''
        try:
            self.server_bind()
            self.server_activate()
            self.comm_manager = Manager()
            self.log_mailbox = self.comm_manager.Queue()
            self.client_list = self.comm_manager.list()
        except:
            self.server_close()
            raise
        logger.info('CommandServer : start command server at {}'.format(self.server_address))
        Thread(target=self.serve_forever).start()

    def quit(self):
        def shutdown_tunnel(server):
            server.shutdown()
            server.comm_manager.shutdown()
        # shutdown must be called in another thread, or it will be blocked forever
        Thread(target=shutdown_tunnel, args=(self,)).start()

    def send_command(self, command):
        self._verbose_info('CommandServer : send command {} to {}'.format(command, self.server_address))
        self.socket.sendto(self.protocol.pack_message(command=command), self.server_address)

    # properties
    @property
    def ip(self):
        return self.server_address[0]

    @ip.setter
    def ip(self, val):
        self.server_address = (val, self.server_address[1])

    @property
    def port(self):
        return self.server_address[1]

    @port.setter
    def port(self, val):
        self.server_address = (self.server_address[0], val)

    @property
    def is_running(self):
        try:
            from socket import socket, AF_INET, SOCK_DGRAM
            soc = socket(family=AF_INET, type=SOCK_DGRAM)
            soc.settimeout(0.5)
            soc.sendto(self.protocol.pack_message(command='running_test'), self.server_address)
            respond, server = soc.recvfrom(1024)
            tag, _ = self.protocol.unpack_message(respond)
            if 'running_test' == tag:
                return True
        except Exception as err:
            self._verbose_info('CommandServer : running_test : {}'.format(err.args))
        return False

    @property
    def verbose(self):
        return self.__empty == self._verbose_info_handler

    @verbose.setter
    def verbose(self, val):
        if val:
            self._verbose_info_handler = logger.info
        else:
            self._verbose_info_handler = self.__empty


    # functional
    def _init_commands(self):
        self.commands['quit']._execute_handler = self.quit

    def _execute_command(self, command, *args):
        if command not in self.commands.keys():
            logger.error('CommandServer : command {} not registered'.format(command))
            return
        try:
            self._verbose_info('ComandServer : executing command {}'.format(command))
            if len(args) == 0:
                self.commands[command].execute()
            else:
                self.commands[command].execute_external(*args)
        except Exception as err:
            logger.error('ComandServer : failed executing command {} with {}'.format(command, err.args))

    def _respond_request(self, client_address, request, **kwargs):
        if 'running_test' == request:
            self.socket.sendto(self.protocol.pack_message(respond='running_test'), client_address)

    def _verbose_info(self, message):
        self._verbose_info_handler('CommandServer : verbose : {}'.format(message))

    @classmethod
    def __empty(*args): pass

def start_lrc_server_console():
    import sys
    config = LRCServerConfig()
    # start a new command server if necessary
    command_server = CommandServer(port=35777, verbose=True)
    if not command_server.is_running:
        command_server.start()
    # send the command
    for i in range(1,len(sys.argv)):
        command_server.send_command(sys.argv[i])

if '__main__' == __name__:

    def __test_case_000():
        start_lrc_server_console()
        return

    def __test_case_001():
        # start a Command Server
        CommandServer.commands['test_comm'] = Command(name='test_comm', execute=logger.info, args=('test_comm called',))
        s = CommandServer(port=35777, verbose=True)
        t = Thread(target=s.serve_forever)
        t.start()
        # connect
        from socket import socket, AF_INET, SOCK_DGRAM
        soc = socket(family=AF_INET, type=SOCK_DGRAM)
        soc.connect(s.server_address)
        p = CommandServerProtocol()
        # try command test_comm
        soc.send(p.pack_message(command='test_comm'))
        # try command quit
        soc.send(p.pack_message(command='quit'))
        return

    __test_case_001()