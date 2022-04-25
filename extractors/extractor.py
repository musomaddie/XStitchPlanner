from abc import ABC

class Extractor(ABC):
    """ A super class for all the extractors. Currently primarily being used to
    store generic pattern information. (Consider making data class)

    This has to extend ABC because it  is required for key and pattern
    extractors and they can only extend one.

    Parameters:
        pdf             pdfplumber.PDF  the PDF being extracted from.
        pattern_name    str             the name of the pattern (PDF filename
                                        with the extension removed).

    Methods:
        __init__(pdf, pattern_name)     creates a new instance of the extractor
    """

    def __init__(self, pdf, pattern_name):
        self.pdf = pdf
        self.pattern_name = pattern_name
