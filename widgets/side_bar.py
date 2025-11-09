from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
import webbrowser
from pathlib import Path
from other import files


class SideBar(QFrame):
    switch = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFixedWidth(100)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setStyleSheet(
            """
            background-color: #303030;
            color: white;
            border-radius: 5px;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 15, 5, 15)
        self.main_layout.setSpacing(25)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.home_button = IconButton(
            QIcon(f"{files.resource_path('assets/home.svg')}")
        )
        self.settings_button = IconButton(
            QIcon(f"{files.resource_path('assets/settings.svg')}")
        )
        self.resolution_button = IconButton(
            QIcon(f"{files.resource_path('assets/web.svg')}")
        )
        self.help_button = IconButton(
            QIcon(f"{files.resource_path('assets/help.svg')}")
        )

        self.home_button.clicked.connect(lambda: self.switch.emit("home"))
        self.settings_button.clicked.connect(lambda: self.switch.emit("settings"))
        self.resolution_button.clicked.connect(
            lambda: webbrowser.open(
                "https://en.wikipedia.org/wiki/Amazon_Kindle#Specifications"
            )
        )
        self.help_button.clicked.connect(lambda: self.switch.emit("help"))

        self.main_layout.addWidget(self.home_button)
        self.main_layout.addWidget(self.settings_button)
        self.main_layout.addWidget(self.resolution_button)

        # bottom stuff
        self.main_layout.addSpacerItem(
            QSpacerItem(0, 1, vData=QSizePolicy.Policy.Expanding)
        )
        self.main_layout.addWidget(self.help_button)


class IconButton(QPushButton):
    def __init__(self, icon: QIcon, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.setIconSize(QSize(50, 50))
        self.setIcon(icon)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(
            """
            QPushButton{
                background-color: #303030;
                padding: 5px;
            }
            QPushButton:hover{
                background-color: #404040;
            }
            """
        )
