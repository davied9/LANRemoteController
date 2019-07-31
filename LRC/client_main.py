
def main():
    import sys
    parsed_args = parse_config_from_console_line_with_parser(sys.argv[1:])
    sys.argv = [sys.argv[0]]

    from LRC.Common.logger import logger as LRCLogger
    LRCLogger.set_logger(name='kivy')

    verbose = parsed_args.verbose

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


def parse_config_from_console_line_with_parser(args):
    from LRC.Common.info import version, url, client_entry
    import argparse

    # help description
    parser = argparse.ArgumentParser(description= '''
LANRemoteController

[more]
    for more information, see {}
'''.format(url), prog=client_entry)
    # version info
    parser.add_argument('--version', '-v', help='version', action='version', version='''
LRC(LAN Remote Controller) version {}
{}
'''.format(version, url))
    # arguments
    parser.add_argument('--verbose', '-vv', help='increase log verbose level', default=False, action='store_true')

    return parser.parse_args(args=args)


def walk_working_dir():
    import os
    from kivy.logger import logging
    for root, dirs, files in os.walk(os.getcwd()):
        logging.info('{:12}: {} :'.format('walking', root))
        for file in files:
            logging.info('{:12}:     {}'.format('walking', file))


if '__main__' == __name__:
    main()
