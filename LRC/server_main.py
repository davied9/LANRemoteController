from __future__ import print_function


def start_lrc_server_console():
    from LRC.Server.Config import LRCServerConfig

    config = LRCServerConfig()
    if config.enable_ui:
        from LRC.Common.logger import logger
        from multiprocessing import freeze_support
        from LRC.Server.ServerUI import LRCServerUI

        logger.set_logger('kivy')
        freeze_support()
        LRCServerUI().run()
    else:
        from LRC.Server.CommandServer import CommandServer
        import sys
        # start a new command server if necessary
        command_server = CommandServer(port=35777, verbose=True)
        if not command_server.is_running:
            command_server.start()
        # send the command
        for i in range(1,len(sys.argv)):
            command_server.send_command(sys.argv[i])


if __name__ == '__main__':
    start_lrc_server_console()
