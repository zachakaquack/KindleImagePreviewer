from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    image_chosen = Signal(str)


def get_signals():
    global _signals_instance
    if "_signals_instance" not in globals():
        _signals_instance = Signals()
    return _signals_instance
