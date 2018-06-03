

class Controller(object):
    '''Controller for a key combination

    components:
        name:       Name of this combination
        buttons:    Buttons needed to press of this combination

    '''

    def __init__(self, name, *args):
        self.name = name
        self.buttons = []
        for key in args:
            self.buttons.append(key)

    def serialize_instance(self):
        return {self.name:self.buttons}


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
