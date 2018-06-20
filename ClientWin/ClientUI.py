from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
import os, json
from ClientWin.ControllerCollectionScreen import ControllerCollectionScreen
from ClientWin.ControllerCollectionBuildScreen import ControllerCollectionBuildScreen
from ClientWin.ControllerScreen import ControllerScreen
from ClientWin.LRCClientWin import LRCClient
from kivy.logger import Logger
import Common.logger


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