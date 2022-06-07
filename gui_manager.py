import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

import resources.gui_strings as s
from gui.view_hierarchy import ViewHierarchy


class MainWindow(QMainWindow):
    """ Responsible for managing the main window of this application.
    Contains the overall view hierarchy and the toolbar.

    Parameters:
        view_hierarchy  ViewHierarchy       the view hierarchy which is shown
        toolbar         PatternViewToolBar  the toolbar for the pattern view

    Methods:
        __init__    MainWindow
    """

    def __init__(self):
        super().__init__()
        self.view_hierarchy = ViewHierarchy(self)
        self.setCentralWidget(self.view_hierarchy)
        self.setWindowTitle(s.program_title())
        # TODO: attach toolbar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
