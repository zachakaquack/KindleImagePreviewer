from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)
from other.signals import get_signals
from other.files import get_singleton


class ImagePicker(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            background-color: #303030;
            border-radius: 5px;
            """
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        if get_singleton("display_resolution_warning"):
            warning_label = QLabel(
                "Make sure to set your Resolution! (see: Settings, Help)"
            )
            warning_label.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
            )
            warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont("Calibri", 18)
            font.setUnderline(True)
            font.setBold(True)
            warning_label.setFont(font)
            self.main_layout.addWidget(warning_label)
            self.main_layout.addSpacing(15)

        self.image_picker_label = QLabel("Select your image...")
        self.image_picker_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.image_picker_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_picker_label.setFont(QFont("Calibri", 24))
        self.main_layout.addWidget(self.image_picker_label)

        self.image_path_label = QLabel("...")
        self.image_path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_path_label.setStyleSheet("color: hsl(0, 0%, 50%)")
        self.image_path_label.setFont(QFont("Calibri", 16))
        self.main_layout.addWidget(self.image_path_label)

        self.main_layout.addSpacing(25)

        self.image_picker_button = QPushButton("Select")
        self.image_picker_button.setFont(QFont("Calibri", 24))
        self.image_picker_button.setStyleSheet("background-color: #1e1e1e;")
        self.image_picker_button.clicked.connect(self._launch_dialog)
        self.image_picker_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.main_layout.addWidget(self.image_picker_button)

    def _prepare_file(self, file):
        self.image_path_label.setText(file)
        signal = get_signals()
        signal.image_chosen.emit(file)

    def _launch_dialog(self) -> None:
        dialog = QFileDialog(
            self,
        )
        dialog.setNameFilters(
            [
                "Images (*.png *.jpg *.jpeg *.webp)",
                "PNG (*.png)",
                "JPEG (*.jpeg)",
                "JPG (*.jpg)",
                "WEBP (*.webp)",
            ]
        )
        dialog.selectNameFilter("Images (*.png *.jpg *.jpeg *.webp)")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.fileSelected.connect(self._prepare_file)
        dialog.exec()
