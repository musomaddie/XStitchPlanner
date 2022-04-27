from enum import Enum, auto

class ExtractorMode(Enum):
    """ Determines how the pattern is to be read from the pdf.

    FONT:    identifies symbols in the pattern by extracting the text from the
             PDF.
    SHAPE:   extract symbols from the PDF by attempting to identify and match
             reoccuring lines and shapes on the page.
    UNKNOWN: the value received is not recognised.
    """
    def from_string(string):
        string = string.lower()
        if string == "font":
            return ExtractorMode.FONT
        elif string == "shape":
            return ExtractorMode.SHAPE
        else:
            return ExtractorMode.UNKNOWN

    FONT = auto()
    SHAPE = auto()
    UNKNOWN = auto()
