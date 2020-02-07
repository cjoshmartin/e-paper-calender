import logging
import os



def Display_Factory():
    build_device = os.getenv('Build')
    logging.info("Display Factory   :Build Device is the following: {}".format(build_device))
    logging.getLogger().setLevel(logging.INFO)
    _instance = None

    if build_device == "target":
        from src.display.E_Paper_Display import E_Paper_Display
        _instance = E_Paper_Display()

    elif build_device == 'simulator':
        from src.display.Mock_Display import Mock_Display
        _instance = Mock_Display()
    else:
        raise Exception("`{}` is not a vaild build device type ".format(build_device))

    return _instance
