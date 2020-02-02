

from Display import Display

class Mock_Display(Display):
    def __init__(self, width: int, height: int):
       Display.__init__(self, width, height)
       pass

    def show(self):
        print('Display Mock Display...')
        _black_image = self.image_black.copy()
        _red_image = self.image_red.copy()

        _red_image.save('red.bmp')
        _black_image.save('black.bmp')
