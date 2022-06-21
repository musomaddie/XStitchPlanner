from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_selector.pattern_selector import PatternSelectorLayout
from gui.patterns_view.pattern_view_tab import PatternViewTab


class ViewHierarchy(QStackedWidget):
    """ Manages the main window for the GUI. This is where all layouts eventually stem from. """
    parent: 'MainWindow'
    toolbar_ref: 'PatternViewToolbar'
    model: PatternDisplayModel
    selector_widget: QWidget
    view_widget: QWidget

    def __init__(
            self,
            toolbar_ref: 'PatternViewToolbar',
            parent: 'MainWindow' = None):
        super().__init__()
        self.parent = parent
        self.toolbar_ref = toolbar_ref
        self.model = None

        self.selector_widget = QWidget()
        self.selector_widget.setLayout(PatternSelectorLayout(self))

        self.addWidget(self.selector_widget)

        self.pattern_chosen("hp")

    def pattern_chosen(self, pattern_name):
        """ Loads the default display window for this pattern.
        """
        self.model = PatternDisplayModel.load_from_pattern_file(pattern_name)
        self.view_widget = PatternViewTab(pattern_name, self.model, self)
        self.toolbar_ref.pattern_chosen(self.model)
        self.addWidget(self.view_widget)
        self.setCurrentWidget(self.view_widget)
