from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
<ControllerEditor>:
    size_hint: 1, None
    height: 100
    left_ctrl_checkbox:     left_ctrl_checkbox
    right_ctrl_checkbox:    right_ctrl_checkbox
    left_shift_checkbox:    left_shift_checkbox
    right_shift_checkbox:   right_shift_checkbox
    left_alt_checkbox:      left_alt_checkbox
    right_alt_checkbox:     right_alt_checkbox
    controller_name_editor: controller_name_editor
    controller_key_editor:  controller_key_editor
    GridLayout:
        cols: 3
        rows: 4
        Widget:
        Label:
            text: 'left'
        Label:
            text: 'right'
        Label:
            text: 'ctrl'
        CheckBox:
            id: left_ctrl_checkbox
            group: 'group_control'
        CheckBox:
            id: right_ctrl_checkbox
            group: 'group_control'
        Label:
            id: shift_label
            text: 'shift'
        CheckBox:
            id: left_shift_checkbox
            group: 'group_shift'
        CheckBox:
            id: right_shift_checkbox
            group: 'group_shift'
        Label:
            id: alt_label
            text: 'alt'
        CheckBox:
            id: left_alt_checkbox
            group: 'group_alternative'
        CheckBox:
            id: right_alt_checkbox
            group: 'group_alternative'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'name'
        Label:
            text: 'key'
    BoxLayout:
        orientation: 'vertical'
        Widget:
        TextInput:
            id: controller_name_editor
            multiline: False
            size_hint: 1,None
            height: 30
        Widget:
        TextInput:
            id: controller_key_editor
            multiline: False
            size_hint: 1,None
            height: 30
        Widget:
''')


class ControllerEditor(BoxLayout):
    '''Controller Editor

    components:
        controller:     Controller that is being edit
    '''
    def __init__(self, **kwargs):
        self.controller = kwargs["controller"]
        self.controller_button = kwargs["controller_button"]
        del(kwargs['controller'], kwargs['controller_button'])
        BoxLayout.__init__(self, **kwargs)
