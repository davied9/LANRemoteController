from __future__ import print_function
from LRC.Server.Config import LRCServerConfig
from LRC.Server.Command import Command, parse_command
from LRC.Common.logger import logger
from LRC.Protocol.v1.CommandServerProtocol import CommandServerProtocol
from multiprocessing import Manager
from threading import Thread
import json

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


class CommandServer(UDPServer):

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
        self.__commands = dict()
        self._init_commands()
        # initialize communication components
        self.comm_manager = None
        self.log_mailbox = None
        self.client_list = None

    def finish_request(self, request, client_address):
        self._verbose_info('CommandServer : got request {} from client {}'.format(request, client_address))
        try:
            # parse command from request
            tag, args = self.protocol.unpack_message(request[0])
            self._verbose_info('CommandServer : unpack result : {}, {}'.format(tag, args))
            # execute command
            if 'command' == tag:
                self._execute_command(args['name'])
            elif 'request' == tag:
                self._respond_request(client_address, request=args['name'], **args)
            elif 'running_test' == tag:
                self._respond_running_test(client_address)
        except Exception as err:
            logger.error('CommandServer : failed to process request {} from {}'.format(request, client_address))

    def start(self):
        '''
        start lrc command server
        :return:
        '''
        try:
            # start command server
            self.server_bind()
            self.server_activate()
            Thread(target=self.serve_forever).start()
            # start process communication server
            self.comm_manager = Manager()
            self.log_mailbox = self.comm_manager.Queue()
            self.client_list = self.comm_manager.list()
            # log
            logger.info('CommandServer : start command server at {}'.format(self.server_address))
        except:
            self.server_close()
            raise

    def quit(self, *args, **kwargs):
        def shutdown_tunnel(server):
            server.shutdown()
            server.comm_manager.shutdown()
        # shutdown must be called in another thread, or it will be blocked forever
        Thread(target=shutdown_tunnel, args=(self,)).start()

    def register_command(self, key, command):
        logger.info('CommandServer : add command {} {}'.format(key, command))
        self.__commands[key] = command

    def send_command(self, command):
        self._verbose_info('CommandServer : send command {} to {}'.format(command, self.server_address))
        self.socket.sendto(self.protocol.pack_message(command=command), self.server_address)

    def load_commands_from_file(self, command_file):
        logger.info('CommandServer : add command from file {}'.format(command_file))
        try:
            with open(command_file, 'r') as fp:
                config_string = fp.read()
            config_dict = json.loads(config_string)
        except Exception as err:
            logger.error('CommandServer : add command from file {} failed with {}'.format(command_file, err.args))
            return
        success=0
        fail=0
        for command_name, command_body in config_dict.items():
            try:
                command = parse_command(**command_body)
                self.register_command(command_name, command)
                success += 1
            except Exception as err:
                logger.error('CommandServer : load command {} failed with {}'.format(command_name, err.args))
                fail += 1
        logger.info('CommandServer : add command from file {} done, total {}, success {}, fail {}'.format(
                command_file, success+fail, success, fail))

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
            soc.sendto(self.protocol.pack_message(running_test=None, state='request'), self.server_address)
            respond, _ = soc.recvfrom(1024)
            tag, args = self.protocol.unpack_message(respond)
            if 'running_test' == tag and 'confirm' == args['state']:
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

    @property
    def commands(self):
        return self.__commands

    # functional
    def _init_commands(self):
        self.register_command('quit', Command(name='quit', execute=self.quit))
        self.register_command('list_commands', Command(name='list_commands', execute=self._list_commands))
        self.load_commands_from_file('LRC/Server/commands.json')

    def _execute_command(self, command, **kwargs):
        if command not in self.commands.keys():
            logger.error('CommandServer : command {} not registered'.format(command))
            return
        try:
            logger.info('CommandServer : executing command {}'.format(command))
            self.commands[command].execute(**kwargs)
        except Exception as err:
            logger.error('ComandServer : failed executing command {} with error {}'.format(command, err.args))

    def _respond_request(self, client_address, request, **kwargs):
        self.socket.sendto(self.protocol.pack_message(respond=request+' confirm'), client_address)

    def _respond_running_test(self, client_address):
        self.socket.sendto(self.protocol.pack_message(running_test=None, state='confirm'), client_address)

    # command entry
    def _list_commands(self,  *args, **kwargs):
        message = 'CommandServer : list commands : \n'
        for v in self.commands.values():
            message += '\t{}\n'.format(v)
        logger.info(message)

    def _verbose_info(self, message):
        self._verbose_info_handler('CommandServer : verbose : {}'.format(message))

    @classmethod
    def __empty(*args): pass


if '__main__' == __name__:

    def __test_case_001():
        # start a Command Server
        s = CommandServer(port=35777, verbose=True)
        s.register_command('test_comm', Command(name='test_comm', execute=logger.info, args=('test_comm called',)))
        s.start()
        # try commands
        s.send_command(command='test_comm')
        s.send_command(command='quit')
        return

    __test_case_001()