from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)


class HelpPage(QScrollArea):
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
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

        steps = [
            'Click on the "Browser" (globe) button on the left, or go to this link: https://en.wikipedia.org/wiki/Amazon_Kindle#Specifications',
            "Scroll down to the chart",
            'Find your Kindle\'s model and its matching generation (see: "How to find your Kindle Model")',
            'Find the resolution (5th white column, under "Display")',
            "Input these values (widthxheight) into the settings",
            'For example, my Kindle Paperwhite 10 is "600x800", so I will input a width of 600, and height of 800',
        ]
        help_resolution = HelpItem("How to find your Kindle Resolution", steps)
        self.main_layout.addWidget(help_resolution)

        steps = [
            "Go to your kindle's home page (not KOReader)",
            "Click on the three dots to find your settings",
            "Click on Settings",
            "Click on Device options",
            "Click on Device info",
            'Read "Device type"',
        ]
        help_resolution = HelpItem("How to find your Kindle Model", steps)
        self.main_layout.addWidget(help_resolution)

        steps = [
            "Open KOReader",
            'Ensure your backgrounds directory is created (see: "How to make your Backgrounds Directory")',
            "Open any book",
            "Tap the top of the screen",
            "Tap the Cog wheel (3rd to left)",
            "Navigate: Screen -> Sleep screen -> Wallpaper",
            'Turn on "Show custom image or cover on sleep screen" or "Show random image from folder on sleep screen"',
            "Navigate: Custom images -> Choose image or document cover -> Choose file",
            "Navigate to your backgrounds directory",
            "Hold press on your image, then Choose",
        ]
        help_resolution = HelpItem("How to set your Sleep Screen", steps)
        self.main_layout.addWidget(help_resolution)

        steps = [
            "Open KOReader",
            "Navigate to your Kindle's directory view",
            'If you\'re in a book, then tap of the top of the screen -> tap on the "Bin" icon',
            "Navigate to where you want your directory to be (for example, mine is /mnt/us)",
            "Click on the Plus icon in the top right",
            'Click on "New Folder", then enter whatever name',
            "Your directory is now created! (mine is: /mnt/us/bgs/)",
        ]
        help_resolution = HelpItem("How to make your Backgrounds Directory", steps)
        self.main_layout.addWidget(help_resolution)


class HelpItem(QFrame):
    def __init__(self, title: str, steps: list[str], *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setStyleSheet(
            """
            background-color: #1e1e1e;
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        title_label = QLabel(f"{title}")
        font = QFont("Calibri", 20)
        font.setUnderline(True)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        self.steps_widget = QFrame()
        self.steps_layout = QVBoxLayout(self.steps_widget)
        self.steps_widget.setLayout(self.steps_layout)
        self.steps_layout.setContentsMargins(5, 5, 5, 5)
        self.steps_layout.setSpacing(10)
        self.steps_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        font = QFont("Calibri", 16)
        for step in steps:
            label = QLabel(f"{step}")
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            label.setFixedWidth(600)
            label.setWordWrap(True)

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(font)
            self.steps_layout.addWidget(label)

        self.main_layout.addWidget(self.steps_widget)
