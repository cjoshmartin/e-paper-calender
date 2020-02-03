import threading
import time
import logging
import urllib

from PIL import Image, ImageDraw
from Fonts import Fonts


class Display:
    def __init__(self, width: int, height: int, type_of_display: str):
        self.width = width
        self.height = height
        # ----------------------------
        self.has_internet = True
        check_internet_thread = threading.Thread(target=self.__is_connected_to_internet, daemon=True)
        check_internet_thread.start()
        # ----------------------------
        self.should_update_display = True
        # ----------------------------
        assert len(type_of_display) > 1
        self.type_of_display = type_of_display
        # ----------------------------
        self.image_black = None
        self.draw_black = None
        # ----------------------------
        self.image_red = None
        self.draw_red = None
        # ----------------------------
        self.update_moment = time.strftime("%I") + ':' + time.strftime("%M") + ' ' + time.strftime("%p")
        # ----------------------------
        self.fonts = Fonts()
        # ----------------------------
        self.reset_screen()

    def __is_connected_to_internet(self):
        time_in_mins = 3
        time_in_seconds = time_in_mins * 60
        while True:
            try:
                urllib.request.urlopen('http://216.58.192.142', timeout=1)
                logging.info("Display:  Has internet connection")
                has_internet = True
            except urllib.error.URLError as err:
                has_internet = False
                logging.info("Display:  Does not have an internet connection")

            if has_internet != self.has_internet:
                self.has_internet = has_internet
                self.should_update_display = True

            logging.info("Display:  checking_for_connection thread is sleeping for {}s".format(time_in_seconds))
            time.sleep(time_in_seconds)

    def header_title(self, title: str) -> None:
        self.draw_red.rectangle((245, 0, 640, 55), fill=0)  # Task area banner
        self.draw_red.text((250, 10), title, font=self.fonts.tasks_list_title, fill=255)  # Task text

    def context_bar_title(self, title: str) -> None:
        unknown_constent = 550 # TODO: Find out what this is
        extra_todos_background_position = (
            unknown_constent,
            self.__starting_vertical_position_of_tasks + 2 + self.__line_location,
            self.__display.width,
            self.__starting_vertical_position_of_tasks + 18 + self.__line_location
        )

        w_notshown_tasks, h_notshown_tasks = self.__fonts.tasks_due_date.getsize(title)
        x_nowshown_tasks = unknown_constent + \
                           ((self.__display.width - unknown_constent) / 2) - (w_notshown_tasks / 2) # TODO:???, figure out what this is

        extra_todos_forground_position = (
            x_nowshown_tasks,
            self.__starting_vertical_position_of_tasks + 3.5 + self.__line_location
        )

        # Print larger rectangle for more tasks
        self.draw_red.rectangle(extra_todos_background_position, fill=0)
        # The placement for extra tasks not shown
        self.draw_red.text(extra_todos_forground_position, title,
                   font=self.__fonts.tasks_due_date, fill=255)  # Print identifier that there are tasks not shown

    def reset_screen(self):
        images_size = (self.width, self.height)
        self.image_black = Image.new('1', images_size, (1))
        self.draw_black = ImageDraw.Draw(self.image_black)

        self.image_red = Image.new('1', images_size, (1))
        self.draw_red = ImageDraw.Draw(self.image_red)

        self.draw_black.rectangle((0, 0, 240, 384), fill=0)  # Calender area rectangle
        self.draw_black.line((10, 320, 230, 320), fill=255)  # Weather line
        self.draw_black.line((250, 320, 640, 320), fill=0)  # Footer for additional items
        self.draw_red.rectangle((245, 0, 640, 55), fill=0)  # Task area banner

        self.update_moment = time.strftime("%I") + ':' + time.strftime("%M") + ' ' + time.strftime("%p")
        self.draw_black.text((585, 370), self.update_moment, font=self.fonts.update_moment,
                             fill=255)  # The update moment in Pooch

    def refresh(self):
        logging.info("Display:  Refreshing on A {} Display".format(self.type_of_display))
        if not self.has_internet:
            self.context_bar_title("No Internet Connection...")

        self.show()

        self.should_update_display = False

    def show(self):
        pass # Do not call this directly
