
if __name__ == '__main__':
    import Common
    from multiprocessing import freeze_support
    from Server import LRCServerUI
    Common.logger.set_logger('kivy')
    freeze_support()
    LRCServerUI().run()

