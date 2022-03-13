import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


# this is the main grid

Builder.load_file('test.kv')

class MainLayout(Widget):
    pass


class Testapp(App):
    def build(self):
        Window.clearcolor = (9/255, 24/255, 77/255, 1)
        return MainLayout()


if __name__ == "__main__":
    Testapp().run()
