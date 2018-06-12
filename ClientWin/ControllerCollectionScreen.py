from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from Common.Exceptions import *
from Controller.LRCController import Controller, ControllerSet, ControllerPackage
import os, json

Builder.load_string('''
<ControllerCollectionScreen>:
    controller_set_scrollview: controller_set_scrollview
    controller_set_container: controller_set_container
    display_title: title_label
    size_hint_min: 400, 600
    BoxLayout:
        orientation: 'vertical'
        padding: 30, 30
        BoxLayout:
            orientation: 'horizontal'
            size_hint_max_y: 50
            Button:
                text: 'Reload'
                size_hint_max: 50, 50
                on_release: root._reload_controller_set_from_local(self)
            Label:
                id: title_label
                text: 'Collections'
                font_size: 43
            Button:
                text: 'Add'
                size_hint_max: 50, 50
                on_release: root._goto_builder_screen(self)
        Widget:
            size_hint_max_y: 30
        ScrollView:
            id: controller_set_scrollview
            do_scroll_x: False
            GridLayout:
                id: controller_set_container
                cols: 1
                spacing: 10
                size_hint: 1, None  # this will make this not in control of its parent
                height: 50

''')


class ControllerCollectionScreen(Screen): # gallery of controller sets

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        if not App.get_running_app().controller_sets:
            self._reload_controller_set_from_local()
        else:
            self._reload_controller_set_from_app()

    def on_leave(self, *args):
        self._reset_controller_set_container()

    def _reload_controller_set_from_app(self, *args):
        for name, _set in App.get_running_app().controller_sets.items():
            self._add_controller_set_button(_set)

    def _reload_controller_set_from_local(self, *args):
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
                    print('loading configuration from "{0}"'.format(full_path))
                    try:
                        info = json.load(file_handle)
                        for name, config in info.items():
                            controller_sets[name] = ControllerSet(name, **config)
                    except Exception as err:
                        print('    failed with message : {0}'.format(err))
            break

        App.get_running_app().controller_sets = controller_sets

        return controller_sets

    def _reset_controller_set_container(self):
        self.controller_set_container.clear_widgets()
        self.controller_set_container.height = 1

    def _add_controller_set_button(self, controller_set):
        self.controller_set_container.add_widget(Button(
            text=controller_set.name,
            size_hint=(1,None),
            height=50,
            on_release=self._goto_controller_screen
        ))
        self.controller_set_container.height += 60

    def _goto_controller_screen(self, button): # goto controller screen to operate
        App.get_running_app().current_edit_set = button.text
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller'

    def _goto_builder_screen(self, button): # add new controller
        App.get_running_app().current_edit_set = None
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller Collection Builder'
