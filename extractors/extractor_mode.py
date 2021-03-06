from enum import Enum, auto


class ExtractorMode(Enum):
    """
    Determines how the pattern is to be read from the pdf.

    FONT:    identifies symbols in the pattern by extracting the text from the
             PDF.
    SHAPE:   extract symbols from the PDF by attempting to identify and match
             reoccurring lines and shapes on the page.
    UNKNOWN: the value received is not recognised.
    """

    @staticmethod
    def from_string(string: str) -> 'ExtractorMode':
        """ Converts a string into an Extractor Mode. """
        string = string.lower()
        for opt in ExtractorMode:
            if string == opt.value:
                return opt
        return ExtractorMode.UNKNOWN

    FONT = "font"
    SHAPE = "shape"
    UNKNOWN = auto()
