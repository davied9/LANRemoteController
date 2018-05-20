# -*-coding:utf-8-*-

import kivy
# kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.button import Button


class test(App):
    def build(self):
        return Button(text='hello world')


if __name__ == '__main__':
    test().run()




