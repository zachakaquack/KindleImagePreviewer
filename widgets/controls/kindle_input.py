from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
)
from other import files


class KindleInput(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFixedHeight(300)

        self.setStyleSheet(
            """
            background-color: #303030;
            color: white;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.width_input = self._Inputter("Enter Kindle Width:")
        self.height_input = self._Inputter("Enter Kindle Height:")

        kindle = files.get_kindle()
        self.width_input.input.setText(f"{kindle.width}")
        self.height_input.input.setText(f"{kindle.height}")

        self.width_input.input.textChanged.connect(files.update_kindle_width)
        self.height_input.input.textChanged.connect(files.update_kindle_height)

        self.main_layout.addWidget(self.width_input)
        self.main_layout.addWidget(self.height_input)

    class _Inputter(QFrame):
        def __init__(self, text, *args, **kwargs):
            super().__init__(*args, *kwargs)

            self.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            self.main_layout = QVBoxLayout(self)
            self.setLayout(self.main_layout)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setSpacing(0)
            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.label = QLabel(text)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setFont(QFont("Calibri", 24))
            self.main_layout.addWidget(self.label)

            self.input = QLineEdit()
            self.input.setMinimumSize(150, 50)
            self.input.setSizePolicy(
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
            )
            self.input.setFont(QFont("Calibri", 16))
            self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.input.setInputMask("9999")
            self.main_layout.addWidget(self.input)
