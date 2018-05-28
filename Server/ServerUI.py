# -*-coding:utf-8-*-
from __future__ import print_function

from Common.KivyImporter import *

class LRCServerUI(App):

    def build(self):
        self.main = BoxLayout(orientation='vertical', pos_hint={'top': 1, 'x': 0}, size_hint_min=[800, 600])
        # up : start/stop buttons
        up_grid = GridLayout(cols=6, padding=10, spacing=10, size_hint_max_y=100)
        self.main.add_widget(up_grid)
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
        self.main.add_widget(Label(text='Log window', size_hint=[0.9, 0.9], pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        return self.main


def __test001_basics():
    LRCServerUI().run()
    pass


if __name__ == '__main__':
    __test001_basics()
    pass

