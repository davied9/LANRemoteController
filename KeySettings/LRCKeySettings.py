from PyUserInput import PyKeyboard

class KeySettings(object):
    '''Key Settings for LAN Remote Controller

    components:


    '''


    def __int__(self):
        keyboard = PyKeyboard()

        self.allowed_functional_keys = [
            'ctrl',  'left ctrl',  'right ctrl',
            'shift', 'left shift', 'right shift',
            'alt',   'left alt',    'right alt',
        ]

        self.allowed_special_keys = [
            'left arrow', 'right arrow', 'up arrow', 'down arrow',
            'space',
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
            # special key
            'left arrow':   keyboard.left_key,
            'right arrow':  keyboard.right_key,
            'up arrow':     keyboard.up_key,
            'down arrow':   keyboard.down_key,
            # other
            'space':        keyboard.space_key,
        }

        self.mutex_keys = [
            ['ctrl',  'left ctrl',  'right ctrl', ], # control
            ['shift', 'left shift', 'right shift',], # shift
            ['alt',   'left alt',    'right alt',  ], # alt
        ]



