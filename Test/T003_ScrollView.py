from KivyImporter import *




class Main(App):

    def build(self):
        root = BoxLayout(orientation='vertical', padding=30, spacing=10)
        root.add_widget(Button(text='add', size_hint=(0.6,0.1), pos_hint={'center_x':0.5, 'center_y':0.5},
                               on_press=self.add_button))

        scroll = ScrollView()
        root.add_widget(scroll)

        layout = BoxLayout(orientation='vertical', size_hint=(1,None))
        scroll.add_widget(layout)

        layout.bind(minimum_height=layout.setter('height'))

        self.index = 7
        for i in range(self.index):
            text = 'joker {0}'.format(i)
            layout.add_widget(Button(text=text, size_hint=(1,None), height=60))

        self.scroll_layout = layout
        return root

    def on_start(self):
        pass

    def add_button(self, _):
        self.index += 1
        text = 'joker {0}'.format(self.index)
        self.scroll_layout.add_widget(Button(text=text, size_hint=(1,None), height=60))

if '__main__' == __name__:
    Main().run()