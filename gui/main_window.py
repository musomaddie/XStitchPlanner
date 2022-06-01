from PyQt6.QtWidgets import QWidget

from gui.layout.pattern_selector import PatternSelectorLayout


class MainWindow(QWidget):
    def __init__(self):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.
        """
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Stitch Please!")

        self.setLayout(PatternSelectorLayout())