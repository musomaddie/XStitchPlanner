from PyQt6.QtWidgets import QWidget
from gui.pattern_selector_layout import create_pattern_selector_layout
from gui.pattern_selector_layout import PatternSelectorLayout

class MainWindow(QWidget):
    def __init__(self):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.
        """
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Stitch Please!")

        self.setLayout(PatternSelectorLayout())
