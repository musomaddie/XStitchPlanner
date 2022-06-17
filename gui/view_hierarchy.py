from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_selector.pattern_selector import PatternSelectorLayout
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


class ViewHierarchy(QStackedWidget):
    """ Manages the main window for the GUI. This is where all layouts
    eventually stem from.
    """
    parent: 'MainWindow'
    toolbar_ref: 'PatternViewToolbar'
    model: PatternDisplayModel
    selector_widget: QWidget
    view_widget: QWidget

    def __init__(
            self, toolbar_ref: 'PatternViewToolbar',
            parent: 'MainWindow' = None):
        super().__init__()
        self.parent = parent
        self.toolbar_ref = toolbar_ref
        self.pattern_model = None

        self.selector_widget = QWidget()
        self.selector_widget.setLayout(PatternSelectorLayout(self))
        self.view_widget = QWidget()

        self.addWidget(self.selector_widget)
        self.addWidget(self.view_widget)

        self.pattern_chosen("hp")

    def pattern_chosen(self, pattern_name):
        """ Loads the default display window for this pattern.
        """
        self.pattern_model = PatternDisplayModel.load_from_pattern_file(
            pattern_name)
        self.toolbar_ref.pattern_chosen(self.pattern_model)
        self.view_widget.setLayout(
            PatternDisplayOverlay(pattern_name, self.pattern_model, self))
        self.setCurrentWidget(self.view_widget)
