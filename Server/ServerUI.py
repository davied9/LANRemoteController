# -*-coding:utf-8-*-
from __future__ import print_function
from multiprocessing import Process, Pool, Manager
from Common.KivyImporter import *


def print_hello():
    print('hello')


def print_hello_from(obj):
    print('hello from', obj)


class LRCCodeUI(App):

    code_bit_size = 4

    def __init__(self, sync_state):
        App.__init__(self)
        self.sync_state = sync_state
        if self.sync_state is None:
            print('sync_state needed for LRCCodeUI')

    def build(self):
        import random
        self.code = random.randint(10**(LRCCodeUI.code_bit_size-1), 10**LRCCodeUI.code_bit_size-1)
        return Button(text=str(self.code), on_press=self.close_this)

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.size = [130, 60]

    def close_this(self, button):
        print(self.sync_state)

        print('closing Code UI')
        self.sync_state.remove('code UI on')

        print(self.sync_state)

        self.stop()


def load_code_ui(sync_state):
    LRCCodeUI(sync_state=sync_state).run()

class LRCServerUI(App):

    def build(self):
        self.root = BoxLayout(orientation='vertical', pos_hint={'top': 1, 'x': 0}, size_hint_min=[800, 600])
        # up : start/stop buttons
        up_grid = GridLayout(cols=6, padding=10, spacing=10, size_hint_max_y=100)
        self.root.add_widget(up_grid)
        up_grid.add_widget(Button(text="Start Server", size_hint_max_x=140, on_press=self.response))
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
        self.root.add_widget(Label(text='Log window', size_hint=[0.9, 0.9], pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        # sync state
        self.sync_state = Manager().list()
        return self.root

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = 800, 600

    def response(self, inst):
        print('Got ', inst)
        from multiprocessing import Process
        self.sync_state.append('code UI on')
        pr = Process(target = load_code_ui, args=(self.sync_state,))
        pr.start()

def __test001_basics():
    LRCServerUI().run()
    print('Done running')
    pass


if __name__ == '__main__':
    __test001_basics()
    pass

