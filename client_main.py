if '__main__' == __name__:
    from kivy.config import Config
    Config.read('Client/android.ini')

    from Common.logger import logger
    from Client import ClientUI

    logger.set_logger('kivy')

    # start application
    ClientUI().run()
