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
        self.connector.ip_button.bind(on_release=self._on_ip_button_released)
        self.connector.port_button.bind(on_release=self._on_port_button_released)
        self.ip_and_port_input = None

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

    # ip_or_port = 'ip' or 'port'
    def _open_ip_port_input(self, button, ip_or_port):
        if not self.ip_and_port_input:
            self.ip_and_port_input = TextInput(text=button.text, size_hint_max_y=30)
            self.ip_and_port_input.bind(focused=self._on_ip_or_port_input_focused)
            self.background_layout.add_widget(self.ip_and_port_input, 999)

        if 'ip' == ip_or_port:
            self.ip_and_port_input.sync_button = self.connector.ip_button
        else:
            self.ip_and_port_input.sync_button = self.connector.port_button

        self.ip_and_port_input.text = self.ip_and_port_input.sync_button.text

    # as callback for ip_button
    def _on_ip_button_released(self, button):
        self._open_ip_port_input(button, 'ip')

    # as callback for port_button
    def _on_port_button_released(self, button):
        self._open_ip_port_input(button, 'port')

    # as callback for ip or port input
    def _on_ip_or_port_input_focused(self, input, focused):
        if focused:
            input.select_all()
        else:
            input.sync_button.text = input.text
            self.background_layout.remove_widget(input)
            self.ip_and_port_input = None

