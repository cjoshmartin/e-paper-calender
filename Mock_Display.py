
import cv2
import numpy as np

from Display import Display

class Mock_Display(Display):
    def __init__(self):
       Display.__init__(self)
       pass 

    def show(self):
        _tuple_of_images = (self.image_red, self.image_black)
        _image =  np.concatenate(_tuple_of_images, axis=0)
        cv2.imshow('image', _image)
        cv2.waitKey(1)