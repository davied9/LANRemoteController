from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.logger import Logger
from time import sleep
import re

Builder.load_string('''
<LRCClientConnector>:
    size_hint_max_y: 30
    ip_label: ip_label
    ip_input: ip_input
    port_label: port_label
    port_input: port_input
    Widget:
    Button:
        text: 'Connect'
        size_hint: None, 1
        width: 70
        on_release: root.on_connect_released(self)
    Label:
        id: ip_label
        text: 'IP'
        size_hint: None, 1
        width: 30
    TextInput:
        id: ip_input
        text: '127.0.0.1'
        size_hint: None, 1
        width: 90
        #background_color: [0, 0, 0, 0]
    Label:
        id: port_label
        text: 'Port'
        size_hint: None, 1
        width: 50
    TextInput:
        id: port_input
        text: '35530'
        size_hint: None, 1
        width: 90
        #background_color: [0, 0, 0, 0]
    Widget:
''')


class LRCClientConnector(BoxLayout):

    def __init__(self, **kwargs):
        self.client = App.get_running_app().client
        BoxLayout.__init__(self, **kwargs)
        self.ip_matcher = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')

    def execute_controller(self, controller):
        sleep(3)
        for _, comb in controller.dump().items():
            combination = comb
        self.client.send_combinations(*combination)

    # as callback for "Connect" button
    def on_connect_released(self, button):
        try:
            ip = self.parse_ip(self.ip_input.text)
            port = self.parse_port(self.port_input.text)
            server_address = (ip, port)
        except ValueError as err:
            server_address = None
            Logger.info('Connector: start server failed, unable to parse ip or port : {0}'.format(err.args))
        if server_address:
            try:
                self.connect(server_address)
            except Exception as err:
                Logger.info('Connector: try to connect to {0} failed: {1}'.format(server_address, err.args))

    def connect(self, server_address):
        self.client.connect(server_address)

    def parse_ip(self, str):
        if '' == str or 'localhost' == str:
            str = '127.0.0.1'
        else:
            vols, = self.ip_matcher.findall(str)
            if len(vols) != 4:
                raise ValueError('ip not correct, must be "xxx.xxx.xxx.xxx", "xxx" should between [0,255]')
            ip_list = []
            for vol in vols:
                val = int(vol)
                if val < 0 or val > 255:
                    raise ValueError('ip should be between [0,255], found %d' % val)
                ip_list.append(vol)
                ip_list.append('.')
            str = ''.join(ip_list[:-1])
        return str

    def parse_port(self, str):
        port = int(str)
        if port > 10000 and port < 49999:
            return port
        else:
            raise ValueError('port should between (10000, 49999)')
