from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.uix.scrollview import ScrollView


class ButtonContainer(ScrollView):

    button_height = NumericProperty(50)
    button_spacing = NumericProperty(2)

    def __init__(self, **kwargs):
        super(ButtonContainer, self).__init__(**kwargs)
        self.do_scroll_x = False
        # initialize UI structure manually here
        container = self.container = BoxLayout()
        container.size_hint = (1, None)
        container.orientation = 'vertical'
        self.add_widget(container)
        # do some binding
        container.bind(minimum_height=container.setter('height'))
        self.bind(button_spacing=container.setter('spacing'))
        self.bind(button_height=self._on_button_height_change)
        self.bind(height=self._on_height_change)

    def _on_button_height_change(self, trigger, value): # sync button_height change to all buttons
        if 0 == len(self.container.children): return
        for button in self.container.children:
            button.height = value

    def _on_height_change(self, *args): # compute height button height and spacing when height changes
        self.button_height = int(0.2 * self.height)
        self.button_spacing = int(0.05 * self.button_height)

    def add_button(self, button, index=0):
        button.size_hint = (1, None)
        button.height = self.button_height
        self.container.add_widget(button, index)

    def remove_button(self, button):
        self.container.remove_widget(button)

    def clear_buttons(self):
        self.container.clear_widgets()

    @property
    def buttons(self):
        return self.container.children


if '__main__' == __name__ :
    from kivy.app import App
    from kivy.uix.button import Button

    class test(App):

        def build(self, **kwargs):
            root = ButtonContainer()
            root.button_height = 60
            for i in range(20):
                root.add_button(Button(text='aa {}'.format(i)))
            return root

    test().run()