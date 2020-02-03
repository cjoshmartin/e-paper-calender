import threading
import time
import logging
import calendar
calendar.setfirstweekday(0)  # Monday is the first day of the week
from Display import Display

class Calender:
    def __init__(self, display: Display):
        logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")
        self.__display = display

        self.cal_width = 240
        # Calendar strings to be displayed
        self.weekday_name = None
        self.month_name = None
        self.day_of_the_month = None
        self.current_year = None
        self.month_cal = None
        self.calendar_month = None

        cal_reset_thread = threading.Thread(target=self.__reset, daemon=True)
        cal_reset_thread.start()

        self.fonts = self.__display.fonts
        logging.info("Calender  : Calender Setup correctly")

    def __reset(self):
        time_in_mins = 30
        time_in_seconds = time_in_mins * 60
        while True:
            logging.info("Calender  : updating Calender")
            day_of_the_month = time.strftime("%d") #[01-31]
            should_update_day = day_of_the_month != self.day_of_the_month
            if should_update_day:
                self.weekday_name = time.strftime("%A") # Monday, Tuesday, Wenesday
                self.day_of_the_month = day_of_the_month

            month_name = time.strftime("%B") # January, October, June
            should_update_month = month_name != self.month_name
            if should_update_month:
                self.month_name = month_name

            current_year = time.strftime("%Y") # 2019, 2020
            should_update_year = current_year != self.current_year
            if should_update_year:
                self.current_year = current_year
                self.month_cal = str(
                    calendar.month(
                        int(current_year),
                        int(time.strftime("%m"))
                    )
                )
                self.month_cal = self.month_cal.split("\n",1) # Splits cal out put into `January 2020` & the days of th month
                self.calendar_month = self.month_cal[0] # January 2020
                self.month_cal = self.month_cal[1] # Holds all the days of the Month


            if should_update_day or should_update_month or should_update_year:
                # TODO: Maybe an need a blocker for all these threads accessing this flag
                self.__display.should_update_display = True
            logging.info("Calender  : Update of Calender when well!")
            logging.info("Calender  : Sleeping calender update thread for {}s".format(time_in_seconds))
            time.sleep(time_in_seconds)

    def refresh(self):
        if self.weekday_name == None:
            return;

        logging.info("Calender  : Updating Calender on screen")
        # This section is to center the calendar text in the middle
        w_day_str, h_day_str = self.fonts.day_str.getsize(self.weekday_name)
        x_day_str = (self.cal_width / 2) - (w_day_str / 2)

        # The settings for the Calendar today number in the middle
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
