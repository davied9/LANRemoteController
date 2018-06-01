from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
from Common.Exceptions import *
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


<ControllerScreen>:
    button_container: button_container
    display_title: title_label
    BoxLayout:
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
                height: 50
                spacing: 10


<ControllerCollectionBuildScreen>:
    display_title: title_input
    button_container: button_container
    FloatLayout:
        BoxLayout:
            orientation: 'vertical'
            padding: 30, 30
            Label:
                id: title_input
                text: 'Builder'
                size_hint_max_y: 80
                font_size: 43
            ScrollView:
                do_scroll_x: False
                GridLayout:
                    id: button_container
                    cols: 1
                    size_hint: 1, None
                    height: 50
                    spacing: 10
            BoxLayout:
                size_hint_max_y: 50
                padding: 10, 0
                Button:
                    text: 'Back'
                    size_hint_max_x: 50
                    on_release: root._go_back_last_screen(self)
                Widget:
                Button:
                    text: 'Save'
                    size_hint_max_x: 50
                    on_release: root._save_controller_set(self)
                Widget:
                Button:
                    text: 'Add'
                    size_hint_max_x: 50
                    on_release: root._add_new_button(self)
        TextInput:
            multiline: False
            size_hint: 0.5, 0.1
''')


class Controller(object):

    def __init__(self, name, *args):
        self.name = name
        self.buttons = []
        for key in args:
            self.buttons.append(key)

    def serialize_instance(self):
        return {self.name:self.buttons}


class ControllerSet(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.controllers = {}
        print('    {0}'.format(self.name))
        for name, config in kwargs.items():
            print('        {0} : {1}'.format(name, config))
            self.controllers[name] = (Controller(name, *config))

        # print('re-dump : {0}'.format(json.dumps(self, default=self.serialize_instance)))

    @staticmethod
    def serialize_instance(inst):
        controllers = {}
        for controller in inst.controllers:
            controllers.update( controller.serialize_instance() )
        return {inst.name:controllers}


class ControllerCollectionScreen(Screen): # gallery of controller sets

    def test_fun(self, *args):
        print('test ', *args)

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.index = 0

    def on_pre_enter(self, *args):
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
                    info = json.load(file_handle)
                    for name, config in info.items():
                        controller_sets[name] = ControllerSet(name, **config)
            break

        App.get_running_app().controller_sets = controller_sets

        return controller_sets

    def _reset_controller_set_container(self):
        self.controller_set_container.clear_widgets()
        self.controller_set_container.height = 50

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


    pass


class ControllerScreen(Screen): # controller operation room

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
        self.button_container.add_widget(Button(
                text=controller.name,
                size_hint=(1, None),
                height=50
            ))
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


class ControllerCollectionBuildScreen(Screen): # controller collection builder

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()
        if current_app.current_edit_set:
            self.display_title.text = current_app.current_edit_set
            self.is_new = False
        else:
            self.display_title.text = 'New'
            self.is_new = True

        self._reset_controller_set_container()
        if not self.is_new:
            for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
                self._add_controller_button(controller)

    def _reset_controller_set_container(self):
        self.button_container.clear_widgets()
        self.button_container.height = 50

    def _add_controller_button(self, controller):
        self.button_container.add_widget(Button(
                text=controller.name,
                size_hint=(1, None),
                height=50
            ))
        self.button_container.height += 60

    def _save_controller_set(self, button): # save this build to a controller set file
        pass

    def _add_new_button(self, button): #
        pass

    def _go_back_last_screen(self, button):
        App.get_running_app().current_edit_set = self.display_title.text

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen


class ClientUI(App):

    def build(self):
        print('working directory : {0}'.format( os.getcwd() ))

        self.screen_manager = ScreenManager(transition=RiseInTransition())

        self.controller_set_screen = ControllerCollectionScreen(name='Controller Collections')
        self.screen_manager.add_widget(self.controller_set_screen)

        self.controller_set_builder_screen = ControllerCollectionBuildScreen(name='Controller Collection Builder')
        self.screen_manager.add_widget(self.controller_set_builder_screen)

        self.controller_screen = ControllerScreen(name='Controller')
        self.screen_manager.add_widget(self.controller_screen)

        self.screen_manager.current = 'Controller Collections'

        self.screen_manager.last_screen = self.screen_manager.current
        self.current_edit_set = None

        return self.screen_manager

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = [400, 600]
            win.size = [400, 600]

    def on_test(self, inst):
        pass

def __test000():
    ClientUI().run()

if '__main__' == __name__:
    __test000()