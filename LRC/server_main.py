from __future__ import print_function
from LRC.Common.logger import logger


def main():
    import sys
    # parse config
    parsed_args = parse_config_from_console_line_with_parser(sys.argv[1:])
    # clean arguments
    sys.argv = [sys.argv[0]]
    # start server
    start_lrc_server_new_entry(parsed_args)


def get_lrc_config(parsed_args):
    from LRC.Server.Config import LRCServerConfig
    lrc_config = LRCServerConfig()
    if parsed_args.lrc_server_address:
        lrc_config.update_server_config(server_address=eval(parsed_args.lrc_server_address))
    if parsed_args.lrc_waiter_address:
        lrc_config.update_waiter_config(waiter_address=eval(parsed_args.lrc_waiter_address))
    if parsed_args.lrc_verify_code:
        lrc_config.apply_config(verify_code=parsed_args.lrc_verify_code)

    lrc_config.apply_config(
        verbose=parsed_args.verbose,
        enable_ui=parsed_args.enable_ui,
        sync_config=parsed_args.sync_config
    )

    return lrc_config

def start_lrc_server_new_entry(parsed_args):

    if parsed_args.enable_ui:
        from multiprocessing import freeze_support
        from LRC.Server.ServerUI import LRCServerUI

        freeze_support()
        logger.set_logger(name='kivy')

        if parsed_args.commands:
            logger.warning('LRC : UI is enabled, commands {} will not be executed.'.format(parsed_args.commands))

        ui = LRCServerUI()
        ui.run()
    else:
        from LRC.Server.CommandServer import CommandServer
        import sys

        lrc_config = get_lrc_config(parsed_args)
        # start a new command server if necessary
        command_server = CommandServer()
        register_lrc_commands(command_server, lrc_config)
        if not command_server.is_running:
            command_server.start()

        # send the command
        for cmd in parsed_args.commands:
            command_server.send_command(cmd)


def parse_config_from_console_line_with_parser(args):
    from LRC.Common.info import version, url, server_entry, description
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter

    # help description
    parser = ArgumentParser(
        prog=server_entry,
        formatter_class=RawTextHelpFormatter,
        description= description,
        epilog='''

[example]
    {} --no-ui start_lrc --lrc-server-address ('0.0.0.0',35589)
    {} --no-ui stop_lrc      # you may need to run this in another command window

[more]
    for more information, see {}

'''.format(server_entry, server_entry, url) )

    # version info
    parser.add_argument('--version', '-v', help='version', action='version', version='''
LRC(LAN Remote Controller) version {}
{}
'''.format(version, url))

    # arguments
    parser.add_argument('--no-ui', help='disable ui', dest='enable_ui', default=True, action='store_false')
    parser.add_argument('--verbose', '-vv', help='increase log verbose level', default=False, action='store_true')
    parser.add_argument('--sync-config', help='command server sync local config to main command server',
                        default=False, action='store_true')
    parser.add_argument('--config-file', help='configuration file')
    parser.add_argument('--lrc-server-address', help='lrc server address')
    parser.add_argument('--lrc-waiter-address', help='lrc waiter address')
    parser.add_argument('--lrc-verify-code', help='lrc verify code')
    parser.add_argument('commands', help='commands to execute on command server', nargs='*')
    return parser.parse_args(args=args)


def register_lrc_commands(command_server, lrc_config):
    from LRC.Server.Commands.LRCServer import start_lrc, start_lrc_server, start_lrc_waiter
    from LRC.Server.Commands.LRCServer import stop_lrc, stop_lrc_server, stop_lrc_waiter
    from LRC.Server.Commands.LRCServer import quit as quit_lrc
    from LRC.Server.Command import Command

    # start/stop LRC
    command_server.register_command('start_lrc', Command(name='start_lrc', execute=start_lrc,
        kwargs={'server_address':lrc_config.server_address, 'waiter_address': lrc_config.waiter_address} ))
    command_server.register_command('stop_lrc', Command(name='stop_lrc', execute=stop_lrc))

    # start/stop LRC server
    command_server.register_command('start_lrc_server', Command(name='start_lrc_server', execute=start_lrc_server,
        kwargs={'server_address':lrc_config.server_address}))
    command_server.register_command('stop_lrc_server', Command(name='stop_lrc_server', execute=stop_lrc_server))

    # start/stop LRC waiter
    command_server.register_command('start_lrc_waiter', Command(name='start_lrc_waiter', execute=start_lrc_waiter,
        kwargs={'waiter_address': lrc_config.waiter_address}))
    command_server.register_command('stop_lrc_waiter', Command(name='stop_lrc_waiter', execute=stop_lrc_waiter))

    # quit LRC
    command_server.register_command('quit_lrc', Command(name='quit_lrc', execute=quit_lrc))
    command_server.register_cleanup_command('quit_lrc')


if __name__ == '__main__':
    main()
