
import cv2
import numpy as np

from Display import Display

class Mock_Display(Display):
    def __init__(self):
       Display.__init__(self)
       pass

    def show(self):
        print('Display Mock Display...')
        # _tuple_of_images = (
                # self.image_red,
                # self.image_black
                # )
        # _image =  np.concatenate(_tuple_of_images, axis=0)
        _image = np.array(self.image_black)
        cv2.imshow('image', cv2.resize(_image, (300, 300)))
        cv2.waitKey(1)

