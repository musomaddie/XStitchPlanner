class PatternExtractor:
    """ A super class for the different types of extractor classes.

    Parameters:
        pdf     pdfplumber.PDF      the PDF to parse.

    Methods:
        __init__(pdf):  creates a new instance of pattern extractor for the
                        given PDF.

    """

    def __init__(self, pdf):
        """ Creates a new instance of the pattern extractor for the given PDF.

        Parameters:
            pdf     pdfplumber.PDF      the PDF to parse.
        """
        self.pdf = pdf
