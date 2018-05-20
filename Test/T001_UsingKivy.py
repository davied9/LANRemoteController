# -*-coding:utf-8-*-

import kivy
# kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class HelloWorld(App):
    def build(self):
        return Button(text='hello world')

def test000():
    HelloWorld().run()


class MultiButton(Widget):
    def __init__(self, **kwargs):
        super(MultiButton, self).__init__(**kwargs)
        self.one = Button(text='one')
        self.two = Button(text='two')
        pass

class test(App):
    def build(self):
        return MultiButton()

def test001():
    test().run()

if __name__ == '__main__':
    test001()
    pass




