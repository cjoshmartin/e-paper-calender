from plugins.google_tasks import Todos_List
from plugins.Calender import Calender

from src.display  import Display
def get_plugins(display: Display ):
    plugin_list = [Todos_List(display), Calender(display)]
    return plugin_list