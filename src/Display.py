from PIL import Image,ImageDraw
from Fonts import Fonts
class Display:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.image_black = None
        self.draw_black = None

        self.image_red =  None
        self.draw_red =  None
        self.fonts = Fonts()

        self.reset_screen()
    
    def header_title(self, title: str) -> None:
        self.draw_red.rectangle((245,0, 640, 55), fill = 0) # Task area banner
        self.draw_red.text((250,10), title, font = self.fonts.tasks_list_title, fill = 255) # Task text

    def reset_screen(self):
        images_size = (self.width, self.height)
        self.image_black = Image.new('1', images_size, (1))
        self.draw_black = ImageDraw.Draw(self.image_black)

        self.image_red = Image.new('1', images_size, (1))
        self.draw_red = ImageDraw.Draw(self.image_red)

        self.draw_black.rectangle((0,0,240, 384), fill = 0) # Calender area rectangle
        self.draw_black.line((10,320,230,320), fill = 255) # Weather line
        self.draw_black.line((250,320,640,320), fill = 0) # Footer for additional items
        self.draw_red.rectangle((245,0, 640, 55), fill = 0) # Task area banner
        #self.draw_black.text((585,370),update_moment,font = font_update_moment, fill = 255) # The update moment in Pooch

    def show(self):
        pass
