from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication
import sys

from widgets.interface import Interface


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # a bit smaller than 1920x1080, same aspect ratio tho
        self.setFixedSize(1664, 936)
        self.interface = Interface()
        self.setCentralWidget(self.interface)

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
