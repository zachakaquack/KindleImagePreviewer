from PySide6.QtCore import QObject, Signal


class NotificationDaemon(QObject):
    new_message = Signal(str)


def get_notification_daemon():
    global _notification_daemon_instance
    if "_notification_daemon_instance" not in globals():
        _notification_daemon_instance = NotificationDaemon()
    return _notification_daemon_instance
