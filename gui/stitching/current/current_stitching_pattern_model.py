from gui.pattern_model import PatternModel
from pattern_cells.stitching_cell import StitchingCell


class CurrentStitchingPatternModel(PatternModel):
    _data: list[list[StitchingCell]]

    def __init__(self, data: list[list[StitchingCell]]):
        super().__init__(data)
