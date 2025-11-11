from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QSizePolicy, QVBoxLayout

from other.notifications import get_notification_daemon
from other.signals import get_signals


class LogWidget(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFixedHeight(150)

        self.setObjectName("scroller")
        self.setStyleSheet(
            """
                background-color: #1e1e1e;
                color: white;
            """
        )

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.main_widget = QFrame(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setWidgetResizable(True)
        self.setWidget(self.main_widget)

        self.notif = get_notification_daemon()
        self.image = get_signals()

        self.notif.new_message.connect(self._create_new_notification)
        self.image.image_chosen.connect(self._create_new_image_chosen)

    def _create_new(self, message: str):
        log = LogItem(message)
        self.main_layout.insertWidget(0, log)

    def _create_new_notification(self, message: str):
        self._create_new(message)

    def _create_new_image_chosen(self, message: str):
        self._create_new("Set image to: " + message)


class LogItem(QFrame):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFixedHeight(50)

        self.setStyleSheet("background-color: #303030; border-radius: 5px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Calibri", 12))
        label.setWordWrap(True)
        label.setFixedWidth(500)
        self.main_layout.addWidget(label)
