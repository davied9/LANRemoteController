from __future__ import print_function
from LRC.Server.Config import get_default_server_config
from LRC.Server.LRCServer import start_LRCWaiter, start_LRCServer
from LRC.Common.logger import logger
from multiprocessing import Process, Manager
from threading import Thread

try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer
except:
    print('can not import packages for UDPServer.')


class CommandServer(UDPServer):

    def __init__(self, **kwargs):
        UDPServer.__init__(self, kwargs["server_address"], None)

    def finish_request(self, request, client_address):


        return

    

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


def start_lrc_server_console(config=get_default_server_config()):
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