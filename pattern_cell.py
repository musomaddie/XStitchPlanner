from dataclasses import dataclass


@dataclass
class PatternCell:
    """
    A class for storing and interacting with the cells in the pattern

    Parameters:
        display_symbol:     the symbol for displaying
        dmc_value:          the dmc_colour code for this cell
        index:              the index of this cell overall (row, col)
        hex_colour:         the hex colour of this cell based on the dmc_value
    """
    display_symbol: str
    dmc_value: str
    index: tuple[int, int]
    hex_colour: str
