from pattern_cells.pattern_cell import PatternCell


class StitchingCell(PatternCell):
    """A class for storing and interacting with the cells as the stitching technique is being
    processed"""
    stitched: bool
    parked: bool

    def __init__(self, display_symbol: str, dmc_value: str):
        super().__init__(display_symbol, dmc_value, [], "")
        self.display_symbol = display_symbol
        self.dmc_value = dmc_value
        self.stitched = False
        self.parked = False

    def __eq__(self, other: 'StitchingCell') -> bool:
        return self.display_symbol == other.display_symbol

    def __repr__(self):
        return f"{self.display_symbol} (s)"
