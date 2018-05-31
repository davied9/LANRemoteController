from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition


Builder.load_string('''
<ControllerCollectionScreen>:
    controller_set_scrollview: controller_set_scrollview
    controller_set_container: controller_set_container
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
                on_release: root.manager.current = 'Controller Collection Builder'
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
                height: 180
                Button:
                    text: 'test'
                    size_hint: 1, None
                    height: 150
                    on_release: root.manager.current = 'Controller'


<ControllerScreen>:
    button_container: button_container
    title_label: title_label
    BoxLayout:
        orientation: 'vertical'
        padding: 30, 30
        BoxLayout:
            size_hint_max_y: 50
            Button:
                text: 'Back'
                size_hint_max_x: 50
                on_release: root.manager.current = 'Controller Collections'
            Label:
                id: title_label
                text: 'Default'
                font_size: 43
            Button:
                text: 'Edit'
                size_hint_max_x: 50
                on_release: root.manager.current = 'Controller Collection Builder'
        Widget:
            size_hint_max_y: 30
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: button_container
                cols: 1
                size_hint: 1, None
                height: 80
                Button:
                    text: 'controller'


<ControllerCollectionBuildScreen>:
    display_title: title_label
    button_container: button_container
    BoxLayout:
        orientation: 'vertical'
        padding: 30, 30
        Label:
            id: title_label
            text: 'Builder'
            size_hint_max_y: 80
            font_size: 43
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: button_container
                cols: 1
                size_hint: 1, None
                height: 80
                Button:
                    text: 'new'
        BoxLayout:
            size_hint_max_y: 50
            padding: 10, 0
            Button:
                text: 'Back'
                size_hint_max_x: 50
                on_release: root.manager.current = 'Controller Collections'
            Widget:
            Button:
                text: 'Save'
                size_hint_max_x: 50
                on_release:
            Widget:
            Button:
                text: 'Add'
                size_hint_max_x: 50
''')



class ControllerCollectionScreen(Screen): # gallery of controller sets

    def test_fun(self, *args):
        print('test ', *args)

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.index = 0

    def on_start(self):
        pass

    def on_pre_enter(self, *args):
        for _set in self._load_controller_set_from_local():
            self._add_controller_set_button()
        pass

    def _load_controller_set_from_local(self):
        return []

    def _add_controller_set_button(self):
        pass

    def _add_control_set(self):
        self.controller_set_container.add_widget(Button(text='joker {0}'.format(self.index), size_hint=(1,None), height=50))
        self.controller_set_container.height += (50 + self.controller_set_container.spacing[-1])
        self.index += 1
        print('pressed {0} times :'.format(self.index))
        self._print_scroll_view_content()

    def _print_scroll_view_content(self):
        print('    scroll view :')
        print('        pos {0}, size {1}'.format(self.controller_set_scrollview.pos, self.controller_set_scrollview.size))
        print('    container :')
        print('        pos {0}, size {1}'.format(self.controller_set_container.pos, self.controller_set_container.size))
        print('    children buttons :')
        for ix in range(len(self.controller_set_container.children)):
            print('        {0} :'.format(ix))
            print('            pos {0}, size {1}'.format(self.controller_set_container.children[ix].pos, self.controller_set_container.children[ix].size))


    pass


class ControllerScreen(Screen): # controller operation room

    pass

class ControllerCollectionBuildScreen(Screen):

    pass

class ClientUI(App):

    def build(self):
        self.screen_manager = ScreenManager(transition=RiseInTransition())

        self.controller_set_screen = ControllerCollectionScreen(name='Controller Collections')
        self.screen_manager.add_widget(self.controller_set_screen)

        self.controller_set_builder_screen = ControllerCollectionBuildScreen(name='Controller Collection Builder')
        self.screen_manager.add_widget(self.controller_set_builder_screen)

        self.controller_screen = ControllerScreen(name='Controller')
        self.screen_manager.add_widget(self.controller_screen)

        self.screen_manager.current = 'Controller Collections'
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