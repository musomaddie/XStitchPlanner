from dataclasses import dataclass


@dataclass
class PatternCell:
    """ A class for storing and interacting with the cells in the pattern """
    display_symbol: str
    dmc_value: str
    index: tuple[int, int]
    hex_colour: str
