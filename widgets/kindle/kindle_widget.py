from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout
from pathlib import Path
from other import image_manip
from other import files
from other.signals import get_signals


class KindleWidget(QFrame):
    def __init__(self, target_size: tuple[int, int], *args, **kwargs):
        super().__init__(*args, *kwargs)

        kindle = files.get_kindle()
        kindle_screen_size = kindle.width, kindle.height

        width_ratio = target_size[0] / kindle_screen_size[0]
        height_ratio = target_size[1] / kindle_screen_size[1]
        scaling_factor = min(width_ratio, height_ratio)

        new_width = int(kindle_screen_size[0] * scaling_factor)
        new_height = int(kindle_screen_size[1] * scaling_factor)

        self.setFixedSize(new_width, new_height)

        self.setStyleSheet(
            """
            background-color: black;
            color: white;
            border-radius: 5px;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kindle_screen = KindleScreen()
        kindle = files.get_kindle()
        self.kindle_screen.setFixedSize(kindle.width, kindle.height)
        self.main_layout.addWidget(self.kindle_screen)


class KindleScreen(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            background-color: hsl(0, 0%, 10%);
            color: white;
            border-radius: 0px;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.screen_label = QLabel()
        self.screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addWidget(self.screen_label)

        self.image_daemon = get_signals()
        self.image_daemon.image_chosen.connect(self.image_fill_transparent)

    def image_fill_transparent(self, path: str):
        new_path = image_manip.resize_image_fill_transparent(Path(path))
        pm = QPixmap(f"{new_path}")
        self.screen_label.setPixmap(pm)
