import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

import resources.gui_strings as s
from gui.patterns_view.pattern_view_toolbar import PatternViewToolBar
from gui.view_hierarchy import ViewHierarchy


class MainWindow(QMainWindow):
    """
    Responsible for managing the main window of this application. Contains the
    overall view hierarchy and the toolbar.

    Parameters:
        view_hierarchy:     the view hierarchy which is shown
        toolbar:            the toolbar for the pattern view

    Methods:
        __init__    MainWindow
    """

    def __init__(self):
        super().__init__()
        self.toolbar = PatternViewToolBar(self)
        self.view_hierarchy = ViewHierarchy(self.toolbar, self)

        self.setCentralWidget(self.view_hierarchy)
        self.addToolBar(self.toolbar)
        self.setWindowTitle(s.program_title())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
