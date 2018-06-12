from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from Common.Exceptions import *
from Controller.LRCController import Controller, ControllerSet, ControllerPackage
import os, json


Builder.load_string('''
<ControllerScreen>:
    background_layout: background_layout
    button_container: button_container
    display_title: title_label
    connector: connector
    BoxLayout:
        id: background_layout
        orientation: 'vertical'
        padding: 30, 30
        BoxLayout:
            size_hint_max_y: 50
            Button:
                text: 'Back'
                size_hint_max_x: 50
                on_release: root._go_back_last_screen(self)
            Label:
                id: title_label
                text: 'Default'
                font_size: 43
            Button:
                text: 'Edit'
                size_hint_max_x: 50
                on_release: root._goto_builder_screen(self)
        Widget:
            size_hint_max_y: 30
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: button_container
                cols: 1
                size_hint: 1, None
                height: 1
                spacing: 10
        LRCClientConnector:
            id: connector
''')


class ControllerScreen(Screen): # controller operation room

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()

        self._reset_button_container()
        for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
            self._add_controller_button(controller)

        self.display_title.text = current_app.current_edit_set

    def _reset_button_container(self):
        self.button_container.clear_widgets()
        self.button_container.height = 50

    def _add_controller_button(self, controller):
        button = Button(
                text=controller.name,
                size_hint=(1, None),
                height=50,
                on_release=self._on_controller_button_released
            )
        button.controller = controller
        self.button_container.add_widget(button)
        self.button_container.height += 60

    def _go_back_last_screen(self, button):
        App.get_running_app().current_edit_set = self.display_title.text

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen

    def _goto_builder_screen(self, button): # Edit current controller collection
        App.get_running_app().current_edit_set = self.display_title.text
        self.manager.last_screen = "Controller"
        self.manager.current = 'Controller Collection Builder'

    def _on_controller_button_released(self, button):
        self._execute_controller(button.controller)

    def _execute_controller(self, controller):
        self.connector.execute_controller(controller)

