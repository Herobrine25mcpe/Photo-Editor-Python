
import kivy
import io
import os
import numpy as np
import cv2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image


Builder.load_file('colorizer_kv.kv')

fmagex = ""


class FullImage(Image):
    pass


def theme(theme):
    print("bgcol")
    if theme=="l":
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
        bgcolor = (0.14,0.85,0.85,1)
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
        bright = cv2.convertScaleAbs(img,alpha=1,beta=beta)
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
        contrast = cv2.convertScaleAbs(img, alpha=alpha,beta=0)
        cv2.imwrite("colorized.jpg", contrast)
        print("done")
    except:
        print("contrast error")



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

    def colorize(self):

        im = self.ids.image1.source
        col = colorizer(im)
        try:
            self.ids.image2.reload()
        except:
            print("coudln't reload")

        self.ids.image2.source = col

    def reset(self):
        try:
            self.ids.image2.source = ""
            self.ids.image1.source = ""

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



    def bright_slider(self, *args):

        x = int(args[1])
        brightness(x)

    def cont_slider(self,*args):

        x = int(args[1])
        contrast(x)


    def satu_slider(self, *args):


        x= int(args[1])/10
        saturation(x)

    def theme(self,id):

        bgcolor=id
        theme(bgcolor)

class Colorizer(App):
    def build(self):
        Window.clearcolor= (0.14, 0.24, 0.34, 1)
        return MainLayout()


if __name__ == "__main__":
    Colorizer().run()
    try:
        os.remove("colorized.jpg")
        os.remove("newimg.jpg")
    except:
        pass
