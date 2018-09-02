if '__main__' == __name__:
    from kivy.config import Config
    Config.read('ClientWin/android.ini')

    from Common.logger import logger
    from ClientWin import ClientUI

    logger.set_logger('kivy')

    # start application
    ClientUI().run()
