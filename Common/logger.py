from __future__ import print_function


class LRCLogger(object):

    def __init__(self, handler=print):
        self.log_handler = handler

    def log(self, *args):
        self.log_handler(*args)


logger = LRCLogger()

def log(*args):
    logger.log(*args)
