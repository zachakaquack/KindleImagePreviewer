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
            background-color: #1e1e1e;
            border-radius: 5px;
            """
        )
        self.setMaximumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
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

        self.image_picker_button = QPushButton("Select your image...")
        self.image_picker_button.setFont(QFont("Calibri", 24))
        self.image_picker_button.setStyleSheet(
            "background-color: #303030; padding: 5px;"
        )
        self.image_picker_button.clicked.connect(self._launch_dialog)
        self.image_picker_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.image_picker_button)

        self.image_exporter_button = QPushButton("Export Image")
        self.image_exporter_button.setFont(QFont("Calibri", 24))
        self.image_exporter_button.setStyleSheet(
            "background-color: #303030; padding: 5px;"
        )
        self.image_exporter_button.clicked.connect(self._export_image)
        self.image_exporter_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.image_exporter_button)

        self.image_path_label = QLabel("...")
        self.image_path_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.image_path_label.setWordWrap(True)
        # self.image_path_label.setFixedWidth(500)
        self.image_path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_path_label.setStyleSheet("color: hsl(0, 0%, 50%)")
        self.image_path_label.setFont(QFont("Calibri", 16))
        self.main_layout.addWidget(self.image_path_label)

    def _export_image(self) -> None:
        signal = get_signals()
        signal.export_image.emit()

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
