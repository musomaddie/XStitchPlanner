from PyQt6.QtWidgets import QWidget

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector import PatternSelectorLayout


class MainWindow(QWidget):
    def __init__(self, istest=False):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.
        """
        super().__init__()

        # Only show the window if this is not a test.
        if not istest:
            self.showMaximized()
        self.setWindowTitle(s.program_title())

        self.setLayout(PatternSelectorLayout(self))

    def pattern_chosen(self, pattern_name):
        """ Loads the default display window for this pattern.
        """
        pass
