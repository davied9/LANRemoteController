from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from Common.Exceptions import *
from Controller.LRCController import Controller, ControllerSet, ControllerPackage
import os, json
from ControllerCollectionScreen import ControllerCollectionScreen
from ControllerCollectionBuildScreen import ControllerCollectionBuildScreen
from ControllerScreen import ControllerScreen


class ClientUI(App):
    '''Client Graphic User Interface

    components:
        screen_manager:                 screen manager
        screen_manager.last_screen:     last screen
        controller_sets:                all controller collections loaded from local files
        current_edit_set:               current edited controller set

    '''

    def build(self):
        print('working directory : {0}'.format( os.getcwd() ))

        self.controller_sets = None
        self.current_edit_set = None # for sync between build screen and controller screen
        self.LRCClient = None

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


def __test000():
    ClientUI().run()

if '__main__' == __name__:
    __test000()