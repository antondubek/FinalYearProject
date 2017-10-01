from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class InitialMenu(BoxLayout):
    def AlertSomeone():
        print 'Alert'

    def RFID():
        print 'RFID'

    def Keypad():
        print 'Keypad'

class introduction(App):
    def build(self):
        return InitialMenu()
