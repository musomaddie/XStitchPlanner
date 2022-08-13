from PyQt6.QtWidgets import QStackedWidget, QWidget

from gui.stitching.current.current_stitching_view_overlay import CurrentStitchingViewOverlay
from gui.stitching.prepare.prepare_stitching_view_overlay import PrepareStitchingViewOverlay
from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import StartingCorner, TOP_LEFT


class StitchingViewOverlay(QStackedWidget):
    prepare_layout: PrepareStitchingViewOverlay
    stitching_layout: CurrentStitchingViewOverlay
    parent: 'StitchingOverlay'

    def __init__(self, model: 'PrepareStitchingDisplayModel', parent: 'StitchingOverlay' = None):
        super().__init__()
        self.parent = parent
        self.stitching_layout = None

        self.prepare_layout = PrepareStitchingViewOverlay(model, self)
        prepare_layout_widget = QWidget()
        prepare_layout_widget.setLayout(self.prepare_layout)
        self.addWidget(prepare_layout_widget)
        # TODO: shortcut added
        self.start_stitching(model._data, TOP_LEFT)

    def start_stitching(
            self, pattern_data: list[list[PatternCell]], starting_corner: StartingCorner):
        """ Starts the stitching for this pattern data. """
        stitcher = FullParkingStitcher(
            [[StitchingCell(cell) for cell in row] for row in pattern_data], starting_corner)

        self.stitching_layout = CurrentStitchingViewOverlay(stitcher, self)
        stitching_layout_widget = QWidget()
        stitching_layout_widget.setLayout(self.stitching_layout)
        self.addWidget(stitching_layout_widget)
        self.setCurrentWidget(stitching_layout_widget)
