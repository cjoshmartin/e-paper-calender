#!/usr/bin/python3

import sys
import os

from dotenv import load_dotenv

from plugins import get_plugins
from src.display import Display_Factory

env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
print("Loading env: " + env_path)
load_dotenv(dotenv_path=env_path, verbose=True)

WEATHER_API = os.getenv('WEATHER_API')

class EPD:
    def __init__(self):
        self.display = Display_Factory()
        self.plugins = get_plugins(self.display)


    def run(self):
        while True:
            self.refresh()

    # Check weather and poppulate the weather variables
    # query_weather()
    # TODO: Fix this weather code

    def refresh(self):
        if self.display.should_update_display:
            self.display.reset_screen()

            for plugin in self.plugins:
                plugin.refresh()

            self.display.refresh()

if __name__ == '__main__':
    edp = EPD()
    edp.run()

sys.exit(0)
