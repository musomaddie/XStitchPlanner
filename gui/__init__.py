import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow

app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet(open("styles/global_styles.qss").read())
window = MainWindow()
window.showMaximized()
sys.exit(app.exec())
