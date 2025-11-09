from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QHBoxLayout,
)
from other.switcher import Switcher
from widgets.side_bar import SideBar

from widgets.controls.main_controls import MainControls
from widgets.settings import SettingsPage
from widgets.help import HelpPage


class ControlsInterface(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            background-color: #1e1e1e;
            color: white;
            """
        )

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebar = SideBar()
        self.main_layout.addWidget(self.sidebar)

        self.switcher = Switcher()
        self.main_layout.addWidget(self.switcher)

        self.main_controls = MainControls()
        self.switcher.addSwitcher("home", self.main_controls)

        self.settings_page = SettingsPage()
        self.switcher.addSwitcher("settings", self.settings_page)

        self.help_page = HelpPage()
        self.switcher.addSwitcher("help", self.help_page)

        self.sidebar.switch.connect(self.switcher.switchTo)
