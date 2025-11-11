from PySide6.QtGui import QImage, QPixmap, Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout
from pathlib import Path
from other import image_manip
from other import files
from other.signals import get_signals
from other.notifications import get_notification_daemon


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

        self.path = ""
        self.image_daemon = get_signals()
        self.image_daemon.image_chosen.connect(self.set_image_path)
        self.image_daemon.image_settings_changed.connect(self.redo_image)
        self.image_daemon.export_image.connect(self.export_image)
        self.image_daemon.refresh_image.connect(self.redo_image)

        self.actual_image: QImage | None = None

    def export_image(self) -> None:
        notif = get_notification_daemon()
        new_path = files.create_export_path(Path(self.path))

        if self.actual_image and self.path:
            self.actual_image.save(f"{new_path}")
            notif.new_message.emit(f"Image Created at {new_path}!")
        else:
            notif.new_message.emit(
                "Cannot create invalid image! Select an image first!"
            )

    def redo_image(self) -> None:
        self.set_image_path(self.path)

    def set_image_path(self, path: str) -> None:
        if path == "":
            return

        self.path = path

        text_image, actual_image = image_manip.scale_image(Path(path))
        pm = QPixmap.fromImage(text_image)

        self.actual_image = actual_image
        self.screen_label.setPixmap(pm)
