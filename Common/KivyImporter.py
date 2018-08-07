import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.factory import Factory
try:
    from kivy.lang.builder import Builder
except ImportError:
    from kivy.lang import Builder


__all__ = (['kivy', 'Builder', 'Factory', 'App',
            'Screen', 'ScreenManager',
            'Widget','Label', 'Button', 'TextInput', 'CheckBox', 'Popup',
            'GridLayout', 'BoxLayout', 'ScrollView',
            ])