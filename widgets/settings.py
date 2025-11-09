from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)

from other import files
from other.signals import get_signals
from pathlib import Path


class SettingsPage(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            """
            background-color: #303030;
            color: white;
            border-radius: 5px;
            """
        )

        self.main_widget = QFrame()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

        title_font = QFont("Calibri", 20)
        title_font.setUnderline(True)
        title_font.setBold(True)

        _string: str = "Hover over the title above the settings for more information!"
        label = QLabel(_string)
        label.setFixedHeight(50)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Calibri", 16))
        label.setStyleSheet("border-bottom: 1px solid white; border-radius: 0px;")
        self.main_layout.addWidget(label)

        description = 'Enter the resolution of your kindle.\nMake sure to follow the help guide in the bottom left corner, then look for "How to find your Kindle Resolution"'
        resolution = TitleLabel(title_font, description, "Kindle Resolution")
        self.main_layout.addWidget(resolution)
        resolution_inputter = ResolutionInputter()
        self.main_layout.addWidget(resolution_inputter)

        description = f"Settings for the prefix and suffix of the file exported.\nThe image is exported @ {Path.cwd()}/images"
        resolution = TitleLabel(title_font, description, "File Exporting")
        self.main_layout.addWidget(resolution)
        other_settings = OtherSettings()
        self.main_layout.addWidget(other_settings)

        _string: str = "Invidiual Settings"
        seperator = QLabel(_string)
        seperator.setFixedHeight(50)
        seperator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        seperator.setFont(QFont("Calibri", 16))
        seperator.setStyleSheet("border-bottom: 1px solid white; border-radius: 0px;")
        self.main_layout.addWidget(seperator)

        description = "Whether or not to display the warning about setting the resolution of your kindle on startup"
        resolution = TitleLabel(title_font, description, "Display Resolution Warning")
        self.main_layout.addWidget(resolution)
        display_resolution_warning = SingletonSwitcher("display_resolution_warning")
        self.main_layout.addWidget(display_resolution_warning)


class TitleLabel(QLabel):
    def __init__(self, font, description: str, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFont(font)
        self.setToolTip(description)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class SingletonSwitcher(QFrame):
    def __init__(self, key: str, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            QFrame{
                background-color: #1e1e1e;
            }
            QPushButton{
                background-color: #353030;
            }
            """
        )

        self.on = files.get_singleton("display_resolution_warning")

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.on_button = QPushButton("On")
        self.off_button = QPushButton("Off")

        font = QFont("Calibri", 24)
        for button in (self.on_button, self.off_button):
            button.setFont(font)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            button.setStyleSheet("background-color: #303030;")

        self.main_layout.addWidget(self.on_button)
        self.main_layout.addWidget(self.off_button)

        self.on_button.clicked.connect(self.toggle_on)
        self.off_button.clicked.connect(self.toggle_off)

        # initial thing
        if self.on:
            self.on_button.setStyleSheet("color: green;")
            self.off_button.setStyleSheet("color: gray;")
        else:
            self.on_button.setStyleSheet("color: gray;")
            self.off_button.setStyleSheet("color: red;")

    def toggle_off(self):
        self.on = False
        files.update_singleton("display_resolution_warning", self.on)

        self.on_button.setStyleSheet("color: gray;")
        self.off_button.setStyleSheet("color: red;")

    def toggle_on(self):
        self.on = True
        files.update_singleton("display_resolution_warning", self.on)

        self.on_button.setStyleSheet("color: green;")
        self.off_button.setStyleSheet("color: gray;")


class ResolutionInputter(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            background-color: #1e1e1e;
            """
        )

        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        width_label = QLabel("Kindle Width (px)")
        height_label = QLabel("Kindle Height (px)")

        width_input = QLineEdit(inputMask="9999", placeholderText="Width (px)")
        height_input = QLineEdit(inputMask="9999", placeholderText="Height (px)")

        width_input.textChanged.connect(files.update_kindle_width)
        height_input.textChanged.connect(files.update_kindle_height)

        kindle = files.get_kindle()
        width_input.setText(str(kindle.width))
        height_input.setText(str(kindle.height))

        font = QFont("Calibri", 24)
        for label in (width_label, height_label):
            label.setFont(font)

        font = QFont("Calibri", 16)
        for input in (width_input, height_input):
            input.setStyleSheet("background-color: #303030;")
            input.setFont(font)

        for widget in (width_label, width_input, height_label, height_input):
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(width_label, 0, 0)
        self.main_layout.addWidget(width_input, 1, 0)

        self.main_layout.addWidget(height_label, 0, 1)
        self.main_layout.addWidget(height_input, 1, 1)


class OtherSettings(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet("background-color: #1e1e1e;")
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.image_path: str = "<IMAGE>"

        self.signals = get_signals()
        self.signals.image_chosen.connect(self._set_image_name)

        self.prefix_input: QLineEdit = QLineEdit(files.get_prefix())
        self.suffix_input: QLineEdit = QLineEdit(files.get_suffix())

        font = QFont("Calibri", 16)
        for input in (self.prefix_input, self.suffix_input):
            input.setFont(font)
            input.textChanged.connect(self._edit_preview)
            input.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            input.setStyleSheet("background-color: #303030;")

        self.preview_label = QLabel()
        self.prefix_label = QLabel("Enter Image Prefix")
        self.suffix_label = QLabel("Enter Image Suffix")
        self._edit_preview()

        font = QFont("Calibri", 24)
        for label in (self.preview_label, self.prefix_label, self.suffix_label):
            label.setFont(font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.preview_label, 0, 0, 1, 2)
        self.main_layout.addWidget(self.prefix_label, 1, 0)
        self.main_layout.addWidget(self.prefix_input, 2, 0)

        self.main_layout.addWidget(self.suffix_label, 1, 1)
        self.main_layout.addWidget(self.suffix_input, 2, 1)

    def _set_image_name(self, name: str) -> None:
        self.image_path = f"{Path(name).stem}"
        self._edit_preview()

    def _edit_preview(self) -> None:
        files.update_prefix_suffix(self.prefix_input.text(), self.suffix_input.text())
        text = (
            f"{self.prefix_input.text()}{self.image_path}{self.suffix_input.text()}.png"
        )
        self.preview_label.setText(text)
