from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QHBoxLayout
from widgets.kindle.kindle_interface import KindleInterface
from widgets.controls.controls_interface import ControlsInterface


class Interface(QFrame):
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
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.controls = ControlsInterface()
        self.main_layout.addWidget(self.controls)

        self.kindle = KindleInterface()
        self.main_layout.addWidget(self.kindle)
