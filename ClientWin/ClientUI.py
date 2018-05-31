from Common.KivyImporter import *

Builder.load_string('''
<ControllerSetScreen>:
    controller_set_scrollview: controller_set_scrollview
    controller_set_container: controller_set_container
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
                on_release: root._goto_screen('Controller Set Builder')
            Widget:
                size_hint_max_x: 30
        Widget:
            size_hint_max_y: 10
        ScrollView:
            id: controller_set_scrollview
            do_scroll_x: False
            size: self.size
            size_hint: 1, 1
            GridLayout:
                id: controller_set_container
                cols: 1
                padding: 20
                spacing: 10
                size_hint: 1, None  # this will make this not in control of its parent
                height: 180
                Button:
                    text: 'test'
                    size_hint: 1, None
                    height: 150
                    on_release: root._goto_screen('Controller')
<ControllerScreen>:
    Button:
        text: 'controller'
<ControllerSetBuildScreen>:
    Button:
        text: 'building'
''')



class ControllerSetScreen(Screen): # gallery of controller sets

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

    def _goto_screen(self, screen):
        self.manager.current = screen

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

class ControllerSetBuildScreen(Screen):


    pass

class ClientUI(App):

    def build(self):
        self.screen_manager = ScreenManager()

        self.controller_set_screen = ControllerSetScreen(name='Controller Set')
        self.screen_manager.add_widget(self.controller_set_screen)

        self.controller_set_builder_screen = ControllerSetBuildScreen(name='Controller Set Builder')
        self.screen_manager.add_widget(self.controller_set_builder_screen)

        self.controller_screen = ControllerScreen(name='Controller')
        self.screen_manager.add_widget(self.controller_screen)

        self.screen_manager.current = 'Controller Set'
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