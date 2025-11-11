from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    # return the path of the image
    image_chosen = Signal(str)
    image_settings_changed = Signal(dict)
    update_image_resolution = Signal(int, int)
    export_image = Signal()
    refresh_image = Signal()


def get_signals():
    global _signals_instance
    if "_signals_instance" not in globals():
        _signals_instance = Signals()
    return _signals_instance
