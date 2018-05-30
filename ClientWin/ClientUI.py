from Common.KivyImporter import *

Builder.load_string('''
<ControlSetScreen>:
    controller_container: controller_container
    size_hint_min: 400, 600
    BoxLayout:
        orientation: 'vertical'
        Widget:
            size_hint_max_y: 30
        BoxLayout:
            orientation: 'horizontal'
            size_hint_max_y: 50
            Widget:
            Button:
                text: 'Add'
                size_hint_max: 50, 50
                on_release: root._add_control_set()
            Widget:
                size_hint_max_x: 30
        Widget:
            size_hint_max_y: 10
        BoxLayout:
            id: controller_container
            orientation: 'vertical'
            padding: 20
            spacing: 10
            Button:
                text: 'test'
<ControllerScreen>:
    Button:
        text: 'controller'
<ControllerSetBuildScreen>:
    Button:
        text: 'building'
''')


class ControlSetScreen(Screen): # gallery of controller sets

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)


    def _add_control_set(self):
        self.controller_container.add_widget(Button(text='joker'))

    pass


class ControllerScreen(Screen): # controller operation room

    pass

class ControllerSetBuildScreen(Screen):
    pass

class ClientUI(App):

    def build(self):
        self.screen_manager = ScreenManager()
        self.control_set_screen = ControlSetScreen(name='Set')
        self.screen_manager.add_widget(self.control_set_screen)
        self.screen_manager.current = 'Set'
        return self.screen_manager

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = [400, 600]

    def on_test(self, inst):
        pass

def __test000():
    ClientUI().run()

if '__main__' == __name__:
    __test000()