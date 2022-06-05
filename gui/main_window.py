from PyQt6.QtWidgets import QStackedWidget, QWidget

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector import PatternSelectorLayout
from gui.patterns_layout.pattern_view_overview import PatternViewOverviewLayout


class MainWindow(QStackedWidget):
    """ Manages the main window for the GUI. This is where all layouts
    eventually stem from.

    """

    def __init__(self, istest=False):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.

        Parameters:
            selector_widget     QWidget     a basic widget containing the
                                                layout for the parent selector
            view_widget         QWidget     a default widget containing the
                                                layout for the pattern viewer
        """
        super().__init__()

        # Only show the window if this is not a test.
        if not istest:
            self.showMaximized()
        self.setWindowTitle(s.program_title())
        self.selector_widget = QWidget()
        self.selector_widget.setLayout(PatternSelectorLayout(self))
        self.view_widget = QWidget()

        self.addWidget(self.selector_widget)
        self.addWidget(self.view_widget)

    def pattern_chosen(self, pattern_name):
        """ Loads the default display window for this pattern.
        """
        self.view_widget.setLayout(
            PatternViewOverviewLayout(pattern_name, self))
        self.setCurrentWidget(self.view_widget)
