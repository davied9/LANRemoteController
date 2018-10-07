from __future__ import print_function
from LRC.Server.Config import LRCServerConfig
from LRC.Server.Command import Command, parse_command
from LRC.Common.logger import logger
from LRC.Common.empty import empty
from LRC.Protocol.v1.CommandServerProtocol import CommandServerProtocol
from multiprocessing import Manager
from threading import Thread
import os, json

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


class CommandServer(UDPServer):

    # interfaces
    def __init__(self, **kwargs):
        # initial configuration
        self.verbose = kwargs["verbose"] if 'verbose' in kwargs else False
        # initialize command server
        server_address = kwargs["server_address"] if 'server_address' in kwargs else ('127.0.0.1', 35589)
        if 'port' in kwargs:
            server_address = (server_address[0], kwargs["port"])
        if 'ip' in kwargs:
            server_address = (kwargs["ip"], server_address[1])
        super(CommandServer, self).__init__(server_address=server_address, RequestHandlerClass=None, bind_and_activate=False)
        # initialize protocol
        self.protocol = CommandServerProtocol()
        # initialize commands
        self.__commands = dict()
        self._init_basic_commands()
        self.__is_main_server = False
        # initialize role
        self.role = 'not started' # 'not started' 'main' 'secondary'

    def finish_request(self, request, client_address):
        self._verbose_info('CommandServer : got request {} from client {}'.format(request, client_address))
        try:
            # parse command from request
            tag, kwargs = self.protocol.unpack_message(request[0])
            self._verbose_info('CommandServer : unpack result : {}, {}'.format(tag, kwargs))
            # execute command
            if 'command' == tag:
                command = kwargs['name']
                del kwargs['name']
                self._execute_command(command, **kwargs)
            elif 'request' == tag:
                self._respond_request(client_address, request=kwargs['name'], **kwargs)
            elif 'running_test' == tag:
                self._respond_running_test(client_address, **kwargs)
        except Exception as err:
            logger.error('CommandServer : failed to process request {} from {}'.format(request, client_address))

    def start(self, start_as_main=True):
        '''
        start lrc command server
        :return:
        '''
        if not start_as_main:
            raise NotImplemented('start command server as secondary is not implemented yet')
        self.is_main_server = start_as_main
        try:
            # start command server
            self.server_bind()
            self.server_activate()
            Thread(target=self.serve_forever).start()
            # log
            role = 'main' if self.is_main_server else 'secondary'
            logger.info('CommandServer : start command server at {} as {}'.format(self.server_address, role))
            self.role = role
        except:
            self.server_close()
            raise

    def quit(self, *args, **kwargs):
        def shutdown_tunnel(server):
            server.shutdown()
        # shutdown must be called in another thread, or it will be blocked forever
        Thread(target=shutdown_tunnel, args=(self,)).start()
        self.role = 'not started'

    def dump_config(self):
        d = dict()
        d.update(self._dump_local_config())
        d.update(self._dump_remote_config())
        return d

    def apply_config(self, **kwargs):
        self._apply_local_config(**kwargs)
        self._apply_remote_config(**kwargs)

    def sync_config(self): # sync this instance's config to the running command server with same address(ip,port)
        self.send_command('sync_config', **self._dump_remote_config())

    def register_command(self, key, command):
        logger.info('CommandServer : add command {} {}'.format(key, command))
        self.commands[key] = command

    def send_command(self, command, **kwargs):
        self._verbose_info('CommandServer : send command {}({}) to {}'.format(command, kwargs, self.command_server_address))
        self.socket.sendto(self.protocol.pack_message(command=command, **kwargs), self.command_server_address)

    def load_commands(self, **command_config):
        logger.info('CommandServer : load commands from config :\n    {}'.format(command_config))
        success, fail = self._load_commands_from_file(**command_config)
        logger.info('CommandServer : load commands from config done, total {}, success {}, fail {}'.format(
                success+fail, success, fail))

    def load_commands_from_string(self, command_config_string):
        logger.info('CommandServer : load commands from config string :\n    {}'.format(command_config_string))
        success, fail = self._load_commands_from_string(command_config_string)
        logger.info('CommandServer : load commands from config string done, total {}, success {}, fail {}'.format(
                success+fail, success, fail))

    def load_commands_from_file(self, command_file):
        logger.info('CommandServer : load commands from config file :\n    {}'.format(command_file))
        success, fail = self._load_commands_from_file(command_file)
        logger.info('CommandServer : load commands from config file done, total {}, success {}, fail {}'.format(
                success+fail, success, fail))

    # properties
    @property
    def server_address(self):
        return self._server_address

    @server_address.setter
    def server_address(self, val):
        self._server_address = val

    @property
    def command_server_address(self):
        if '0.0.0.0' == self.ip:
            return ('127.0.0.1', self.port)
        else:
            return self.server_address

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
            soc.sendto(self.protocol.pack_message(running_test='CommandServer', state='request'), self.command_server_address)
            respond, _ = soc.recvfrom(1024)
            tag, kwargs = self.protocol.unpack_message(respond)
            if 'running_test' == tag and 'CommandServer' == kwargs['target'] and 'confirm' == kwargs['state']:
                return True
        except Exception as err:
            self._verbose_info('CommandServer : running_test : {}'.format(err.args))
        return False

    @property
    def verbose(self):
        return empty != self._verbose_info_handler

    @verbose.setter
    def verbose(self, val):
        if val:
            self._verbose_info_handler = logger.info
        else:
            self._verbose_info_handler = empty

    @property
    def commands(self):
        return self.__commands

    @property
    def is_main_server(self):
        return self.__is_main_server

    @is_main_server.setter
    def is_main_server(self, val):
        if self.__is_main_server == val:
            return
        if val:
            self._init_commands()
        else:
            self._clear_commands()
            self._init_basic_commands()
        self.__is_main_server = val

    # functional
    def _init_commands(self):
        default_commands_file = os.path.abspath(os.path.join('LRC','Server','commands.json'))
        try:
            self.load_commands_from_file(default_commands_file)
        except Exception as err:
            logger.error('CommandServer : load commands from default command file {} failed : {}'.format(default_commands_file, err.args))

    def _init_basic_commands(self): # those should not be deleted
        self.register_command('quit', Command(name='quit', execute=self.quit))
        self.register_command('register_command', Command(name='register_command', execute=self.register_command))
        self.register_command('list_commands', Command(name='list_commands', execute=self._list_commands))
        self.register_command('sync_config', Command(name='sync_config', execute=self._apply_remote_config))

    def _clear_commands(self):
        for k in self.commands.keys():
            logger.warning('CommandServer : commands {} removed'.format(k))
        self.commands.clear()
        logger.warning('CommandServer : commands cleared')

    def _execute_command(self, command, **kwargs):
        if command not in self.commands.keys():
            logger.error('CommandServer : command {} not registered'.format(command))
            return
        try:
            logger.info('CommandServer : executing command {}({})'.format(command, kwargs))
            self.commands[command].execute(**kwargs)
        except Exception as err:
            logger.error('CommandServer : failed executing command {} with error {}'.format(command, err.args))

    def _respond_request(self, client_address, request, **kwargs):
        self.socket.sendto(self.protocol.pack_message(respond=request+' confirm'), client_address)

    def _respond_running_test(self, client_address, **kwargs):
        if 'CommandServer' == kwargs['target']:
            self.socket.sendto(self.protocol.pack_message(running_test='CommandServer', state='confirm'), client_address)
        self._verbose_info('receive unavailable running_test {} from {}'.format(kwargs, client_address))

    def _dump_local_config(self): # dump config can work all right only in local
        d = dict()
        d['commands']  = self.commands
        # todo:
        # d['protocol']  = self.server_address
        return d

    def _dump_remote_config(self): # dump config can work all right only in local
        d = dict()
        d['server_address']  = self.server_address
        d['verbose']  = self.verbose
        return d

    def _apply_local_config(self, **kwargs): # apply config can work all right only in local
        if 'commands' in kwargs:
            self.commands.update(kwargs['commands'])

    def _apply_remote_config(self, **kwargs): # apply config can work all right remotely
        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']
        if 'server_address' in kwargs:
            if 'not started' == self.role:
                self.server_address = kwargs['server_address']
        if 'port' in kwargs:
            self.server_address = (self.server_address[0], kwargs["port"])
        if 'ip' in kwargs:
            self.server_address = (kwargs["ip"], self.server_address[1])

    def _load_commands(self, **command_config):
        success=0
        fail=0
        for command_name, command_body in command_config.items():
            try:
                command = parse_command(**command_body)
                self.register_command(command_name, command)
                success += 1
            except Exception as err:
                logger.error('CommandServer : load command {} failed with {} from command body {}'.format(command_name, err.args, command_body))
                fail += 1
        return success, fail

    def _load_commands_from_string(self, command_config_string):
        try:
            command_config = json.loads(command_config_string)
            return self._load_commands(**command_config)
        except Exception as err:
            logger.error('CommandServer : load commands failed with {} from string {}'.format(err.args, command_config_string))

    def _load_commands_from_file(self, command_file):
        try:
            with open(command_file, 'r') as fp:
                command_config_string = fp.read()
            return self._load_commands_from_string(command_config_string)
        except Exception as err:
            logger.error('CommandServer : load commands failed with {} from file {}'.format(err.args, command_file))

    def _verbose_info(self, message):
        self._verbose_info_handler('CommandServer : verbose : {}'.format(message))

    # local command entry
    def _list_commands(self,  *args, **kwargs):
        message = 'CommandServer : list commands : \n'
        for v in self.commands.values():
            message += '\t{}\n'.format(v)
        logger.info(message)


if '__main__' == __name__:

    def __test_case_001(): # send and execute command
        # start a Command Server
        s = CommandServer(port=35777, verbose=True)
        s.register_command('test_comm', Command(name='test_comm', execute=logger.info, args=('test_comm called',)))
        s.start()
        # try commands
        s.send_command(command='test_comm')
        s.send_command(command='quit')

    def __test_case_002(): # test sync_config
        # start a Command Server
        s_main = CommandServer(port=35777, verbose=False)
        s_main.register_command('test_comm', Command(name='test_comm', execute=logger.info, args=('test_comm called',)))
        s_main.start()
        # try commands
        s_sync = CommandServer(port=35777, verbose=True)
        s_sync.register_command('test_juice', Command(name='test_juice', execute=logger.info, args=('test_juice called',)))
        s_sync.sync_config()
        s_sync.send_command('list_commands')
        logger.info('s_sync role before start : {}'.format(s_sync.role))
        try:
            s_sync.start()
        except Exception as err:
            logger.error('start s_sync failed with : {}'.format(err.args))
        logger.info('s_sync role after start : {}'.format(s_sync.role))

    __test_case_002()