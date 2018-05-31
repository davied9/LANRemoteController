from KivyImporter import *

class Main(App):

    def build(self):
        root = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint=(1,None))
        root.add_widget(layout)

        for i in range(50):
            text = 'joker {0}'.format(i)
            layout.add_widget(Button(text=text, size_hint=(1,None), height=60))

        self.layout=layout
        return root

    def on_start(self):
        self.layout.bind(minimum_height=self.layout.setter('height'))

if '__main__' == __name__:
    Main().run()