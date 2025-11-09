from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout
from widgets.kindle.kindle_widget import KindleWidget


class KindleInterface(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFixedHeight(936)
        # self.setFixedSize(936, 936)
        self.setStyleSheet(
            """
            background-color: #303030;
            color: white;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        window_size: tuple[int, int] = (936, 936)
        self.kindle = KindleWidget(window_size)
        self.main_layout.addWidget(self.kindle)
