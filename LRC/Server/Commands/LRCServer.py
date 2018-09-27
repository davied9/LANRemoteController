from LRC.Server.Command import BaseCommand
from LRC.Common.logger import logger
from LRC.Server.LRCServer import LRCServer, LRCWaiter
from multiprocessing import Process, Manager, freeze_support


def start_server(**kwargs):
    '''
    start LRC server with given parameters
    :param kwargs:
        required :
            server_address      -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address      -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding    -- 'utf-8'(default)
            verify_code         -- None
            client_list         -- None
            log_mailbox         -- None
    :return:
    '''
    LRCServer(**kwargs).serve_forever()


def start_waiter(**kwargs):
    '''
    start LRC waiter with given parameters
    :param kwargs:
        required :
            connect_server_address  -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address          -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding        -- 'utf-8'(default)
            verify_code             -- None
            client_list             -- None
            log_mailbox             -- None
    :return:
    '''
    LRCWaiter(**kwargs).serve_forever()


class LRCServerManager(object):

    def __init__(self):
        try:
            self.communication_manager = Manager()
            self.client_list = self.communication_manager.list()
            self.log_mailbox = self.communication_manager.Queue()
            self.mode = 'full'
        except Exception as err:
            logger.error('LRC : Manager start failed, only basic function started')
            self.communication_manager = None
            self.client_list = None
            self.log_mailbox = None
            self.mode = 'basic'

        self._server_process = None
        self.server_config = dict()

        self._waiter_process = None
        self.waiter_config = dict()

    # commands interfaces
    def start_server(self, **kwargs):
        kwargs = self._update_server_config(kwargs)
        self._start_server(**kwargs)

    def stop_server(self):
        if self._server_process:
            if self._server_process.is_alive():
                logger.info('LRC : stop server')
                self._server_process.terminate()
            self._server_process = None

    def start_waiter(self, **kwargs):
        kwargs = self._update_waiter_config(kwargs)
        self._start_waiter(**kwargs)

    def stop_waiter(self):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                logger.info('LRC : stop waiter')
                self._waiter_process.terminate()
            self._waiter_process = None

    def quit(self):
        self.stop_server()
        self.stop_waiter()

    # functional
    def _update_server_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox
        return config

    def _start_server(self, **kwargs):
        if self._server_process:
            if self._server_process.is_alive():
                if kwargs == self.server_config:
                    logger.info('LRC : server already running')
                    return
                else:
                    logger.info('LRC : terminate server process for restart')
                    self._server_process.terminate()
            self._server_process = None
        try:
            self._server_process = Process(target=start_server, kwargs=kwargs)
            self._server_process.start()
            self.server_config = kwargs
            logger.info('LRC : start server process at {}'.format(kwargs['server_address']))
        except Exception as err:
            logger.error('LRC : start server process failed : {}'.format(err.args))

    def _update_waiter_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox
        return config

    def _start_waiter(self, **kwargs):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                if kwargs == self.waiter_config:
                    logger.info('LRC : waiter already running')
                    return
                else:
                    logger.info('LRC : terminate waiter process for restart')
                    self._waiter_process.terminate()
            self._waiter_process = None
        try:
            self._waiter_process = Process(target=start_waiter, kwargs=kwargs)
            self._waiter_process.start()
            self.waiter_config = kwargs
            logger.info('LRC : start waiter process at {}'.format(kwargs['waiter_address']))
        except Exception as err:
            logger.error('LRC : start waiter process failed : {}'.format(err.args))


_manager = None
def manager():
    global _manager
    if not _manager:
        _manager = LRCServerManager()
    return _manager


if '__main__' == __name__:

    def test_case_000(): # basic usage
        from LRC.Server.Config import LRCServerConfig
        from time import sleep
        freeze_support()

        manager = LRCServerManager()

        config = LRCServerConfig()
        config.server_port = 35530
        config.waiter_port = 35527

        manager.start_server(**config.server_config)
        manager.start_waiter(**config.waiter_config)

        sleep(30)
        manager.quit()


    def test_case_001():
        from LRC.Server.Config import LRCServerConfig
        from time import sleep

        config = LRCServerConfig()
        config.server_port = 35530
        config.waiter_port = 35527

        manager().start_server(**config.server_config)
        manager().start_waiter(**config.waiter_config)

        sleep(30)
        manager().quit()


    test_case_001()