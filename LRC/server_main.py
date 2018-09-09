def main():

    def get_default_config():
        pass

    def parse_arguments():
        pass

    from LRC.Common.logger import logger
    from multiprocessing import freeze_support
    from LRC.Server.ServerUI import LRCServerUI
    logger.set_logger('kivy')
    freeze_support()
    LRCServerUI().run()


if __name__ == '__main__':
    main()
