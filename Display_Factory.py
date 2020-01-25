import os

from E_Paper_Display import E_Paper_Display
from Mock_Display import Mock_Display

def Display_Factory():
    build_device = os.getenv('Build')
    _instance = None

    if build_device == "target":
        _instance = E_Paper_Display()

    elif build_device == 'simulator':
        _instance = Mock_Display()

    return _instance