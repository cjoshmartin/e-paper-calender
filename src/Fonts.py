from PIL import ImageFont

# All fonts used in frames
class Fonts:
    def __init__(self):
        self.cal = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        self.day = ImageFont.truetype('fonts/Roboto-Black.ttf', 110)
        self.weather = ImageFont.truetype('fonts/Roboto-Black.ttf', 20)
        self.day_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 35)
        self.month_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 25)
        self.weather_icons = ImageFont.truetype('fonts/meteocons-webfont.ttf', 45)
        self.tasks_list_title = ImageFont.truetype('fonts/Roboto-Light.ttf', 30)
        self.tasks_list = ImageFont.truetype('fonts/tahoma.ttf', 12)
        self.tasks_due_date = ImageFont.truetype('fonts/tahoma.ttf', 11)
        self.tasks_priority = ImageFont.truetype('fonts/tahoma.ttf', 9)
        self.update_moment = ImageFont.truetype('fonts/tahoma.ttf', 9)
        self.icons_list = {u'01d':u'B',u'01n':u'C',u'02d':u'H',u'02n':u'I',u'03d':u'N',u'03n':u'N',u'04d':u'Y',u'04n':u'Y',u'09d':u'R',u'09n':u'R',u'10d':u'R',u'10n':u'R',u'11d':u'P',u'11n':u'P',u'13d':u'W',u'13n':u'W',u'50d':u'M',u'50n':u'W'}
