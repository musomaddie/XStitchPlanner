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
    def from_string(string):
        """ Converts a string into a KeyForm.
        Args:
            string:     the string to convert

        Returns:
            KeyForm     the KeyForm described by the string
        """
        string = string.lower().translate(
            str.maketrans('', '', punctuation)
        ).replace(" ", "").replace("\t", "")

        if string == "fulllines":
            return KeyForm.FULL_LINES
        elif string == "onlyheaderline":
            return KeyForm.ONLY_HEADER_LINE
        elif string == "nolines":
            return KeyForm.NO_LINES
        return KeyForm.UNKNOWN

    FULL_LINES = auto()
    ONLY_HEADER_LINE = auto()
    NO_LINES = auto()
    UNKNOWN = auto()


@dataclass
class KeyLayout:
    """
    A data class for storing information about the layout of the key.
    Parameters:
        key_form(KeyForm):          the form this key file takes
        n_rows_start(int):          the row where the key starts on the 1st page
        n_rows_end(int):            the row where the key stops on the 1st page
        n_rows_start_pages(int):    the row where the key starts for the pages
                                        that aren't the first page
        n_rows_end_pages(int):      the row where the key ends for pages that
                                        aren't the first page
        headings(list[str]):        an ordered list of every heading in the key
                                        column
    """
    key_form: KeyForm
    n_rows_start: int
    n_rows_end: int
    n_rows_start_pages: int
    n_rows_end_pages: int
    n_colours_per_row: int
    headings: list[str]
