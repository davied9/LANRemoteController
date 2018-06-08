from Common.KivyImporter import *
from kivy.uix.screenmanager import CardTransition, SwapTransition, ShaderTransition, SlideTransition
from kivy.uix.screenmanager import WipeTransition, FadeTransition, FallOutTransition, RiseInTransition
from kivy.properties import ObjectProperty
from Common.Exceptions import *
from Controller.LRCController import Controller, ControllerSet, ControllerPackage
import os, json


Builder.load_string('''
<ControllerCollectionScreen>:
    controller_set_scrollview: controller_set_scrollview
    controller_set_container: controller_set_container
    display_title: title_label
    size_hint_min: 400, 600
    BoxLayout:
        orientation: 'vertical'
        padding: 30, 30
        BoxLayout:
            orientation: 'horizontal'
            size_hint_max_y: 50
            Label:
                id: title_label
                text: 'Collections'
                font_size: 43
            Button:
                text: 'Add'
                size_hint_max: 50, 50
                on_release: root._goto_builder_screen(self)
        Widget:
            size_hint_max_y: 30
        ScrollView:
            id: controller_set_scrollview
            do_scroll_x: False
            GridLayout:
                id: controller_set_container
                cols: 1
                spacing: 10
                size_hint: 1, None  # this will make this not in control of its parent
                height: 50


<ControllerScreen>:
    button_container: button_container
    display_title: title_label
    BoxLayout:
        orientation: 'vertical'
        padding: 30, 30
        BoxLayout:
            size_hint_max_y: 50
            Button:
                text: 'Back'
                size_hint_max_x: 50
                on_release: root._go_back_last_screen(self)
            Label:
                id: title_label
                text: 'Default'
                font_size: 43
            Button:
                text: 'Edit'
                size_hint_max_x: 50
                on_release: root._goto_builder_screen(self)
        Widget:
            size_hint_max_y: 30
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: button_container
                cols: 1
                size_hint: 1, None
                height: 1
                spacing: 10


<ControllerCollectionBuildScreen>:
    display_title: title_button
    button_container: button_container
    background_floatlayout: background_floatlayout
    info_label: info_label
    set_name_editor: None
    FloatLayout:
        id: background_floatlayout
        BoxLayout:
            orientation: 'vertical'
            padding: 30, 30
            Button:
                id: title_button
                text: 'Builder'
                size_hint_max_y: 80
                font_size: 43
                background_color: [0, 0, 0, 0]
                on_release: root._open_set_name_editor(self, self.text)
            ScrollView:
                do_scroll_x: False
                GridLayout:
                    id: button_container
                    cols: 1
                    size_hint: 1, None
                    height: 1
                    spacing: 10
            BoxLayout:
                size_hint_max_y: 80
                padding: 10, 30, 10, 0 # left, top, right, down
                Button:
                    text: 'Back'
                    size_hint_max_x: 50
                    on_release: root._go_back_last_screen(self)
                Widget:
                Button:
                    text: 'Save'
                    size_hint_max_x: 50
                    on_release: root._save_controller_set(self)
                Widget:
                Button:
                    text: 'Add'
                    size_hint_max_x: 50
                    on_release: root._create_new_button(self)
        Label:
            id: info_label
            font_size: 12
            pos_hint: {'x':0, 'y':0}
            size_hint_max_y: 15

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
        del(kwargs['controller'])
        BoxLayout.__init__(self, **kwargs)


class ControllerCollectionScreen(Screen): # gallery of controller sets

    def test_fun(self, *args):
        print('test ', *args)

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.index = 0

    def on_pre_enter(self, *args):
        self._reset_controller_set_container()
        for _set in self._load_controller_set_from_local().values():
            self._add_controller_set_button(_set)

    def _load_controller_set_from_local(self):
        controller_sets = {}
        for r, dirs, files in os.walk('./collections'):
            for file_name in files:
                if not file_name.endswith('.json'): continue
                full_path = r+'/'+file_name
                with open(full_path) as file_handle:
                    print('loading configuration from "{0}"'.format(full_path))
                    info = json.load(file_handle)
                    for name, config in info.items():
                        controller_sets[name] = ControllerSet(name, **config)
            break

        App.get_running_app().controller_sets = controller_sets

        return controller_sets

    def _reset_controller_set_container(self):
        self.controller_set_container.clear_widgets()
        self.controller_set_container.height = 1

    def _add_controller_set_button(self, controller_set):
        self.controller_set_container.add_widget(Button(
            text=controller_set.name,
            size_hint=(1,None),
            height=50,
            on_release=self._goto_controller_screen
        ))
        self.controller_set_container.height += 60

    def _goto_controller_screen(self, button): # goto controller screen to operate
        App.get_running_app().current_edit_set = button.text
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller'

    def _goto_builder_screen(self, button): # add new controller
        App.get_running_app().current_edit_set = None
        self.manager.last_screen = "Controller Collections"
        self.manager.current = 'Controller Collection Builder'


class ControllerScreen(Screen): # controller operation room

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()

        self._reset_button_container()
        for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
            self._add_controller_button(controller)

        self.display_title.text = current_app.current_edit_set

    def _reset_button_container(self):
        self.button_container.clear_widgets()
        self.button_container.height = 50

    def _add_controller_button(self, controller):
        self.button_container.add_widget(Button(
                text=controller.name,
                size_hint=(1, None),
                height=50
            ))
        self.button_container.height += 60

    def _go_back_last_screen(self, button):
        App.get_running_app().current_edit_set = self.display_title.text

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen

    def _goto_builder_screen(self, button): # Edit current controller collection
        App.get_running_app().current_edit_set = self.display_title.text
        self.manager.last_screen = "Controller"
        self.manager.current = 'Controller Collection Builder'


class ControllerCollectionBuildScreen(Screen): # controller collection builder
    '''Controller Collection Build Screen
    use "set" instead of "Collection" in code for short

    components:
        display_title:      title Button
        button_container:   button container for controllers
        background_floatlayout:  background FloatLayout
        set_name_editor:    controller collection TextInput

    '''

    set_name_editor = ObjectProperty(None, allownone=True)
    controller_editor = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()
        if current_app.current_edit_set:
            self.display_title.text = current_app.current_edit_set
            self.is_new = False
        else:
            self.display_title.text = 'New'
            self.is_new = True

        self._reset_controller_set_container()
        if not self.is_new:
            for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
                self._add_controller_button(controller)

    def present_info(self, info):
        self.info_label.text = info

    # as callback for display_title on_press
    def _open_set_name_editor(self, *args):
        print('_open_set_name_editor', args)
        # disable display_title to avoid re-call of _open_set_name_editor
        self.display_title.disabled = True
        # create set_name_editor
        if self.set_name_editor is None:
            self.set_name_editor = TextInput(
                size_hint=[ None, None],
                font_size=43,
                multiline=False
            )
            self.background_floatlayout.add_widget(self.set_name_editor)
        self.set_name_editor.size = self.display_title.size
        self.set_name_editor.pos  = self.display_title.pos
        self.set_name_editor.text = self.display_title.text
        self.set_name_editor.bind(focused=self._on_focused_set_name_editor)
        # bind size && pos, call sync once manually to sync pos && size
        self.display_title.bind(size=self._sync_display_title_size_to_set_name_editor)
        self.display_title.bind(pos=self._sync_display_title_pos_to_set_name_editor)

    # as callback for set_name_editor focus
    def _on_focused_set_name_editor(self, _set_name_eidtor, focused):
        if focused:
            self.set_name_editor.select_all()
        else:
            self._close_set_name_editor()

    def _close_set_name_editor(self, *args):
        print('_close_set_name_editor', args)
        self.display_title.unbind(size=self._sync_display_title_size_to_set_name_editor)
        self.display_title.unbind(pos=self._sync_display_title_pos_to_set_name_editor)
        self.display_title.disabled = False
        self.display_title.text = self.set_name_editor.text
        self.background_floatlayout.remove_widget(self.set_name_editor)
        self.set_name_editor = None

    # as callback for display_title pos
    def _sync_display_title_pos_to_set_name_editor(self, _display_title, new_pos):
        self.set_name_editor.pos = new_pos

    # as callback for display_title size
    def _sync_display_title_size_to_set_name_editor(self, _display_title, new_size):
        self.set_name_editor.size = new_size

    # as callback for set_name_editor
    def _sync_set_name_to_display_title(self, _set_name_editor, text):
        self.display_title.text = text

    def _reset_controller_set_container(self):
        self.button_container.clear_widgets()
        self.button_container.height = 1

    # add controller button to controller container for exist controller collection
    def _add_controller_button(self, controller):
        button = Button( text=controller.name, size_hint=(1, None), height=50, on_release=self._on_controller_button_released )
        button.controller = controller
        self.button_container.add_widget(button)
        self.button_container.height += (button.height + self.button_container.spacing[1])

    # as callback for "Save" button -- save this build to a controller set file
    def _save_controller_set(self, button):
        pass

    # as callback for "Add" button -- add button for new created controller
    def _create_new_button(self, button):
        new_controller = Controller('New', 'a')
        self._add_controller_button(new_controller)

    # as callback for "Back" button
    def _go_back_last_screen(self, button):
        App.get_running_app().current_edit_set = self.display_title.text

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen

        if self.set_name_editor:
            self._close_set_name_editor()

        if self.controller_editor:
            self._close_controller_editor()

    # as callback for controller button
    def _on_controller_button_released(self, controller_button):
        if not self.controller_editor: # not editing
            self._open_controller_editor(controller_button)
        elif self.controller_editor.controller is controller_button.controller: # editing this
            try:
                self._sync_controller_editor_to_controller()
                self._close_controller_editor()
            except Controller.UnsupportedKeyForControllerError as err: # unsupported key
                self.present_info(str(err))
            finally:
                pass
        else: # another button is released
            self._close_controller_editor()
            self._open_controller_editor(controller_button)

    def _open_controller_editor(self, controller_button):
        controller = controller_button.controller
        print('edit {0}'.format(controller) )
        # create editor
        self.controller_editor = ControllerEditor(controller=controller)
        # add editor to layout
        ix_button = self._get_controller_button_index(controller_button)
        self.button_container.add_widget(self.controller_editor, index=ix_button)
        self.button_container.height += (self.controller_editor.height + self.button_container.spacing[1])
        # set checkboxes
        if controller.ctrl.enable:
            if controller.ctrl.is_left:
                self.controller_editor.left_ctrl_checkbox.active = True
            else:
                self.controller_editor.right_ctrl_checkbox.active = True
        if controller.shift.enable:
            if controller.shift.is_left:
                self.controller_editor.left_shift_checkbox.active = True
            else:
                self.controller_editor.right_shift_checkbox.active = True
        if controller.alt.enable:
            if controller.alt.is_left:
                self.controller_editor.left_alt_checkbox.active = True
            else:
                self.controller_editor.right_alt_checkbox.active = True
        # set editor name
        self.controller_editor.controller_name_editor.text = controller.name
        # set key
        self.controller_editor.controller_key_editor.text = controller.key

    def _close_controller_editor(self):
        controller = self.controller_editor.controller
        print('close editor for {0}'.format(controller))
        # remove editor from layout
        self.button_container.remove_widget(self.controller_editor)
        self.button_container.height -= (self.controller_editor.height + self.button_container.spacing[1])
        # reset
        self.controller_editor = None

    def _sync_controller_editor_to_controller(self):
        controller = self.controller_editor.controller
        # save edit to controller set
        Controller.validate_key(self.controller_editor.controller_key_editor.text)
        # .. sync key
        controller.key = self.controller_editor.controller_key_editor.text
        # .. sync editor name
        controller.name = self.controller_editor.controller_name_editor.text
        # .. sync ctrl
        if self.controller_editor.left_ctrl_checkbox.active:
            controller.ctrl.enable  = True
            controller.ctrl.is_left = True
        elif self.controller_editor.right_ctrl_checkbox.active:
            controller.ctrl.enable  = True
            controller.ctrl.is_left = False
        else:
            controller.ctrl.enable  = False
            controller.ctrl.is_left = True
        # .. sync shift
        if self.controller_editor.left_shift_checkbox.active:
            controller.shift.enable  = True
            controller.shift.is_left = True
        elif self.controller_editor.right_shift_checkbox.active:
            controller.shift.enable  = True
            controller.shift.is_left = False
        else:
            controller.shift.enable  = False
            controller.shift.is_left = True
        # .. sync alt
        if self.controller_editor.left_alt_checkbox.active:
            controller.alt.enable  = True
            controller.alt.is_left = True
        elif self.controller_editor.right_alt_checkbox.active:
            controller.alt.enable  = True
            controller.alt.is_left = False
        else:
            controller.alt.enable  = False
            controller.alt.is_left = True

    class ControllerButtonNotFoundError(NotFoundError):

        def __int__(self, controller_button, button_container, *args):
            self.controller_button = controller_button
            self.button_container  = button_container
            NotFoundError.__init__(self, *args)

        def __str__(self):
            return ('Controller button {0} is not in button container {1}'.format(self.controller_button, self.button_container))

    def _get_controller_button_index(self, controller_button):
        for index in range(len(self.button_container.children)):
            if controller_button is self.button_container.children[index]:
                return index
        raise ClientUI.ControllerButtonNotFoundError(controller_button, self.button_container)


class ClientUI(App):
    '''Client Graphic User Interface

    components:
        screen_manager:                 screen manager
        screen_manager.last_screen:     last screen
        controller_sets:                all controller collections loaded from local files
        current_edit_set:               current edited controller set

    '''

    def build(self):
        print('working directory : {0}'.format( os.getcwd() ))

        self.screen_manager = ScreenManager(transition=RiseInTransition())

        self.controller_set_screen = ControllerCollectionScreen(name='Controller Collections')
        self.screen_manager.add_widget(self.controller_set_screen)

        self.controller_set_builder_screen = ControllerCollectionBuildScreen(name='Controller Collection Builder')
        self.screen_manager.add_widget(self.controller_set_builder_screen)

        self.controller_screen = ControllerScreen(name='Controller')
        self.screen_manager.add_widget(self.controller_screen)

        self.screen_manager.current = 'Controller Collections'

        self.screen_manager.last_screen = self.screen_manager.current
        self.current_edit_set = None

        return self.screen_manager

    def on_start(self):
        win = self.root.get_root_window()
        if win:
            win.minimum_width, win.minimum_height = [400, 600]
            win.size = [400, 600]


def __test000():
    ClientUI().run()

if '__main__' == __name__:
    __test000()