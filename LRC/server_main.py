from __future__ import print_function
from LRC.Common.logger import logger
from LRC.Server.Config import LRCServerConfig


def main():
    import sys
    config, commands = parse_config_from_console_line(*sys.argv[1:])
    start_lrc_server_console(config, commands)


def start_lrc_server_console(config, commands):

    if config.enable_ui:
        from multiprocessing import freeze_support
        from LRC.Server.ServerUI import LRCServerUI

        logger.set_logger('kivy')
        freeze_support()
        LRCServerUI().run()
    else:
        from LRC.Server.CommandServer import CommandServer
        import sys
        # start a new command server if necessary
        command_server = CommandServer(**config.command_server_config)
        if not command_server.is_running:
            command_server.start()
        # send the command
        for cmd in commands:
            command_server.send_command(cmd)


def parse_config_from_console_line(*args):
    # init
    reserved = []
    commands = []
    config = LRCServerConfig()
    config_command_lines = dict()
    # parse command lines
    ix = 0
    while ix < len(args):
        arg = args[ix]
        if '--no-ui' == arg:
            config_command_lines['enable_ui'] = False
        elif '--enable-ui' == arg:
            config_command_lines['enable_ui'] = True
        elif '--verbose' == arg:
            config_command_lines['verbose'] = True
        elif arg.startswith('--config-file='):
            config.config_file = arg[len('--config-file='):]
        else:
            if arg.startswith('--'):
                reserved.append(arg)
            else:
                commands.append(arg)
        ix += 1
    # sync config with command line configurations
    config.apply_config(**config_command_lines)
    # clean up
    if 0 == len(commands):
        logger.info('LRC : no command given, start_lrc will be executed.')
        commands.append('start_lrc')

    if 0 != len(reserved):
        logger.warning('LRC : unknown options : {}.'.format(reserved))

    return config, commands


if __name__ == '__main__':
    main()
