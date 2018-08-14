
if __name__ == '__main__':
    import Common.logger
    from multiprocessing import freeze_support
    from Server import LRCServerUI
    Common.logger.logger.set_logger('kivy')
    freeze_support()
    LRCServerUI().run()

