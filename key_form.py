from enum import Enum, auto

class KeyForm(Enum):
    """ Determines how the key is to be extracted from the pdf.

    TABLE:      looks for a literal table in the pdf with both horizontal and
                vertical lines.
    LINE:       extracts the text straight from the PDF and splits it into
                rows. Requires ExtractorMode.FONT (currently).
    UNKNOWN:    the value received is not recognised.
    """

    def find_form_from_string(string):
        string = string.lower()
        if string == "table":
            return KeyForm.TABLE
        elif string == "line":
            return KeyForm.LINE
        else:
            return KeyForm.UNKNOWN
    TABLE = auto()
    LINE = auto()
    UNKNOWN = auto()
