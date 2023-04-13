from pattern_cells.pattern_cell import PatternCell
from pattern_cells.started_from import StartedFrom


class StitchingCell(PatternCell):
    """A class for storing and interacting with the cells as the stitching technique is being
    processed"""
    latest_stitched: bool
    stitched: bool
    parked: bool
    to_start_with: bool

    def __init__(self, original_cell: PatternCell):
        super().__init__(
            original_cell.display_symbol,
            original_cell.dmc_value,
            original_cell.index,
            original_cell.hex_colour)
        self.latest_stitched = False
        self.stitched = False
        self.parked = False
        self.to_start_with = False
        self.started_from = StartedFrom.NOT_STARTED

    def stitch(self, started_from: StartedFrom):
        self.latest_stitched = True
        self.stitched = True
        self.started_from = started_from

    def __eq__(self, other: 'StitchingCell') -> bool:
        return self.display_symbol == other.display_symbol

    def __repr__(self):
        return f"{self.display_symbol} (s)"
