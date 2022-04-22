from dataclasses import dataclass

@dataclass
class Thread:
    """ A class for storing and interacting with all the threads used in the
    pattern as identified by the key.

    Parameters:
        dmc_value   str     the value of the dmc identifier for this thread.
        identifier  str     the unique symbol used to identify this thread when
                            reading from the pattern PDF.
        symbol      str     the unique symbol for displaying in the pattern,
                             may not match the identifier.
        name        str     an English description of the colour of the thread
        hex_colour  str     the colour of the thread in hex form.
    """
    dmc_value: str
    identifier: str
    symbol: str
    name: str
    hex_colour: str
