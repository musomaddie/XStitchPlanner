import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.showMaximized()
sys.exit(app.exec())
