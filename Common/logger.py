from __future__ import print_function


class LRCLogger(object):

    def __init__(self, **kwargs):
        self._info_handler = print
        self._warning_handler = print
        self._error_handler = print

    def log(self, *args):
        self._info_handler(*args)

    def info(self, *args):
        self._info_handler(*args)

    def warning(self, *args):
        self._warning_handler(*args)

    def error(self, *args):
        self._error_handler(*args)

    def replace_info_handler(self, handler):
        self._info_handler = handler

    def replace_warning_handler(self, handler):
        self._warning_handler = handler

    def replace_error_handler(self, handler):
        self._error_handler = handler

    def set_logger(self, keyword):
        if 'kivy' == keyword:
            import kivy.logger
            self._info_handler      = kivy.logger.Logger.info
            self._warning_handler   = kivy.logger.Logger.warning
            self._error_handler     = kivy.logger.Logger.error

logger = LRCLogger()
