from PyQt6.QtWidgets import QHBoxLayout

from gui.stitching.pattern_prepare_stitching_view import PatternPrepareStitchingView


class StitchingViewOverlay(QHBoxLayout):
    pattern_view: PatternPrepareStitchingView
    parent: 'StitchingOverlay'

    def __init__(
            self, model: 'PrepareStitchingDisplayModel', parent: 'StitchingOverlay' = None):
        super().__init__()
        self.parent = parent
        self.pattern_view = PatternPrepareStitchingView(model, self)
        self.addWidget(self.pattern_view)
