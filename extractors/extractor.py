from abc import ABC

import pdfplumber


class Extractor(ABC):
    """
    A super class for all the extractors. Currently, primarily being used to store generic
    pattern information.

    This has to extend ABC because it  is required for key and pattern
    extractors which can only extend one super class.

    Parameters:
        pdf: the PDF being extracted from
        pattern_name: the name of the pattern (PDF filename with the extension removed).

    Methods:
        __init__(pdf, pattern_name):    creates a new instance of the extractor
    """
    pdf: pdfplumber.PDF
    pattern_name: str

    def __init__(self, pdf: pdfplumber.PDF, pattern_name: str):
        self.pdf = pdf
        self.pattern_name = pattern_name
        self.key_filename = f"{pattern_name}.key"
        self.pattern_filename = f"{pattern_name}.pat"


class PatternFormatError(Exception):
    """ Custom error to be used when the modifiers passed do not match the result"""
    pass
