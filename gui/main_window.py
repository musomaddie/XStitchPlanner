from PyQt6.QtWidgets import QWidget

from gui.patterns_layout.pattern_selector import PatternSelectorLayout


class MainWindow(QWidget):
    def __init__(self):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.
        """
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Stitch Please!")

        self.setLayout(PatternSelectorLayout(self))

    def pattern_chosen(self, pattern_name):
        """ Loads the default display window for this pattern.
        """
        pass
