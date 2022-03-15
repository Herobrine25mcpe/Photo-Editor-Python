import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image


# this is the main grid

Builder.load_file('test_kv.kv')

global fimage
fmagex = "images/img1.jpg"


class FullImage(Image):
    pass


bgcolor = (0.54, 0.54, 0.54, 1)


class MainLayout(Widget):
    # Image Selector Function
    def selected(self, filename):

        try:
            self.ids.image1.source = filename[0]
        except:
            pass

    def apply(self):
        try:
            self.ids.image2.source = fmagex
        except:
            pass

    def preview(self):
        try:
            self.ids.image2.source = fmagex
        except:
            pass

    def download(self):
        try:
            self.ids.image2.source = fmagex
        except:
            pass





class Testapp(App):
    def build(self):
        Window.clearcolor = bgcolor
        return MainLayout()


if __name__ == "__main__":
    Testapp().run()
