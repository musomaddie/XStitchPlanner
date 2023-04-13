from gui.pattern_view import PatternView


class CurrentStitchingPatternView(PatternView):
    def __init__(
            self,
            model: 'StitchingPatternModel',
            parent: 'CurrentStitchingViewOverlay' = None):
        super().__init__(model)
        self.setShowGrid(True)
        self.parent = parent
