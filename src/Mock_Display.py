

from Display import Display

class Mock_Display(Display):
    def __init__(self, width: int, height: int):
       _type = "Mock"
       Display.__init__(self, width, height, _type)

    def show(self):
        _black_image = self.image_black.copy()
        _red_image = self.image_red.copy()

        _red_image.save('red.bmp')
        _black_image.save('black.bmp')
