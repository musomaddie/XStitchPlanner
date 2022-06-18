from dataclasses import dataclass
from enum import Enum, auto
from string import punctuation


class KeyForm(Enum):
    """ An enum to represent the (currently) three different ways that the key
    can be read from the PDF.

    FULL_LINES:         finds a table using full vertical and horizontal lines
    ONLY_HEADER_LINE:   finds a table where the only visible line is the vertical
                            header line
    NO_LINES:           finds a table that has no lines at all
    UNKNOWN:            the value received is not recognised
    """

    @staticmethod
    def from_string(string: str) -> 'KeyForm':
        """ Converts a string into a KeyForm """
        string = string.lower().translate(
            str.maketrans('', '', punctuation)).replace(" ", "").replace("\t", "")

        for opt in KeyForm:
            if string == opt.value:
                return opt
        return KeyForm.UNKNOWN

    FULL_LINES = "fulllines"
    ONLY_HEADER_LINE = "onlyheaderline"
    NO_LINES = "nolines"
    UNKNOWN = auto()


@dataclass
class KeyLayout:
    """
    A data class for storing information about the layout of the key.
    Parameters:
        key_form: the form this key file takes
        n_rows_start: the row where the key starts on the 1st page
        n_rows_end: the row where the key stops on the 1st page
        n_rows_start_pages: the row where the key starts for the pages that aren't the first page
        n_rows_end_pages: the row where the key ends for pages that aren't the first page
        headings: an ordered list of every heading in the key column
    """
    key_form: KeyForm
    n_rows_start: int
    n_rows_end: int
    n_rows_start_pages: int
    n_rows_end_pages: int
    n_colours_per_row: int
    headings: list[str]
