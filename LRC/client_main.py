def main():
    import sys
    if '-h' in sys.argv or '--help' in sys.argv:
        print(_help_str())
        exit()
    if '--version' in sys.argv:
        from LRC.Common.info import version
        print('LRC version {}'.format(version))
        exit()

    from LRC.Common.logger import logger as LRCLogger
    LRCLogger.set_logger(name='kivy')

    verbose = False
    if '--verbose' in sys.argv:
        verbose = True
        sys.argv.remove('--verbose')

    import os
    from kivy.logger import logging
    from kivy.config import Config
    from kivy.utils import platform
    if platform == 'android': # set log path to sdcard for android devices
        Config.set(section="kivy", option="log_dir", value="/sdcard/LRC/logs")
        verbose=True

    if verbose:
        logging.info("{:12}: system path {}".format( 'Entry', sys.path) )
        walk_working_dir()
    config_file_path = os.path.abspath(os.path.join('Client', 'android.ini'))
    Config.read(config_file_path)

    logging.info("{:12}: loading config from {}".format( 'Entry', config_file_path) )
    logging.info("{:12}: plaform {}".format( 'Entry', sys.platform) )

    # start application
    from LRC.Client.ClientUI import ClientUI
    ClientUI(verbose=verbose).run()


def walk_working_dir():
    import os
    from kivy.logger import logging
    for root, dirs, files in os.walk(os.getcwd()):
        logging.info('{:12}: {} :'.format('walking', root))
        for file in files:
            logging.info('{:12}:     {}'.format('walking', file))


def _help_str():
    return '''
LRC server
[Usage]
    lrcwaiter

[options]
    --help, -h              show this help info
    --version               show LRC version
    --verbose               show more information in log

[more]
    for more infomation, see https://github.com/davied9/LANRemoteController
'''


if '__main__' == __name__:
    main()
