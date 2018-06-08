from kivy.properties import ObjectProperty
from Exceptions import ArgumentError
from Controller.LRCKeySettings import KeySettings

class AlternateKey(object):

    def __init__(self, enable, is_left=True):
        self.enable = enable # True or False
        self.is_left = is_left # True or False


class Controller(object):
    '''Controller for a key combination

    components:
        name:       Name of this combination
        ctrl:       Information of control key
        shift:      Information of shift key
        alt:        Information of alt key
        key:        The key to press for this Control

    '''

    settings = KeySettings()

    class UnsupportedKeyForControllerError(Exception):

        def __init__(self, key, info=None):
            self.key = key
            self.info = info

        def __str__(self):
            if self.info:
                return 'un-supported key "{0}" for Controller : {1}.'.format(self.key, self.info)
            else:
                return 'un-supported key "{0}" for Controller.'.format(self.key)

    def __init__(self, name, *args):
        self.name  = name

        self.ctrl  = AlternateKey(enable=False, is_left=True)
        self.shift = AlternateKey(enable=False, is_left=True)
        self.alt   = AlternateKey(enable=False, is_left=True)

        buffer = []
        for val in args:
            buffer.append(val)

        for ctrl_tag in Controller.settings.ctrl_keys:
            if ctrl_tag in buffer:
                self.ctrl.enable = True
                self.ctrl.is_left = False if 'right' in ctrl_tag else True
                buffer.remove(ctrl_tag)

        for shift_tag in Controller.settings.shift_keys:
            if shift_tag in buffer:
                self.shift.enable = True
                self.shift.is_left = False if 'right' in shift_tag else True
                buffer.remove(shift_tag)

        for alt_tag in Controller.settings.alt_keys:
            if alt_tag in buffer:
                self.alt.enable = True
                self.alt.is_left = False if 'right' in alt_tag else True
                buffer.remove(alt_tag)

        n_left = len(buffer)
        if 1 == n_left:
            key = buffer[0]
            Controller.validate_key(key)
            self.key = key
        else: # 0 == n_left or n_left > 1
            raise ArgumentError('un-recongnized key in given keys for a Control (one special key or letter key should be provided) : {0}'.format(args) )

    def __str__(self):
        return '{0}'.format(Controller.serialize_instance(self))

    @staticmethod
    def serialize_instance(inst):
        buttons = []
        if inst.ctrl.enable:
            if inst.ctrl.is_left:
                buttons.append(Controller.settings.ctrl_keys[1])
            else:
                buttons.append(Controller.settings.ctrl_keys[2])
        if inst.shift.enable:
            if inst.shift.is_left:
                buttons.append(Controller.settings.shift_keys[1])
            else:
                buttons.append(Controller.settings.shift_keys[2])
        if inst.alt.enable:
            if inst.alt.is_left:
                buttons.append(Controller.settings.alt_keys[1])
            else:
                buttons.append(Controller.settings.alt_keys[2])
        buttons.append(inst.key)
        return { inst.name : buttons }

    @staticmethod
    def validate_key(key):
        N = len(key)
        if key in Controller.settings.allowed_special_keys:
            return
        elif 1 == N: # letter or number
            if key.isalnum():
                return
            else:
                raise Controller.UnsupportedKeyForControllerError(key, 'expecting a letter or a number string length of 1 as a key')
        else:
            raise Controller.UnsupportedKeyForControllerError(key, 'un-supported special key')

    def available(self):
        if self.key:
            return True
        else:
            return False


class ControllerSet(object):
    '''Controller Collection(Use set as short for collection)

    components:
        name:           Name of this controller collection
        controllers:    Controllers(Controller) of this collection

    '''

    def __init__(self, name, **kwargs):
        self.name = name
        self.controllers = {}
        print('    {0}'.format(self.name))
        for name, config in kwargs.items():
            print('        {0} : {1}'.format(name, config))
            self.controllers[name] = (Controller(name, *config))
        # print('re-dump : {0}'.format(json.dumps(self, default=self.serialize_instance)))

    @staticmethod
    def serialize_instance(inst):
        controllers = {}
        for controller in inst.controllers:
            controllers.update( Controller.serialize_instance(controller) )
        return { inst.name : controllers }


class ControllerPackage(object):
    '''Controller Package : a collection of controller collection

    '''

    def __int__(self):
        pass
