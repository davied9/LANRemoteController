if '__main__' == __name__:
    import Common
    from ClientWin import ClientUI
    Common.logger.logger.set_logger('kivy')
    # start application
    ClientUI().run()
