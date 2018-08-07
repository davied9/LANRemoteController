from Common.KivyImporter import *

from kivy.logger import Logger
import Common.logger

try:
    from kivy.uix.screenmanager import CardTransition
except ImportError:
    Logger.error('Import: can\'t import CardTransition')
try:
    from kivy.uix.screenmanager import SwapTransition
except ImportError:
    Logger.error('Import: can\'t import SwapTransition')
try:
    from kivy.uix.screenmanager import ShaderTransition
except ImportError:
    Logger.error('Import: can\'t import ShaderTransition')
try:
    from kivy.uix.screenmanager import SlideTransition
except ImportError:
    Logger.error('Import: can\'t import SlideTransition')
try:
    from kivy.uix.screenmanager import WipeTransition
except ImportError:
    Logger.error('Import: can\'t import WipeTransition')
try:
    from kivy.uix.screenmanager import FadeTransition
except ImportError:
    Logger.error('Import: can\'t import FadeTransition')
try:
    from kivy.uix.screenmanager import FallOutTransition
except ImportError:
    Logger.error('Import: can\'t import FallOutTransition')
try:
    from kivy.uix.screenmanager import RiseInTransition
except ImportError:
    Logger.error('Import: can\'t import RiseInTransition')

import os, json
from ClientWin.ControllerCollectionScreen import ControllerCollectionScreen
from ClientWin.ControllerCollectionBuildScreen import ControllerCollectionBuildScreen
from ClientWin.ControllerScreen import ControllerScreen
from ClientWin.LRCClientWin import LRCClient


class ClientUI(App):
    '''Client Graphic User Interface

    components:
        screen_manager:                 screen manager
        screen_manager.last_screen:     last screen
        controller_sets:                all controller collections loaded from local files
        current_edit_set:               current edited controller set
        client:                         client ( LRCClientConnector ), provide access for LRCClient

    '''

    def build(self):
        Logger.info('Start: working directory : {0}'.format( os.getcwd() ))

        self.controller_sets = None
        self.current_edit_set = None # for sync between build screen and controller screen
        self.client = LRCClient()

        self.screen_manager = ScreenManager(transition=RiseInTransition())

        self.controller_set_screen = ControllerCollectionScreen(name='Controller Collections')
        self.screen_manager.add_widget(self.controller_set_screen)

        self.controller_set_builder_screen = ControllerCollectionBuildScreen(name='Controller Collection Builder')
        self.screen_manager.add_widget(self.controller_set_builder_screen)

        self.controller_screen = ControllerScreen(name='Controller')
        self.screen_manager.add_widget(self.controller_screen)

        self.screen_manager.current = 'Controller Collections'

        self.screen_manager.last_screen = self.screen_manager.current

        return self.screen_manager

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = [400, 600]
            win.size = [400, 600]


# this file should be renamed to main.py when copy to android for Kivy laucher
if '__main__' == __name__:
    Common.logger.logger.set_logger('kivy')
    # start application
    ClientUI().run()
