# -*-coding:utf-8-*-
from __future__ import print_function
from Common.KivyImporter import *
from multiprocessing import Process
from threading import Thread
from random import randint
from time import sleep

def start_LRCServer(server_address, waiter_address):
    from LRCServer import LRCServer
    LRCServer(server_address, waiter_address).serve_forever()


def start_LRCWaiter(server_address):
    from LRCServer import LRCWaiter
    LRCWaiter(server_address).serve_forever()


class LRCServerUI(App):

    def build(self):
        self.root = BoxLayout(orientation='vertical', pos_hint={'top': 1, 'x': 0}, size_hint_min=[800, 600])
        # up : start/stop buttons
        up_grid = GridLayout(cols=6, padding=10, spacing=10, size_hint_max_y=100)
        self.root.add_widget(up_grid)
        self.server_button      = Button(text="Start Server", size_hint_max_x=140, on_press=self.on_start_server_pressed)
        self.server_info_label  = Label()
        self.server_ip_input    = TextInput(text='text default', size_hint_max_x=140)
        self.server_port_input  = TextInput(text='text default', size_hint_max_x=140)
        self.waiter_button      = Button(text="Start Waiter", on_press=self.on_start_waiter_pressed)
        self.waiter_info_label  = Label()
        self.waiter_ip_input    = TextInput(text='text default')
        self.waiter_port_input  = TextInput(text='text default')
        up_grid.add_widget(self.server_button)
        up_grid.add_widget(Label(text="IP", size_hint_max_x=40))
        up_grid.add_widget(self.server_ip_input)
        up_grid.add_widget(Label(text="Port", size_hint_max_x=60))
        up_grid.add_widget(self.server_port_input)
        up_grid.add_widget(self.server_info_label)
        up_grid.add_widget(self.waiter_button)
        up_grid.add_widget(Label(text="IP"))
        up_grid.add_widget(self.waiter_ip_input)
        up_grid.add_widget(Label(text="Port"))
        up_grid.add_widget(self.waiter_port_input)
        up_grid.add_widget(self.waiter_info_label)
        # down : log window
        self.root.add_widget(Label(text='Log window', size_hint=[0.9, 0.9], pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        return self.root

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = 800, 600
        # servers
        self.server_address = ('127.0.0.1', 35530)
        self.server_process = None
        self.waiter_address = ('127.0.0.1', 35527)
        self.waiter_process = None
        self.watch_interval = 0.5

    def start_server(self):
        self.server_process = Process(target=start_LRCServer, args=(self.server_address, self.waiter_address))
        print('start server at :', self.server_address)
        self.server_process.start()
        self.server_button.text = 'Close Server'
        self.server_info_label.text = 'code : ' + str(randint(1000, 9999)) + ', running ...'
        self.server_ip_input.disabled = True
        self.server_port_input.disabled = True
        Thread(target=self.server_watcher).start()

    def stop_server(self):
        print('terminate server ')
        self.server_process.terminate()
        self.server_process = None
        self.server_button.text = 'Start Server'
        self.server_info_label.text = ''
        self.server_ip_input.disabled = False
        self.server_port_input.disabled = False

    def start_waiter(self):
        self.waiter_process = Process(target=start_LRCWaiter, args=(self.waiter_address, ))
        print('start waiter at :', self.waiter_address)
        self.waiter_process.start()
        self.waiter_button.text = 'Close Waiter'
        self.waiter_info_label.text = 'running ...'
        self.waiter_ip_input.disabled = True
        self.waiter_port_input.disabled = True
        Thread(target=self.waiter_watcher).start()

    def stop_waiter(self):
        print('terminate waiter ')
        self.waiter_process.terminate()
        self.waiter_process = None
        self.waiter_button.text = 'Start Waiter'
        self.waiter_info_label.text = ''
        self.waiter_ip_input.disabled = False
        self.waiter_port_input.disabled = False

    def server_watcher(self):
        while True:
            if not self.server_process:
                break
            if not self.server_process.is_alive():
                break
            sleep(self.watch_interval)
        self.stop_server()

    def waiter_watcher(self):
        while True:
            if not self.waiter_process:
                break
            if not self.waiter_process.is_alive():
                break
            sleep(self.watch_interval)
        self.stop_waiter()

    def on_start_server_pressed(self, inst):
        if self.server_process: # process is running, close it
            self.stop_server()
        else: # start new server
            self.start_server()

    def on_start_waiter_pressed(self, inst):
        if self.waiter_process: # process is running, close it
            self.stop_waiter()
        else: # start new waiter
            self.start_waiter()



def __test001_basics():
    LRCServerUI().run()
    print('Done running')
    pass


if __name__ == '__main__':
    __test001_basics()
    pass

