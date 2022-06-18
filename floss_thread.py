from dataclasses import dataclass


@dataclass
class Thread:
    """
    A class for storing and interacting with all the threads used in the pattern as identified by
    the key.
    """
    dmc_value: str
    identifier: str
    symbol: str
    name: str
    hex_colour: str
