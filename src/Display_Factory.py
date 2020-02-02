import os


def Display_Factory(width: int, height: int):
    build_device = os.getenv('Build')
    print("Build Device is the following: {}".format(build_device))
    _instance = None

    if build_device == "target":
        from E_Paper_Display import E_Paper_Display
        _instance = E_Paper_Display(width, height)

    elif build_device == 'simulator':
        from Mock_Display import Mock_Display
        _instance = Mock_Display(width, height)
    else:
        raise Exception("`{}` is not a vaild build device type ".format(build_device))

    return _instance
