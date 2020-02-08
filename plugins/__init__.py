import os
import logging
from importlib import import_module
from src.display  import Display

plugins_to_exclude = set(['weather', '__pycache__'])

def get_plugins(display: Display ):
    plugin_list = []
    start_of_log_messages = "{}: ".format(__name__)
    logging.info(start_of_log_messages + "Starting to load plugins")
    root = os.path.dirname(__file__)

    for file in os.scandir(root):
        if file.is_dir() and file.name not in plugins_to_exclude:
            plugin_to_import = ".{}".format(file.name) # relative path inside the plugins folder
            plugin_module = import_module(plugin_to_import, package=__name__)
            plugin_class = getattr(plugin_module, file.name)
            plugin_list.append(plugin_class(display))
            logging.info(start_of_log_messages + "Successfully loaded `{}`".format(file.name))

    logging.info(start_of_log_messages + "Finished loading plugins")
    return plugin_list