from typing import Any
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QFont, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QColorDialog,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from other import files
from other.signals import get_signals


class ImageSettings(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setStyleSheet(
            """
            background-color: #1e1e1e;
            border-radius: 5px;
            """
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(50)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # stretch box

        stretcher_settings = StretcherSettings()
        self.main_layout.addWidget(stretcher_settings)


class SettingsGroup(QFrame):
    radio_clicked = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(20, 0, 0, 0)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

    def add_child(self, widget: QWidget) -> None:
        self.main_layout.addWidget(widget)


class StretcherSettings(SettingsGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        settings = files.get_image_settings()
        signal = get_signals()
        signal.update_image_resolution.connect(self.update_slider_ranges)

        # actual stretching
        self.x_cb = CheckBox()
        self.x_cb.setChecked(settings["fit_x"])
        self.x_cb.clicked.connect(
            lambda: files.update_image_settings("fit_x", self.x_cb.isChecked())
        )

        self.y_cb = CheckBox()
        self.y_cb.setChecked(settings["fit_y"])
        self.y_cb.clicked.connect(
            lambda: files.update_image_settings("fit_y", self.y_cb.isChecked())
        )

        stretch_x = Pair("Fit X", self.x_cb)
        stretch_y = Pair("Fit Y", self.y_cb)

        self.add_child(stretch_x)
        self.add_child(stretch_y)

        # other stuff
        self.current_image_width = 0
        self.current_image_height = 0

        self.x_offset_slider = QSlider()
        # self.x_offset_slider.setValue(settings["offset_x"])
        self.x_offset_slider.setOrientation(Qt.Orientation.Horizontal)

        # the "zero" is centered
        self.x_offset_slider.mouseReleaseEvent = lambda _: files.update_image_settings(
            "offset_x", self.x_offset_slider.value()
        )

        self.y_offset_slider = QSlider()
        # self.y_offset_slider.setValue(settings["offset_y"])
        self.y_offset_slider.setOrientation(Qt.Orientation.Horizontal)
        self.y_offset_slider.mouseReleaseEvent = lambda _: files.update_image_settings(
            "offset_y", self.y_offset_slider.value()
        )

        reversed_layout: bool = True
        x_offset = Pair("X Offset", self.x_offset_slider, reversed_layout)
        y_offset = Pair("Y Offset", self.y_offset_slider, reversed_layout)

        self.add_child(x_offset)
        self.add_child(y_offset)

        # scale factor
        self.scale_slider = QSlider()
        self.scale_slider.setValue(settings["scale_factor"])
        self.scale_slider.setOrientation(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(1, 200)
        self.scale_slider.mouseReleaseEvent = lambda _: files.update_image_settings(
            "scale_factor", self.scale_slider.value()
        )

        reversed_layout: bool = True
        scale = Pair("Scale Factor", self.scale_slider, reversed_layout)

        self.add_child(scale)

        self.rotation = RotationPane()
        self.add_child(self.rotation)
        #

        reset_buttons = ResetButtons()
        reset_buttons.reset_x.connect(self._update_slider_values)
        reset_buttons.reset_y.connect(self._update_slider_values)
        reset_buttons.reset_scale.connect(self._update_slider_values)
        reset_buttons.center_x.connect(self._center_x)
        reset_buttons.center_y.connect(self._center_y)
        reset_buttons.center_both.connect(self._center_both)

        self.add_child(reset_buttons)

        self.color_picker = ColorPicker()
        self.add_child(self.color_picker)

    def _center_x(self) -> None:
        kindle = files.get_kindle()
        offset_x = (kindle.width // 2) - (self.current_image_width // 2)
        self.x_offset_slider.setValue(offset_x)
        files.update_image_settings("offset_x", offset_x)

    def _center_y(self) -> None:
        kindle = files.get_kindle()
        offset_y = (kindle.height // 2) - (self.current_image_height // 2)
        self.y_offset_slider.setValue(offset_y)
        files.update_image_settings("offset_y", offset_y)

    def _center_both(self) -> None:
        self._center_x()
        self._center_y()

    def _update_slider_values(self, kind: str) -> None:
        if kind == "reset_x":
            self.x_offset_slider.setValue(0)
            files.update_image_settings("offset_x", 0)

        elif kind == "reset_y":
            self.y_offset_slider.setValue(0)
            files.update_image_settings("offset_y", 0)
        else:
            self.scale_slider.setValue(100)
            files.update_image_settings("scale_factor", 100)

    def update_slider_ranges(self, image_width, image_height):
        kindle = files.get_kindle()

        x_min = -image_width
        x_max = kindle.width

        y_min = -image_height
        y_max = kindle.height

        self.x_offset_slider.setRange(x_min, x_max)
        self.y_offset_slider.setRange(y_min, y_max)

        self.current_image_width = image_width
        self.current_image_height = image_height


class ColorPicker(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )

        self.button = QPushButton("Open Color Picker")
        self.set_button_bg(
            QColor(
                str(files.get_image_settings()["fill_color"]),
            )
        )
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setFont(QFont("Calibri", 20))
        self.button.clicked.connect(self.open_color_dialog)
        self.main_layout.addWidget(self.button)

    def set_button_bg(self, color: QColor) -> None:
        gray = int(
            (color.red() * 0.299) + (color.green() * 0.587) + (color.blue() * 0.114)
        )
        alpha = color.alpha()

        gray_color = QColor(gray, gray, gray, alpha)
        self.button.setStyleSheet(
            f"""
            background-color: {gray_color.name(QColor.NameFormat.HexArgb)};
            color: white;
            padding: 5px;
            border: 1px solid white;
            """
        )

    def open_color_dialog(self) -> None:
        current_color = files.get_image_settings()["fill_color"]
        color = QColorDialog.getColor(
            current_color,
            title="Choose Background Color",
            options=QColorDialog.ColorDialogOption.ShowAlphaChannel,
        )
        if color.isValid():
            self.update_bg_color(color)
            self.set_button_bg(color)

    def update_bg_color(self, color: QColor) -> None:
        files.update_image_settings("fill_color", color.name(QColor.NameFormat.HexArgb))


class RotationPane(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )

        # slider
        settings = files.get_image_settings()
        self.rot_count = settings["rotation_count"]

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.mouseReleaseEvent = lambda _: files.update_image_settings(
            "rotation_offset", self.slider.value()
        )
        self.slider.setRange(-45, 45)
        self.slider.setValue(settings["rotation_offset"])

        left = QPushButton("Rotate -90")
        right = QPushButton("Rotate 90")
        reset = QPushButton("Reset")

        left.clicked.connect(self._go_left)
        right.clicked.connect(self._go_right)
        reset.clicked.connect(self._reset)

        font = QFont("Calibri", 20)
        for button in left, right, reset:
            button.setStyleSheet("background-color: #303030; padding: 5px;")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(font)

        self.main_layout.addWidget(left)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(right)
        self.main_layout.addWidget(reset)

    def _reset(self) -> None:
        self.rot_count = 0
        files.update_image_settings("rotation_count", self.rot_count)
        files.update_image_settings("rotation_offset", 0)
        self.slider.setValue(0)

    def _go_left(self) -> None:
        self.rot_count -= 1
        self.rot_count %= 4
        files.update_image_settings("rotation_count", self.rot_count)

    def _go_right(self) -> None:
        self.rot_count += 1
        self.rot_count %= 4
        files.update_image_settings("rotation_count", self.rot_count)


class ResetButtons(QFrame):
    reset_x = Signal(str)
    reset_y = Signal(str)
    reset_scale = Signal(str)

    center_x = Signal()
    center_y = Signal()
    center_both = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 10, 10, 0)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        reset_x_offset = QPushButton("Reset X Offset")
        reset_y_offset = QPushButton("Reset Y Offset")
        reset_scale_factor = QPushButton("Reset Scale Factor")

        reset_x_offset.clicked.connect(lambda: self.reset_x.emit("reset_x"))
        reset_y_offset.clicked.connect(lambda: self.reset_y.emit("reset_y"))
        reset_scale_factor.clicked.connect(lambda: self.reset_scale.emit("reset_scale"))

        center_x = QPushButton("Center X")
        center_y = QPushButton("Center Y")
        center_both = QPushButton("Center Both")

        center_x.clicked.connect(self.center_x.emit)
        center_y.clicked.connect(self.center_y.emit)
        center_both.clicked.connect(self.center_both.emit)

        self.top = QHBoxLayout()
        self.top.setContentsMargins(5, 5, 5, 5)
        self.top.setSpacing(5)
        self.top.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.bottom = QHBoxLayout()
        self.bottom.setContentsMargins(5, 5, 5, 5)
        self.bottom.setSpacing(5)
        self.bottom.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        font = QFont("Calibri", 20)
        for button in (
            reset_x_offset,
            reset_y_offset,
            reset_scale_factor,
            center_x,
            center_y,
            center_both,
        ):
            button.setFont(font)
            button.setStyleSheet("background-color: #303030; padding: 5px;")
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.top.addWidget(reset_x_offset)
        self.top.addWidget(reset_y_offset)
        self.top.addWidget(reset_scale_factor)

        self.bottom.addWidget(center_x)
        self.bottom.addWidget(center_y)
        self.bottom.addWidget(center_both)

        self.main_layout.addLayout(self.top)
        self.main_layout.addLayout(self.bottom)


class Pair(QFrame):
    def __init__(
        self, text: str, widget: QWidget, reversed_layout: bool = False, *args, **kwargs
    ):
        super().__init__(*args, *kwargs)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.label = QLabel(text)
        self.label.setFont(QFont("Calibri", 20))

        if reversed_layout:
            self.main_layout.addWidget(self.label)
            self.main_layout.addWidget(widget)
        else:
            self.main_layout.addWidget(widget)
            self.main_layout.addWidget(self.label)


class CheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setObjectName("checkbox")
        self.setStyleSheet("""
        QCheckBox::indicator:enabled {
            width: 40px; height: 40px;
            color: white;
        }
        QCheckBox::indicator:disabled {
            width: 40px; height: 40px;
            color: white;
        }
        """)
