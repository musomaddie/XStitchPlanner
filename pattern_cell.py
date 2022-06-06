from dataclasses import dataclass


@dataclass
class PatternCell:
    """ A class for storing and interacting with the cells in the pattern

    Parameters:
        display_symbol  str         the symbol for displaying
        dmc_value       str         the dmc color code for this cell
        index           [int,int]   the index of the cell overall (row, col)
        hex_colour      str         the hex colour of this cell
    """
    display_symbol: str
    dmc_value: str
    index: list
    hex_colour: str
