from abc import ABC, abstractmethod

class KeyExtractor(ABC):
    """ A super class for the different types of key extractor classes.

    Parameters:
        pdf         pdfplumber.PDF      the PDF to extract the key from.

    Methods:
        __init__(pdf)       creates a new instance of the key extractor for the

    Abstract Methods:
        extract_key(start_page_idx, end_page_idx): extracts the key from the
                                                   given pages of the PDF.
    """

    def __init__(self, pdf):
        """ Creates a new instance of the key extractor for the given PDF.

        Paramaters:
            pdf         pdfplumber.PDF      the PDF to read the key from.
        """
        self.pdf = pdf

    @abstractmethod
    def extract_key(self, key_start_page_idx, key_end_page_idx=None):
        """ Extracts the key which is found on the key page range provided.

        TODO: actually handle multiple pages. (For now goal is to maintain
        functionality). --> include some error checking / handlding.

        Parameters:
            key_start_page_idx  int     The first page where the key can be
                                        found.
            key_end_page_idx    int     The last page where the key can be
                                        found. If this is not passed only the
                                        page specified by key_start_page_idx is
                                        parsed. [default: None]
        Returns:
            list(tuple(str))    a list of three tuples in the form (identifer,
                                dmc value, colour_description)
                                TODO: make this a data class so this can be
                                consistent even if some fields are missing.
        """
        pass
