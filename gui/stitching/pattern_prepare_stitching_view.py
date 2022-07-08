from gui.pattern_view import PatternView
from gui.stitching.prepare_stitching_display_model import PrepareStitchingDisplayModel


class PatternPrepareStitchingView(PatternView):
    model: PrepareStitchingDisplayModel
    parent: 'StitchingViewOverlay'

    def __init__(self, model: PrepareStitchingDisplayModel, parent: 'StitchingViewOverlay' = None):
        super().__init__(model)
        self.parent = parent
