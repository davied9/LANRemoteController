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
        'quit'          :   Command(name='exit', execute=exit, args=None),
        'test_comm'    :   Command(name='exit', execute=print, args=('test')),
    }

    # interfaces
    def __init__(self, **kwargs):
        self.port = kwargs["port"]
        self.ip = kwargs["ip"] if 'ip' in kwargs else '127.0.0.1'
        self.protocol = CommandServerProtocol()
        UDPServer.__init__(self, self.server_address, None)


    def finish_request(self, request, client_address):
        # parse command from request
        cmd = self.protocol.unpack_message(request[0])
        # execute command
        self._execute_command(cmd)

    # properties
    @property
    def server_address(self):
        return (self.ip, self.port)

    # functional interfaces
    def _execute_command(self, command, *args):
        try:
            logger.info('ComandServer : executing command {}'.format(command))
            self.commands[command].execute()
        except Exception as err:
            logger.error('ComandServer : failed with {}'.format(err))




def _mailbox_watcher(mail_box):
    while True:
        try:
            logger.info(mail_box.get()) # get will block until there is data
        except Exception as err:
            if not logger.running:
                logger.info('Server : closing servers.')
                break
            else:
                logger.error('Error : {}'.format(err))


def start_lrc_server_console(config=LRCServerConfig()):
    manager = Manager()
    client_list = manager.list()
    mail_box = manager.Queue()

    logger.info('starting console with config : {}'.format(config))

    waiter_process = Process( target=start_LRCServer, args=(
                config.server_address,
                config.waiter_address,
                config.verify_code,
                client_list,
                mail_box
    ))
    waiter_process.start()

    server_process = Process( target=start_LRCWaiter, args=(
            config.waiter_address,
            config.server_address,
            client_list,
            mail_box
    ))
    server_process.start()

    # watcher_thread = Thread(
    #
    #
    # )

    return


if '__main__' == __name__:

    def __test_case_000():
        start_lrc_server_console()
        return

    __test_case_000()