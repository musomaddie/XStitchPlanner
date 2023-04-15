from PyQt6.QtWidgets import QMainWindow

from gui.layouts.contents import Contents


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO: style window title.
        self.setWindowTitle("Stitch Please!")

        self.setCentralWidget(Contents())
