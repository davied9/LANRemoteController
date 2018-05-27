# -*-coding:utf-8-*-
from __future__ import print_function

from Common.KivyImporter import *


class LRCServerApp(App):

    def build(self):
        return LRCServerUI()


class LRCServerUI(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.orientation = 'vertical'
        self.pos_hint = { 'top' : 1, 'x' : 0 }
        self.size_hint_min = [800,600]
        # up : start/stop buttons
        up_grid = GridLayout(cols=6, padding=10, spacing=10, size_hint_max_y=100)
        self.add_widget(up_grid)
        up_grid.add_widget(Button(text="Start Server", size_hint_max_x=140))
        up_grid.add_widget(Label(text="IP", size_hint_max_x=40))
        up_grid.add_widget(TextInput(text='text default', size_hint_max_x=140))
        up_grid.add_widget(Label(text="Port", size_hint_max_x=60))
        up_grid.add_widget(TextInput(text='text default', size_hint_max_x=140))
        up_grid.add_widget(Label())
        up_grid.add_widget(Button(text="Start Waiter"))
        up_grid.add_widget(Label(text="IP"))
        up_grid.add_widget(TextInput(text='text default'))
        up_grid.add_widget(Label(text="Port"))
        up_grid.add_widget(TextInput(text='text default'))
        up_grid.add_widget(Label())
        # down : log window
        #down_box = BoxLayout()
        self.add_widget(Label(text='Log window', size_hint=[0.9,0.9], pos_hint={'center_x':0.5, 'center_y':0.5}))
        #down_box.add_widget(Label(text='Log window'))


def __test001_basics():
    LRCServerApp().run()
    pass


if __name__ == '__main__':
    __test001_basics()
    pass

