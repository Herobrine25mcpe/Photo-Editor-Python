
import kivy
import io
import time
import os
import numpy as np
import cv2
import random
from kivy.app import App
from kivy.properties import ColorProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock



Builder.load_file('test_kv.kv')

fmagex = ""


class FullImage(Image):
    pass


def theme(theme):
    print("bgcol")
    if theme=="w":
        bgcolor = (0.84, 0.84, 0.84, 1)
    if theme=="d":
        bgcolor = (0.14, 0.14, 0.14, 1)
    if theme=="lp":
        bgcolor = (0.54,0.54,0.65,1)
    if theme=="dp":
        bgcolor =(0.14,0.14,0.25,1)
    if theme=="b":
        bgcolor =(0.14,0.24,0.55,1)
    if theme =="db":
        bgcolor = (0.14,0.24,0.85,1)
    if theme == "r":
        bgcolor = (0.68, 0.24, 0.24, 1)

    Window.clearcolor = bgcolor


def colorizer(file):
    print("loading models.....")
    net = cv2.dnn.readNetFromCaffe('./models/colorization_deploy_v2.prototxt','./models/colorization_release_v2.caffemodel')
    pts = np.load('./models/pts_in_hull.npy')


    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2,313,1,1)

    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1,313],2.606,dtype='float32')]


    image = cv2.imread(file)
    scaled = image.astype("float32")/255.0
    lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)


    resized = cv2.resize(lab,(224,224))
    L = cv2.split(resized)[0]
    L -= 50


    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1,2,0))

    ab = cv2.resize(ab, (image.shape[1],image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized,0,1)

    colorized = (255 * colorized).astype("uint8")

    print("done")
    filename="colorized.jpg"
    cv2.imwrite(filename, colorized)
    return filename




def saver(f):
    try:
        fmagex = f[0]
        f = open(fmagex,'rb')
        newimg = open('newimg.jpg','wb')
        for line in f:
            newimg.write(line)
    except:
        pass

def saturation(u):
    try:
        x = "colorized.jpg"
        img = cv2.imread(x)
        imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype('float32')
        h, s, v = cv2.split(imghsv)
        s = s * (int(u))
        print(s)
        s = np.clip(s, 0, 255)
        imghsv = cv2.merge([h, s, v])
        saturated = cv2.cvtColor(imghsv.astype('uint8'), cv2.COLOR_HSV2BGR)
        cv2.imwrite("colorized.jpg", saturated)
        print("done")
    except:
        print("saturation error")

def brightness(b):
    try:
        x = "colorized.jpg"
        img = cv2.imread(x)
        beta = b
        print(beta)
        bright = cv2.convertScaleAbs(img,alpha=0.9,beta=beta)
        cv2.imwrite("colorized.jpg", bright)
        print("done")
    except:
        print("brightness error")

def contrast(c):
    try:
        x = "colorized.jpg"
        img = cv2.imread(x)
        alpha = c/100
        print(alpha)
        contrast = cv2.convertScaleAbs(img, alpha=alpha,beta=1)
        cv2.imwrite("colorized.jpg", contrast)
        print("done")
    except:
        print("contrast error")

def hue(e):
    try:
        x = "colorized.jpg"
        img = cv2.imread(x)
        imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype('float32')
        h, s, v = cv2.split(imghsv)
        h = h * (int(e))
        h = np.clip(s, 0, 255)
        imghsv = cv2.merge([h, s, v])
        hueed = cv2.cvtColor(imghsv.astype('uint8'), cv2.COLOR_HSV2BGR)
        cv2.imwrite("colorized.jpg", hueed)
        print("done")
    except:
        print("hue error")


def smooth(s):
    try:
        x = "colorized.jpg"
        img = cv2.imread(x)
        sigmas = s*2
        sigmar = s/100
        print(sigmar, sigmas)
        smth= cv2.edgePreservingFilter(img,cv2.RECURS_FILTER, sigmas, sigmar)
        cv2.imwrite("colorized.jpg",smth)
        print("done")
    except:
        print("smooth error")



class MainLayout(Widget):


    def selected(self, filename):

        saver(filename)
        im = "newimg.jpg"
        im = colorizer(im)
        try:
            print(filename)
            self.ids.image1.source = filename[0]
            self.ids.image2.source = ''
        except:
            pass

    def apply(self):

            im="colorized.jpg"

            try:
                self.ids.image2.reload()
            except:
                print("coudln't reload")

            self.ids.image2.source = im


    def preview(self):
        try:
            self.ids.image2.source = ""
            self.ids.image1.source = ""
            bgcol="db"
            theme(bgcol)
        except:
            pass

    def download(self):
        try:
            fmagex = self.ids.image2.source
            print(fmagex)
            f = open(fmagex, 'rb')
            newimg = open('col-img.jpg', 'wb')
            for line in f:
                newimg.write(line)
        except:
            pass

    def update_image(self, dt):
        self.ids.image2.source.reload()

    def slide_it(self, *args):
        print(args)

    def bright_slider(self, *args):

        x = int(args[1])
        brightness(x)

    def cont_slider(self,*args):

        x = int(args[1])
        contrast(x)

    def hue_slider(self,*args):

        x = int(args[1])/10
        hue(x)

    def smooth_slider(self, *args):

        x = int(args[1])
        smooth(x)


    def satu_slider(self, *args):


        x= int(args[1])/10
        saturation(x)



class Testapp(App):
    def build(self):
        Window.clearcolor= (0.74, 0.74, 0.74, 1)
        return MainLayout()


if __name__ == "__main__":
    Testapp().run()
    try:
        os.remove("colorized.jpg")
        os.remove("newimg.jpg")
    except:
        pass
