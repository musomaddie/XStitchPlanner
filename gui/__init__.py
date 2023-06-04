import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # app.setStyleSheet(generate_style_sheet("global"))
    # TODO: add some global stuff back here for styling (e.g. general button theme (?) anything particular is ignored.
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
