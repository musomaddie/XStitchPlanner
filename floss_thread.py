from dataclasses import dataclass


@dataclass
class Thread:
    """
    A class for storing and interacting with all the threads used in the pattern
    as identified by the key.

    Parameters:
        dmc_value:      the value of the dmc identifier used for this thread
        identifier:      the unique symbol used to identify this thread when
                            reading from the pattern PDF
        symbol:         the unique symbol for displaying this thread in the
                            pattern, may not match the identifier
        name:           an English description of the colour of this thread
        hex_colour:     the colour of this thread in hex form
    """
    dmc_value: str
    identifier: str
    symbol: str
    name: str
    hex_colour: str
