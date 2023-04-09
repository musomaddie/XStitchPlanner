from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_selector.pattern_selector import PatternSelectorLayout
from gui.patterns_view.pattern_view_tab_list import PatternViewTabList
from gui.stitching.prepare.prepare_stitching_display_model import PrepareStitchingDisplayModel
from gui.stitching.stitching_overlay import StitchingOverlay


class ViewHierarchy(QStackedWidget):
    """ Manages the main window for the GUI. This is where all layouts eventually stem from. """
    parent: 'MainWindow'
    model: PatternDisplayModel
    selector_widget: QWidget
    view_widget: QWidget
    stitching_layout: StitchingOverlay
    stitching_widget: QWidget

    def __init__(
            self,
            parent: 'MainWindow' = None):
        super().__init__()
        self.parent = parent
        self.model = None

        self.selector_widget = QWidget()
        self.selector_widget.setLayout(PatternSelectorLayout(self))

        self.addWidget(self.selector_widget)

        # TODO: Shortcuts added
        # self.pattern_chosen("hp")
        # self.load_stitch_view(
        #     "hp", PatternDisplayModel.load_from_pattern_file(
        #         "hp-row-between[126_392]-col-to[39]-variant"))

    def pattern_chosen(self, pattern_name: str) -> None:
        """ Loads the default display window for this pattern. """
        self.model = PatternDisplayModel.load_from_pattern_file(pattern_name)
        self.view_widget = PatternViewTabList(pattern_name, self.model, self)
        self.addWidget(self.view_widget)
        self.setCurrentWidget(self.view_widget)

    # TODO: update calls to use the data not the model
    def load_stitch_view(self, pattern_name: str, pattern_model: PatternDisplayModel) -> None:
        """ Loads the stitching technique window for the given pattern model and name."""
        self.stitching_layout = StitchingOverlay(
            pattern_name,
            PrepareStitchingDisplayModel(pattern_model._data),
            self)
        self.stitching_widget = QWidget()
        self.stitching_widget.setLayout(self.stitching_layout)
        self.addWidget(self.stitching_widget)
        self.setCurrentWidget(self.stitching_widget)
