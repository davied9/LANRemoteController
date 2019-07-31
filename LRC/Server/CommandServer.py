from __future__ import print_function
from LRC.Server.Config import LRCServerConfig
from LRC.Server.Command import Command, parse_command
from LRC.Common.logger import logger
from LRC.Common.Exceptions import ArgumentError
from LRC.Common.empty import empty
from LRC.Protocol.v1.CommandServerProtocol import CommandServerProtocol
from multiprocessing import Manager
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
import os, json

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


class CommandServer(UDPServer):

    # interfaces
    def __init__(self, *, verbose=False, sync_config=False, server_address=('127.0.0.1', 35589), ip=None, port=None, **kwargs):
        # initial configuration
        self.verbose = verbose
        self.__sync_config = sync_config
        # initialize command server
        if port:
            server_address = (server_address[0], port)
        if ip:
            server_address = (ip, server_address[1])
        super(CommandServer, self).__init__(server_address=server_address, RequestHandlerClass=None, bind_and_activate=False)
        # initialize protocol
        self.protocol = CommandServerProtocol()
        # initialize commands
        self.__commands = dict()
        self._init_basic_commands()
        self.__is_main_server = False
        # initialize role
        self.role = 'not started' # 'not started' 'main' 'secondary'
        self.__cleanup_commands = list()
        # initialize temp_socket
        self.__temp_socket = None

    def finish_request(self, request, client_address):
        self._verbose_info('CommandServer : got request {} from client {}'.format(request, client_address))
        try:
            # parse command from request
            tag, kwargs = self.protocol.unpack_message(request[0])
            self._verbose_info('CommandServer : unpack result : {}, {}'.format(tag, kwargs))
            # execute command
            if 'command' == tag:
                command = kwargs['name']
                if 'args' in kwargs:
                    args = kwargs['args']
                    del kwargs['args']
                else:
                    args = list()
                del kwargs['name']
                self._execute_command_from_remote(client_address, command, *args, **kwargs)
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

    def quit(self):
        def shutdown_tunnel(server):
            server.shutdown()
        # shutdown must be called in another thread, or it will be blocked forever
        Thread(target=shutdown_tunnel, args=(self,)).start()
        for key in self.cleanup_commands:
            try:
                self._verbose_info('execute cleanup command {}'.format(key))
                self.commands[key].execute()
            except Exception as err:
                logger.error('LRC : execute cleanup command {} failed {}({})'.format(key, err, err.args))
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
        # accessing remote main command server -- sync_config
        # done : sync_config command should actually do the following code, but for now just send 'sync_config' command
        #        sync_config do not directly execute command, use --sync-config flag in console
        # done : sync verbose for only current command
        if not self.is_main_server:
            self._send_command('sync_config', **self._dump_remote_config())

    def show_config(self):
        config = self._dump_remote_config()
        msg = 'CommandServer : configurations :\n'
        for k, v in config.items():
            msg += '    {:22} : {}\n'.format(k, v)
        logger.info(msg)

    def register_cleanup_command(self, *keys):
        for key in keys:
            if key in self.cleanup_commands:
                self._verbose_info('duplicate cleanup command {}'.format(key))
                continue
            logger.info('CommandServer : add cleanup command {}'.format(key))
            self.cleanup_commands.append(key)

    def register_cleanup_command_remotely(self, *args):
        # accessing remote main command server -- register_cleanup_command_remotely
        self.send_command('register_cleanup_command', args=args)

    def register_command(self, key, command, *, overwrite=False):
        if not overwrite and key in self.commands.keys():
            self._verbose_info('duplicate command {}, abort'.format(key))
            return False
        logger.info('CommandServer : add command {} {}'.format(key, command))
        self.commands[key] = command
        return True

    def register_command_remotely(self, command_config, *, overwrite=False):
        # accessing remote main command server -- register_command_remotely
        self.send_command('register_command', command_config=command_config, overwrite=overwrite)

    def send_command(self, command, *, sync_config_for_one_shot=False, args=(), **kwargs):
        if self.need_sync_config or sync_config_for_one_shot:
            self.sync_config()
        # accessing remote main command server -- send_command
        if self.is_main_server: # for main server, execute locally
            self._execute_command_locally(command, *args, **kwargs)
        else: # for other server, send command to main server
            self._send_command(command, args=args, **kwargs)

    def load_commands(self, command_config, *, overwrite=False):
        logger.info('CommandServer : load commands from config :\n{}'.format(command_config))
        done, fail, ignore = self._load_commands(command_config, overwrite=overwrite)
        logger.info('CommandServer : load commands from config done, total {}, done {}, ignore {}, fail {}'.format(
                done+fail+ignore, done, ignore, fail))

    def load_commands_from_string(self, command_config_string, *, overwrite=False):
        logger.info('CommandServer : load commands from config string :\n{}'.format(command_config_string))
        done, fail, ignore = self._load_commands_from_string(command_config_string, overwrite=overwrite)
        logger.info('CommandServer : load commands from config string done, total {}, done {}, ignore {}, fail {}'.format(
                done+fail+ignore, done, ignore, fail))

    def load_commands_from_file(self, command_file, *, overwrite=False):
        logger.info('CommandServer : load commands from config file :\n{}'.format(command_file))
        done, fail, ignore = self._load_commands_from_file(command_file, overwrite=overwrite)
        logger.info('CommandServer : load commands from config file done, total {}, done {}, ignore {}, fail {}'.format(
                done+fail+ignore, done, ignore, fail))

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
    def temp_socket(self): # this socket is used as a client to main command server, when this server is not main
        if not self.__temp_socket:
            self.__temp_socket = self._get_temp_socket()
        return self.__temp_socket

    @property
    def is_running(self):
        try:
            self.temp_socket.sendto(self.protocol.pack_message(running_test='CommandServer', state='request'), self.command_server_address)
            respond, _ = self.temp_socket.recvfrom(1024)
            tag, kwargs = self.protocol.unpack_message(respond)
            if 'running_test' == tag:
                return ('CommandServer' == kwargs['target'] and 'confirm' == kwargs['state'])
            else:
                logger.error('CommandServer : [abnormal] got {} message while expecting running_test result'.format(tag))
        except: pass
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
    def need_sync_config(self):
        return self.__sync_config

    @property
    def commands(self):
        return self.__commands

    @property
    def cleanup_commands(self):
        return self.__cleanup_commands

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
    def _init_commands(self): # loading default commands from current directory
        default_commands_file = os.path.abspath('default_commands.json')
        try:
            self._load_commands_from_file(default_commands_file)
        except Exception as err:
            self._verbose_info('CommandServer : load commands from default command file {} failed : {}'.format(default_commands_file, err.args))

    def _init_basic_commands(self): # those should not be deleted
        # place associated command definition is not approved
        # do not define command like 'def execute(var1, var2)'
        # use kwargs instead, like 'def execute(var1='default', var2=None)'
        # place not related command is OK, such as :
        # 'def execute(*args)'
        self.commands['quit'] = Command(name='quit', execute=self.quit)
        self.commands['register_command'] = Command(name='register_command', execute=self.load_commands, kwargs=dict())
        self.commands['register_cleanup_command'] = Command(name='register_cleanup_command', execute=self.register_cleanup_command, args=tuple())
        self.commands['list_commands'] = Command(name='list_commands', execute=self._list_commands)
        self.commands['sync_config'] = Command(name='sync_config', execute=self._apply_remote_config, kwargs=dict())
        self.commands['show_config'] = Command(name='show_config', execute=self.show_config)

    def _clear_commands(self):
        for k in self.commands.keys():
            logger.warning('CommandServer : commands {} removed'.format(k))
        self.commands.clear()
        logger.warning('CommandServer : commands cleared')

    def _send_command(self, command, *, args=(), **kwargs):
        try:
            # done : send_command should first check local configurations, make sure local settings of commands should be executed
            kwargs = self._update_command_config(command, args, kwargs)
            logger.info('CommandServer : send command {}({}) to {}'.format(command, kwargs, self.command_server_address))
            # todo : send command will sync target command to execution server before execution
            # send command
            self.temp_socket.sendto(self.protocol.pack_message(command=command, **kwargs), self.command_server_address)
            # done : send command will check execution result after send one
            respond_msg, _ = self.temp_socket.recvfrom(1024)
            tag, kwargs = self.protocol.unpack_message(respond_msg)
            #   detail : check result
            if 'respond' == tag and 'command' == kwargs['request'] and 'success' == kwargs['state']:
                logger.info('CommandServer : execute command {} on {} success'.format(kwargs['command_name'], self.command_server_address))
            else: # 'respond' != tag -> send command is used for other server(except for main), when this server is running, this may happen when load is full
                if 'respond' != tag:
                    logger.error('CommandServer : [abnormal] got {} message while expecting respond of command'.format(tag))
                elif 'command' != kwargs['request']:
                    logger.error('CommandServer : [abnormal] got {} respond while expecting respond of command'.format(kwargs['request']))
                elif 'success' != kwargs['state']:
                    raise RuntimeError(kwargs['err_info'])
        except Exception as err:
            logger.error('CommandServer : send command {} failed with {}({})'.format(command, err, err.args))

    def _execute_command_locally(self, command, *args, **kwargs):
        logger.info('CommandServer : execute command {}({},{}) locally'.format(command, args, kwargs))
        try:
            self._execute_command_imp(command, *args, **kwargs)
            logger.info('CommandServer : execute command {} successful'.format(command))
            return True
        except Exception as err:
            logger.error('CommandServer : execute command {} failed with error {}'.format(command, err.args))
            return False

    def _execute_command_from_remote(self, client_address, command, *args, **kwargs):
        logger.info('CommandServer : execute command {}({},{}) from {}'.format(command, args, kwargs, client_address))
        # execute command
        try:
            self._execute_command_imp(command, *args, **kwargs)
            logger.info('CommandServer : execute command {} successful'.format(command))
            msg = self.protocol.pack_message(respond='command', command_name=command, state='success')
            success = True
        except Exception as err:
            err_info = 'CommandServer : execute command {} failed with error {}'.format(command, err.args)
            logger.error(err_info)
            msg = self.protocol.pack_message(respond='command', command_name=command, state='failed', err_info=err_info)
            success = False
        # send execute result
        self.socket.sendto(msg, client_address)
        return success

    def _execute_command_imp(self, command, *args, **kwargs):
        if command not in self.commands.keys():
            raise ValueError('CommandServer : command {} not registered'.format(command))
        self.commands[command].execute(*args, **kwargs)

    def _update_command_config(self, command, args, kwargs):
        '''
        sync arguments to command arguments : priority : command line > register > command definition
        :param command:     command name
        :param args:        command args
        :param kwargs:      command kwargs
        :return kwargs:     command kwargs merged from args, input kwargs, and command args && kwargs registered in self.commands
        '''
        if command in self.commands.keys():
            self._verbose_info('CommandServer : found local command {}({})'.format(command, self.commands[command]))
            if hasattr(self.commands[command], 'kwargs'):
                if self.commands[command].kwargs is None:
                    if kwargs:
                        raise ArgumentError('command {} do not support kwargs, got {}'.format(command, kwargs))
                else:
                    kwargs.update(self.commands[command].kwargs)
            if hasattr(self.commands[command], 'args'):
                if self.commands[command].args is None:
                    if args:
                        raise ArgumentError('command {} do not support args, got {}'.format(command, args))
                else:
                    _args = list(self.commands[command].args)
                    if args:
                        _args.extend(args)
                    kwargs['args'] = _args
        return kwargs

    def _respond_request(self, client_address, request, **kwargs):
        msg = self.protocol.pack_message(respond=request, state ='confirm')
        self._verbose_info('CommandServer : send "{}" to {}'.format(msg, client_address))
        self.socket.sendto(msg, client_address)

    def _respond_running_test(self, client_address, **kwargs):
        if 'CommandServer' == kwargs['target']:
            if 'request' == kwargs['state']:
                self.socket.sendto(self.protocol.pack_message(running_test='CommandServer', state='confirm'), client_address)
                return
        logger.warning('receive unavailable running_test {} from {}'.format(kwargs, client_address))

    def _get_temp_socket(self):
        temp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        temp_socket.settimeout(0.5)
        return temp_socket

    def _dump_local_config(self): # dump config can work all right only in local
        d = dict()
        d['commands']  = self.commands
        d['server_address']  = self.server_address
        # todo: try to sync protocol
        # d['protocol']  = self.server_address
        return d

    def _dump_remote_config(self): # dump config can work all right only in local
        d = dict()
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

    def _load_commands(self, command_config, *, overwrite=False):
        done=0
        fail=0
        ignore=0
        for command_name, command_body in command_config.items():
            try:
                command = parse_command(**command_body)
                if self.register_command(command_name, command, overwrite=overwrite):
                    done += 1
                else:
                    ignore += 1
            except Exception as err:
                logger.error('CommandServer : load command {} failed with {}({}) from command body {}'.format(command_name, err, err.args, command_body))
                fail += 1
        return done, fail, ignore

    def _load_commands_from_string(self, command_config_string, *, overwrite=False):
        try:
            command_config = json.loads(command_config_string)
            return self._load_commands(**command_config, overwrite=overwrite)
        except Exception as err:
            logger.error('CommandServer : load commands failed with {}({}) from string {}'.format(err, err.args, command_config_string))

    def _load_commands_from_file(self, command_file, *, overwrite=False):
        try:
            with open(command_file, 'r') as fp:
                command_config_string = fp.read()
            return self._load_commands_from_string(command_config_string, overwrite=overwrite)
        except Exception as err:
            logger.error('CommandServer : load commands failed with {}({}) from file {}'.format(err, err.args, command_file))

    def _verbose_info(self, message):
        self._verbose_info_handler('CommandServer : [verbose] {}'.format(message))

    # local command entry
    def _list_commands(self): # entry for command "list_commands"
        message = 'CommandServer : list commands : \n'
        for k, v in self.commands.items():
            message += '{:22} -- {}\n'.format(k, v)
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
        s_main = CommandServer(verbose=True)
        s_main.start()
        # try commands
        s_sync = CommandServer(verbose=False)
        s_sync.sync_config()
        # test s_main config
        logger.info('before sync -- s_main.verbose = {}'.format(s_main.verbose))
        from time import sleep
        sleep(0.5)
        logger.info('after sync -- s_main.verbose = {}'.format(s_main.verbose))

    def __test_case_003(): # test start a duplicate command server, see the role changing
        # start a Command Server
        s_main = CommandServer()
        s_main.start()
        # try commands
        s_sync = CommandServer()
        # try start another time
        from time import sleep
        sleep(0.5)
        logger.info('')
        logger.info('')
        logger.info('')
        logger.info('s_sync role before start : {}'.format(s_sync.role))
        try:
            s_sync.start()
        except Exception as err:
            logger.error('start s_sync failed with : {}'.format(err.args))
        logger.info('s_sync role after start : {}'.format(s_sync.role))

    def __test_case_004(): # test
        command_config = {
            "test_juice":{
                "import":"LRC.Common.logger",
                "execute":"logger.warning",
                "args":("test_juice",)
            },
            "test_kwargs":{
                "import":"LRC.Server.Commands.LRCServer",
                "execute":"start_lrc",
                "kwargs":{
                    "server_address":("127.0.0.1", 35789)
                 }
            }
        }
        # start a Command Server
        s_main = CommandServer(verbose=True)
        s_main.start()
        # start a client command server
        s_sync = CommandServer(verbose=True)
        s_sync.register_command_remotely(command_config)
        s_sync.send_command('list_commands')
        s_sync.send_command('test_juice')
        s_sync.send_command('test_kwargs')

    __test_case_004()