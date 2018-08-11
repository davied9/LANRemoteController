from Common.KivyImporter import *
from kivy.clock import Clock
from kivy.logger import Logger
from Common.Exceptions import *
from ClientWin.LRCClientConnector import LRCClientConnector
from Controller.LRCController import Controller, ControllerSet, ControllerPackage
import os, json


Builder.load_string('''
<ControllerCollectionScreen>:
    # configuratins
    button_height: 50
    button_spacing: 10
    # widgets
    background_layout: background_layout
    controller_set_scrollview: controller_set_scrollview
    controller_set_container: controller_set_container
    display_title: title_label
    connector: connector
    info_label: info_label
    # layout begins
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            id: background_layout
            orientation: 'vertical'
            size_hint: 0.95, 0.95
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 0.1
                Button:
                    text: 'Reload'
                    size_hint: 0.2, 1
                    on_release: root._reload_controller_set_from_local(self)
                Label:
                    id: title_label
                    text: 'Collections'
                    font_size: 43
                Button:
                    text: 'Add'
                    size_hint: 0.2, 1
                    on_release: root._goto_builder_screen(self)
            Widget:
                size_hint: 1, 0.05
            ScrollView:
                id: controller_set_scrollview
                do_scroll_x: False
                color: 1, 1, 0, 1
                GridLayout:
                    id: controller_set_container
                    cols: 1
                    size_hint: 1, None
                    spacing: root.button_spacing
            Widget:
                size_hint: 1, 0.05
            LRCClientConnector:
                id: connector
                size_hint: 1, 0.05
            Label:
                id: info_label
                size_hint: 1, 0.05
                font_size: 12
                color: 1, 0, 0, 1

''')


class ControllerCollectionScreen(Screen): # gallery of controller sets

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.connector.ip_button.bind(on_release=self._on_ip_button_released)
        self.connector.port_button.bind(on_release=self._on_port_button_released)
        self.ip_and_port_input = None
        self.connector.ext_err_logger = self.present_info

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()
        if not current_app.controller_sets:
            self._reload_controller_set_from_local()
        else:
            self._reload_controller_set_from_app()
        if current_app.client.server_address:
            self.connector.ip_button.text   = current_app.client.server_address[0]
            self.connector.port_button.text = str(current_app.client.server_address[1])

    def on_leave(self, *args):
        self._reset_controller_set_container()

    def _compute_button_size(self):
        self.button_height = 0.2 * self.controller_set_scrollview.height
        self.button_spacing = 0.05 * self.button_height

    def _reload_controller_set_from_app(self, *args):
        self._compute_button_size()
        for name, _set in App.get_running_app().controller_sets.items():
            self._add_controller_set_button(_set)

    def _reload_controller_set_from_local(self, *args):
        self._compute_button_size()
        self._reset_controller_set_container()
        for _set in self._load_controller_set_from_local().values():
            self._add_controller_set_button(_set)

    def _load_controller_set_from_local(self):
        controller_sets = {}
        for r, dirs, files in os.walk('./collections'):
            for file_name in files:
                if not file_name.endswith('.json'): continue
                full_path = r+'/'+file_name
                with open(full_path) as file_handle:
                    Logger.info('Collection: loading configuration from "{0}"'.format(full_path))
                    try:
                        info = json.load(file_handle)
                        for name, config in info.items():
                            controller_sets[name] = ControllerSet(name, **config)
                    except Exception as err:
                        Logger.info('Collection:     failed with message : {0}'.format(err))
            break

        App.get_running_app().controller_sets = controller_sets

        return controller_sets

    def _reset_controller_set_container(self):
        self.controller_set_container.clear_widgets()
        self.controller_set_container.height = 1

    def _add_controller_set_button(self, controller_set):
        self.controller_set_container.add_widget(Button(
            text=controller_set.name,
            height=self.button_height,
            on_release=self._goto_controller_screen
        ))
        self.controller_set_container.height += self.button_height + self.button_spacing

    def _goto_controller_screen(self, button): # goto controller screen to operate
        App.get_running_app().current_edit_set = button.text
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller'

    def _goto_builder_screen(self, button): # add new controller
        App.get_running_app().current_edit_set = None
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller Collection Builder'

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

    def present_info(self, info, time_last=5):
        self.info_label.text = info
        self.clear_info_event = Clock.schedule_once(self._clear_info_helper, time_last)

    def _clear_info_helper(self, *args): # the argument passed maybe the position of touch
        self.info_label.text = ''
        self.clear_info_event = None
