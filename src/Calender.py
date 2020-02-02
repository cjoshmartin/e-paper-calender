import time
import logging
import calendar
calendar.setfirstweekday(0)  # Monday is the first day of the week
from Display import Display

class Calender:
    def __init__(self, display: Display):
        self.__display = display

        self.cal_width = 240
        # Calendar strings to be displayed
        self.weekday_name = time.strftime("%A") # Monday, Tuesday, Wenesday
        self.month_name = time.strftime("%B") # January, October, June
        self.day_of_the_month = time.strftime("%d") #[01-31]
        self.current_year = time.strftime("%Y") # 2019, 2020
        self.month_cal = str(
            calendar.month(
                int(self.current_year),
                int(time.strftime("%m"))
                )
            )
        self.month_cal = self.month_cal.split("\n",1) # Splits cal out put into `January 2020` & the days of th month
        self.calendar_month = self.month_cal[0] # January 2020
        self.month_cal = self.month_cal[1] # Holds all the days of the Month

        self.fonts = self.__display.fonts
        logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Calender  : Calender Setup correctly")

    def reset(self):
        logging.info("Calender  : Resetting Calender")
        self.weekday_name = time.strftime("%A") # Monday, Tuesday, Wenesday
        self.month_name = time.strftime("%B") # January, October, June
        self.day_of_the_month = time.strftime("%d") #[01-31]
        self.current_year = time.strftime("%Y") # 2019, 2020
        self.month_cal = str(
            calendar.month(
                int(self.current_year),
                int(time.strftime("%m"))
            )
        )
        self.month_cal = self.month_cal.split("\n",1) # Splits cal out put into `January 2020` & the days of th month
        self.calendar_month = self.month_cal[0] # January 2020
        self.month_cal = self.month_cal[1] # Holds all the days of the Month

        logging.info("Calender  : Resetting Calender when well!")

    def refresh(self):
        self.reset()
        logging.info("Calender  : Updating Calender on screen")
        # This section is to center the calendar text in the middle
        w_day_str, h_day_str = self.fonts.day_str.getsize(self.weekday_name)
        x_day_str = (self.cal_width / 2) - (w_day_str / 2)

        # The settings for the Calenday today number in the middle
        w_day_num, h_day_num = self.fonts.day.getsize(self.day_of_the_month)
        x_day_num = (self.cal_width / 2) - (w_day_num / 2)

        # The settings for the month string in the middle
        w_month_str, h_month_str = self.fonts.month_str.getsize(self.month_cal)
        x_month_str = (self.cal_width / 2) - (w_month_str / 2)

        self.__display.draw_black.text((20, 190),self.month_cal , font = self.fonts.cal, fill = 255) # Month calender text
        self.__display.draw_black.text((x_day_str,10),self.weekday_name, font = self.fonts.day_str, fill = 255) # Day string calender text
        self.__display.draw_black.text((x_day_num,35),self.day_of_the_month, font = self.fonts.day, fill = 255) # Day number string text
        self.__display.draw_black.text((x_month_str,150), self.month_cal, font = self.fonts.month_str, fill = 255) # Month string text
        logging.info("Calender  : Finished updating Calender on screen")
