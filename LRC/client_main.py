def main():
    import sys
    if '-h' in sys.argv or '--help' in sys.argv:
        print(_help_str())
        exit()
    if '--version' in sys.argv:
        from LRC.Common.info import version
        print('LRC version {}'.format(version))
        exit()
    verbose = False
    if '--verbose' in sys.argv:
        verbose = True

    import os
    from kivy.logger import logging
    from kivy.config import Config
    if sys.platform != 'win32':
        Config.set(section="kivy", option="log_dir", value="/sdcard/DAV")
    config_file_path = os.path.abspath(os.path.join('Client', 'android.ini'))
    Config.read(config_file_path)

    logging.info("{:12}: loading config from {}".format( 'Entry', config_file_path) )

    from LRC.Common.logger import logger
    from LRC.Client.ClientUI import ClientUI

    logger.set_logger(name='kivy')

    # start application
    ClientUI(verbose=verbose).run()


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
