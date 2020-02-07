import logging
from lib import epd7in5b
from src.display.Display import Display

class E_Paper_Display (Display):
    def __init__(self):
       Display.__init__(self)
       self.__epd = epd7in5b.EPD() 
       self.__epd.init()

    def show(self):
        _black_image = self.__epd.get_frame_buffer(self.image_black)
        _red_image = self.__epd.get_frame_buffer(self.image_red)

        logging.info('{}   : -= Updating ePaper... =-'.format(self.__name__))
        self.__epd.display_frame(
            _black_image,
            _red_image
            )
        logging.info('{}     : -= ...Done =-'.format(self.__name__))
