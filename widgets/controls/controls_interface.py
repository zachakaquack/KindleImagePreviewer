from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
import webbrowser

from widgets.controls.kindle_input import KindleInput
from widgets.controls.image_picker import ImagePicker
from widgets.controls.log import LogWidget


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

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton(
            "Click to find your kindle's resolution (scroll down)"
        )
        self.button.clicked.connect(
            lambda: webbrowser.open(
                "https://en.wikipedia.org/wiki/Amazon_Kindle#Specifications"
            )
        )
        self.main_layout.addWidget(self.button)

        self.kindle_input = KindleInput()
        self.main_layout.addWidget(self.kindle_input)

        self.image_picker = ImagePicker()
        self.main_layout.addWidget(self.image_picker)

        self.logger = LogWidget()
        self.main_layout.addWidget(self.logger)
