if '__main__' == __name__:
    import os, sys; sys.path.append(os.path.dirname(sys.argv[0]))
    
    from kivy.config import Config
    Config.read(os.path.join('Client', 'android.ini'))

    from Common.logger import logger
    from Client.ClientUI import ClientUI

    logger.set_logger('kivy')

    # start application
    ClientUI().run()
