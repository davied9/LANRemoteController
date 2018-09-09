import kivy
kivy.require('1.10.1')

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from LRC.Common.logger import logger
from LRC.Client.ControllerCollectionScreen import ControllerCollectionScreen
from LRC.Client.ControllerCollectionBuildScreen import ControllerCollectionBuildScreen
from LRC.Client.ControllerScreen import ControllerScreen
from LRC.Client.LRCClient import LRCClient

# from kivy.uix.screenmanager import SwapTransition
# from kivy.uix.screenmanager import ShaderTransition
# from kivy.uix.screenmanager import SlideTransition
# from kivy.uix.screenmanager import WipeTransition
# from kivy.uix.screenmanager import FadeTransition
# from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.screenmanager import RiseInTransition


class ClientUI(App):
    '''Client Graphic User Interface

    components:
        screen_manager:                 screen manager
        screen_manager.last_screen:     last screen
        controller_sets:                all controller collections loaded from local files
        current_edit_set:               current edited controller set
        client:                         client ( LRCClient ), provide access for LRCClient

    '''

    def build(self):
        logger.info('Start: working directory : {0}'.format( os.getcwd() ))

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


# this file should be renamed to main.py when copy to android for Kivy laucher
if '__main__' == __name__:
    import Common.logger
    Common.logger.logger.set_logger('kivy')
    # start application
    ClientUI().run()