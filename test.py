import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# this is the main grid


class MyGridLayout(Widget):
    def press(self):
        name = self.name.text


class Testapp(App):
    def build(self):
        return MyGridLayout()


if __name__ == "__main__":
    Testapp().run()
