#!/usr/bin/python3

import time
import sys
import os
import logging

from dotenv import load_dotenv

from tasks.Todo_List import Todos_List
from Display_Factory import Display_Factory
from Calender import Calender


env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
print("Loading env: " + env_path)
load_dotenv(dotenv_path=env_path, verbose=True)

WEATHER_API = os.getenv('WEATHER_API')

EPD_WIDTH = 640
EPD_HEIGHT = 384

class EPD: 
    def __init__(self):
        self.display = Display_Factory(EPD_WIDTH, EPD_HEIGHT)
        self.do_screen_update = 1
        self.todo_response = ''
        self.line_start = 48
        self.refresh_time = 60
        self.todos = Todos_List(self.display)
        self.calender = Calender(self.display)

    def run(self):
        while True:
            self.refresh()
            logging.info('EPD   : Sleeping for {}s...'.format(self.refresh_time))
            time.sleep(self.refresh_time)

    def refresh(self):
        self.display.reset_screen()
        # TODO: Refresh Calender
        self.calender.refresh()
        # Check weather and poppulate the weather variables
        # query_weather()
        # TODO: Fix this weather code

        # TODO: Refresh todos
        self.todos.refresh()

        self.display.show()

if __name__ == '__main__':
    edp = EPD()
    edp.run()

sys.exit(0)
