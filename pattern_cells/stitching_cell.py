from pattern_cells.pattern_cell import PatternCell


class StitchingCell(PatternCell):
    """A class for storing and interacting with the cells as the stitching technique is being
    processed"""
    stitched: bool
    parked: bool

    def __init__(self, original_cell: PatternCell):
        super().__init__(
            original_cell.display_symbol,
            original_cell.dmc_value,
            original_cell.index,
            original_cell.hex_colour)
        self.stitched = False
        self.parked = False

    def __eq__(self, other: 'StitchingCell') -> bool:
        return self.display_symbol == other.display_symbol

    def __repr__(self):
        return f"{self.display_symbol} (s)"
