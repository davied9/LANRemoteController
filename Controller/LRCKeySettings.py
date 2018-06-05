from PyUserInput import PyKeyboard
from LRCController import Controller
from Exceptions import ArgumentError

class KeyCombinationNotAvailableError(ArgumentError):

    def __init__(self, *args):
        self.keys = []
        for k in args:
            self.keys.append(k)

    def __str__(self):
        n = len(self.keys)
        if 0 == n:
            return ('Key combination not available : no key found')
        elif 1 == n:
            return ('Key combination not available : {0}'.format(self.keys[0]))
        elif 2 == n:
            return ('Key combination not available : {0}, {1}'.format(self.keys[0], self.keys[1]))
        elif 3 == n:
            return ('Key combination not available : {0}, {1}, {2}'.format(self.keys[0], self.keys[1], self.keys[2] ))
        else:
            return ('Key combination not available : {0}, {1}, {2}, ...'.format(self.keys[0], self.keys[1], self.keys[2] ))


class KeySetting(object):
    '''Key Settings for LAN Remote Controller

    components:
        allowed_functional_keys:
        allowed_special_keys:
        key_map:
    '''

    def __init__(self):

        import sys

        if sys.platform.startswith('java'):
            raise NotImplementedError()
            # from .java_ import PyKeyboard
        elif sys.platform == 'darwin':
            raise NotImplementedError()
            # from .mac import PyKeyboard, PyKeyboardEvent
        elif sys.platform == 'win32':
            self._init_windows_setting()
        else:
            raise NotImplementedError()
            # from .x11 import PyKeyboard, PyKeyboardEvent

    def _init_windows_setting(self):
        keyboard = PyKeyboard()

        self.allowed_functional_keys = [
            'ctrl',  'left ctrl',  'right ctrl',
            'shift', 'left shift', 'right shift',
            'alt',   'left alt',    'right alt',
        ]

        self.allowed_special_keys = [
            'left arrow', 'right arrow', 'up arrow', 'down arrow',
            'space', 'home', 'end',
        ]

        self.key_map = {
            # functional key
            'ctrl':          keyboard.control_l_key,
            'left ctrl':    keyboard.control_l_key,
            'right ctrl':   keyboard.control_r_key,
            'alt':           keyboard.alt_l_key,
            'left alt':      keyboard.alt_l_key,
            'right alt':     keyboard.alt_r_key,
            'shift':         keyboard.shift_l_key,
            'left shift':    keyboard.shift_l_key,
            'right shift':   keyboard.shift_r_key,
            # arrow key
            'left arrow':   keyboard.left_key,
            'right arrow':  keyboard.right_key,
            'up arrow':     keyboard.up_key,
            'down arrow':   keyboard.down_key,
            # other
            'space':        keyboard.space_key,
            'home':         keyboard.home_key,
            'end':          keyboard.end_key,
        }

        self.ctrl_keys  = ['ctrl',  'left ctrl',  'right ctrl', ], # control
        self.shift_keys = ['shift', 'left shift', 'right shift',], # shift
        self.alt_keys   = ['alt',   'left alt',    'right alt',  ], # alt


    def validate_key_combination(self, combination): # raise Error if validation failed

        # mutex keys can not appear at the same time

        return


