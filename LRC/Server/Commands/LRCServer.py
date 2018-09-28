from LRC.Server.LRCServer import LRCServerManager
from multiprocessing import Process, Manager, freeze_support


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