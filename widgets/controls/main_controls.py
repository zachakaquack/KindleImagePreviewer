from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QPushButton, QSizePolicy, QVBoxLayout
import webbrowser

# from widgets.controls.kindle_input import KindleInput
from widgets.controls.image_picker import ImagePicker
from widgets.controls.image_settings import ImageSettings
from widgets.controls.log import LogWidget


class MainControls(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setStyleSheet(
            """
            background-color: #303030;
            border-radius: 5px;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # self.kindle_input = KindleInput()
        # self.main_layout.addWidget(self.kindle_input)

        image_picker = ImagePicker()
        self.main_layout.addWidget(image_picker)

        image_settings = ImageSettings()
        self.main_layout.addWidget(image_settings)

        logger = LogWidget()
        self.main_layout.addWidget(logger)
