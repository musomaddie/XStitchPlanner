class StitchingCell:
    """A class for storing and interacting with the cells as the stitching technique is being
    processed"""
    display_symbol: str
    dmc_value: str
    stitched: bool
    parked: bool

    # TODO: I think I will need the index of this cell when it comes to displaying this in the GUI

    def __init__(self, display_symbol: str, dmc_value: str):
        self.display_symbol = display_symbol
        self.dmc_value = dmc_value
        self.stitched = False
        self.parked = False

    def __eq__(self, other: 'StitchingCell') -> bool:
        return self.display_symbol == other.display_symbol

    def __repr__(self):
        return f"{self.display_symbol} (s)"
