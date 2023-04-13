from dataclasses import dataclass


@dataclass
class PatternCell:
    """ A class for storing and interacting with the cells in the pattern """
    display_symbol: str
    dmc_value: str
    # TODO: consider making this a custom class for my ease of use
    index: tuple[int, int]
    hex_colour: str


def missing_thread(x, y):
    return PatternCell("", "0", (x, y), "FFFFFF")
