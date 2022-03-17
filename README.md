# Photo-Editor-Python
This is the Photo Edtior project in python with additional functionality of colorization of black and white images using opencv. Kivy is used ad the Ui/Ux framework for this project.


#Instruction:

Step 1: Install python 3.9 becuase as of now (March 2022) Kivy don't like python 3.10 very much.

Step 2: Install Pycharm for ease as it creates a virtual enviroment of its own, because if you don't things will get real messy really quick.

Step 2.5: If you refuse to install Pycharm use virtual environment in python.

              > python -m pip install --upgrade pip setuptools virtualenv
              > python -m virtualenv kivy_venv
              > kivy_venv\Scripts\activate
              
   And this is how you create a virtual environment in python, Thank you.
              
Step 3: install kivy in the Pycharm using python packages OR install it by using

               > python -m pip install --pre "kivy[full]" kivy_examples
   in the directory where you made the virtual environment.

Step 4: install opencv for python and also numpy

               > pip install opencv-python
               > pip install numpy
               
Step 5: paste the two files .py and .kv in the same directory. Make another folder name "modles" and put
        (colorization_deploy_v2.prototxt, colorization_release_v2.caffemodel and pts_in_hull.npy) in the folder

Step 5: run the code and enjoy.
