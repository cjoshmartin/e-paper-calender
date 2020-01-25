#!/usr/bin/python3

from PIL import Image,ImageDraw, ImageFont
import calendar
import time
import requests
import sys
import json
import datetime
import os, sys
from dotenv import load_dotenv

from Todo_List import Todos_List
from Display_Factory import Display_Factory


env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
print("Loading env: " + env_path)
load_dotenv(dotenv_path=env_path, verbose=True)

TODOIST_TOKEN = os.getenv('TODOIST_TOKEN')
WEATHER_API = os.getenv('WEATHER_API')

print(TODOIST_TOKEN + "\n" + WEATHER_API)
EPD_WIDTH = 640
EPD_HEIGHT = 384

Display = Display_Factory()


class EPD: 
    def __init__(self):
        self.do_screen_update = 1
        self.todo_response = ''
        self.line_start = 48
        self.weather_reponse= None
        self.forecast_reponse = None
        self.todo_wait= 600
        self.refresh_time= 600
        self.start_time = time.time() + self.refresh_time
        self.todos = Todos_List()

    def refresh(self):
        pass

    def run(self):
        while True:
            query_todo_list()
            if (do_screen_update == 1):
                do_screen_update = 0
                refresh_Screen()
                start_time = time.time() + refresh_time
            elif (time.time() - start_time) > 0:
                print('-= General Refresh =-')
                refresh_Screen()
                start_time = time.time() + refresh_time
            time.sleep(todo_wait)

    def refresh_Screen(self):
        update_moment = time.strftime("%I") + ':' + time.strftime("%M") + ' ' + time.strftime("%p")
        # TODO: Refresh Calender

        # Check weather and poppulate the weather variables
        query_weather()
        # TODO: Fix this weather code

        # TODO: Refresh todos
        if(self.todos.get_todos()):
            self.todos.refresh(Display.draw_black, Display.draw_red)
        Display.show()

if __name__ == '__main__':
    edp = EPD()
    edp.run()

sys.exit(0)
