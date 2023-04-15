from PyQt6.QtWidgets import QMainWindow

from gui.layouts.contents import Contents


def read_stylesheet():
    with open("styles.qss") as f:
        return f.read()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO: style window title.
        self.setStyleSheet(self._read_stylesheet())
        self.setWindowTitle("Stitch Please!")
        self.setObjectName("testing")

        self.setCentralWidget(Contents())

    @staticmethod
    def _read_stylesheet():
        with open("styles.qss") as f:
            return f.read()
