from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.stitching.prepare.pattern_prepare_stitching_view import PatternPrepareStitchingView
from gui.stitching.prepare.pre_stitching_options_overlay import PreStitchingOptionsOverlay
from stitchers.starting_corner import StartingCorner


class PrepareStitchingViewOverlay(QHBoxLayout):
    pattern_view: PatternPrepareStitchingView
    options_view: PreStitchingOptionsOverlay
    parent: 'StitchingViewOverlay'

    def __init__(
            self, model: 'PrepareStitchingDisplayModel', parent: 'StitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent
        self.pattern_view = PatternPrepareStitchingView(model, self)
        self.addWidget(self.pattern_view)

        self.options_view = PreStitchingOptionsOverlay(self)
        options_view_layout_widget = QWidget()
        options_view_layout_widget.setLayout(self.options_view)
        # TODO: make more dynamic
        options_view_layout_widget.setMinimumSize(
            300, options_view_layout_widget.minimumSize().height())
        self.addWidget(options_view_layout_widget)

    def start_stitching(self, starting_corner: StartingCorner):
        """ Starts stitching this pattern and changes the layout to reflect this """
        self.parent.start_stitching(self.pattern_view.model._data, starting_corner)
