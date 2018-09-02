
if __name__ == '__main__':
    import os, sys; sys.path.append(os.path.dirname(sys.argv[0]))

    import Common.logger
    from multiprocessing import freeze_support
    from Server.ServerUI import LRCServerUI
    Common.logger.logger.set_logger('kivy')
    freeze_support()
    LRCServerUI().run()

