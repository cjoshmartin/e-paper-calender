from PIL import Image,ImageDraw
from Fonts import Fonts
class Display:
    def __init__(self):
        # Create clean black frames with any existing Bitmaps
        self.image_black = Image.open('BK_Black.bmp')
        self.draw_black = ImageDraw.Draw(self.image_black)

        # Create clean red frames with any existing Bitmaps
        self.image_red = Image.open('BK_Red.bmp')
        self.draw_red = ImageDraw.Draw(self.image_red)
        self.fonts = Fonts()

        self.setup()
    
    def setup(self):
        self.draw_black.rectangle((0,0,240, 384), fill = 0) # Calender area rectangle
        self.draw_black.line((10,320,230,320), fill = 255) # Weather line
        self.draw_black.line((250,320,640,320), fill = 0) # Footer for additional items
        self.draw_red.rectangle((245,0, 640, 55), fill = 0) # Task area banner
        self.draw_red.text((250,10), "Tasks", font = self.fonts.tasks_list_title, fill = 255) # Task text
        #self.draw_black.text((585,370),update_moment,font = font_update_moment, fill = 255) # The update moment in Pooch

    def show(self):
        pass
