from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.patterns_selector.pattern_selector import PatternSelectorLayout
from gui.patterns_view.pattern_view_overview import \
    PatternViewOverviewLayout


class ViewHierarchy(QStackedWidget):
    """ Manages the main window for the GUI. This is where all layouts
    eventually stem from.

    """

    def __init__(self, parent=None):
        """ Initialises the main window. This is the GUI contain that contains
        all the elements of the program.

        Parameters:
            parent              MainWindow
            selector_widget     QWidget     a basic widget containing the
                                                layout for the parent selector
            view_widget         QWidget     a default widget containing the
                                                layout for the pattern viewer
        """
        super().__init__()

        self.parent = parent

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
