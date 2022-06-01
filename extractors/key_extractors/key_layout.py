from dataclasses import dataclass
from enum import Enum, auto
from string import punctuation


class KeyForm(Enum):
    """ A enum to represent the (currently) three different ways that the key
    can be read from the PDF.

    FULL_LINES          finds a table using full vertical and horizontal lines
    ONLY_HEADER_LINE    finds a table where the only visible line is the
                        vertical header line
    NO_LINES            finds a table that has no lines at all
    UNKNOWN             the value received is not recognised
    """

    def from_string(string):
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
    """ A data class for storing information about the layout of the key.
    key_form            KeyForm     the form that the key takes on the page
    filled_rects         bool    whether the rectangles that contain the images
                                are filled with color or not [default: False]
    n_rows_start        int     the row where the key starts on the first page
    n_rows_end          int     the row where the key stops on the first page
    n_rows_start_pages  int     the number of the row where the key starts for
                                the pages that aren't the first page. 0 if this
                                is not a multi-page key.

    n_rows_end_pages    int     the row where the key ends for pages that
                                aren't the first page. 0 if this is not a
                                multi-page key.
    headings            list[str]   an ordered list of every heading in the key
                                    column.
    """
    key_form: KeyForm
    filled_rects: bool
    n_rows_start: int
    n_rows_end: int
    n_rows_start_pages: int
    n_rows_end_pages: int
    n_colours_per_row: int
    headings: list[str]
