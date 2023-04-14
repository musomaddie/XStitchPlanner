from PyQt6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stitch Please!")

        tmp = QLabel("Hello world")
        self.setCentralWidget(tmp)
        self.setStyleSheet(self._read_stylesheet())

    @staticmethod
    def _read_stylesheet():
        with open("styles.qss") as f:
            return f.read()
