from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.stitching.current.current_stitching_pattern_model import CurrentStitchingPatternModel
from gui.stitching.current.current_stitching_pattern_view import CurrentStitchingPatternView
from gui.stitching.current.options.current_stitching_options_overlay import \
    CurrentStitchingOptionsOverlay
from stitchers.OLD_full_parking_stitcher import FullParkingStitcher


class CurrentStitchingViewOverlay(QHBoxLayout):
    options_view: CurrentStitchingOptionsOverlay
    stitcher: 'FullParkingStitcher'
    model: CurrentStitchingPatternModel
    pattern_view: CurrentStitchingPatternView
    parent: 'StitchingViewOverlay'

    def __init__(
            self,
            stitcher: 'FullParkingStitcher',
            parent: 'StitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent

        self.stitcher = stitcher
        self.model = CurrentStitchingPatternModel(stitcher)
        self.pattern_view = CurrentStitchingPatternView(self.model)
        self.addWidget(self.pattern_view)

        self.options_view = CurrentStitchingOptionsOverlay(stitcher, self)
        options_view_layout_widget = QWidget()
        options_view_layout_widget.setLayout(self.options_view)
        options_view_layout_widget.setMinimumSize(
            300, options_view_layout_widget.minimumSize().height())
        self.addWidget(options_view_layout_widget)
