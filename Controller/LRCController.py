from kivy.properties import ObjectProperty
from Exceptions import ArgumentError

class AlternateKey(object):

    def __init__(self, enable, position='left'):
        self.enable = enable # True or False
        self.position = position # 'left' or 'right'

class Controller(object):
    '''Controller for a key combination

    components:
        name:       Name of this combination
        ctrl:       Information of control key
        shift:      Information of shift key
        alt:        Information of alt key
        key:        The key to press for this Control

    '''

    import LRCKeySettings
    setting = ObjectProperty(LRCKeySettings.KeySetting(), allownone=True)

    def __init__(self, name, *args):
        self.name  = name

        self.ctrl  = AlternateKey(False, 'left')
        self.shift = AlternateKey(False, 'left')
        self.alt   = AlternateKey(False, 'left')

        buffer = []
        for val in args:
            buffer.append(val)

        if 'ctrl' in buffer:
            self.ctrl.enable = True
            buffer.remove('ctrl')
        if 'left ctrl' in buffer:
            self.ctrl.enable = True
            buffer.remove('left ctrl')
        if 'right ctrl' in buffer:
            self.ctrl.enable = True
            self.ctrl.position = 'right'
            buffer.remove('right ctrl')

        if 'shift' in buffer:
            self.shift.enable = True
            buffer.remove('shift')
        if 'left shift' in buffer:
            self.shift.enable = True
            buffer.remove('left shift')
        if 'right shift' in buffer:
            self.shift.enable = True
            self.shift.position = 'right'
            buffer.remove('right shift')

        if 'alt' in buffer:
            self.alt.enable = True
            buffer.remove('alt')
        if 'left alt' in buffer:
            self.alt.enable = True
            buffer.remove('left alt')
        if 'right alt' in buffer:
            self.alt.enable = True
            self.alt.position = 'right'
            buffer.remove('right alt')

        n_left = len(buffer)
        if 1 == n_left:


            self.key  = buffer[0]
        elif 0 == n_left:
            pass
        else:
            raise ArgumentError('un-recongnized key set for a Control : ', args)


    def serialize_instance(self):
        buttons = []
        if self.ctrl.enable:
            buttons.append(self.ctrl.position + ' ctrl')
        if self.shift.enable:
            buttons.append(self.shift.position + ' shift')
        if self.alt.enable:
            buttons.append(self.alt.position + ' alt')
        return { self.name : buttons }

    def available(self):
        if not self.key:
            return False
        return True

    @classmethod
    def validate_(cls):

        pass


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
            controllers.update( controller.serialize_instance() )
        return {inst.name:controllers}


class ControllerPackage(object):
    '''Controller Package : a collection of controller collection

    '''

    def __int__(self):
        pass
