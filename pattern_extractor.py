from abc import ABC, abstractmethod
from io import BytesIO
from PIL import Image

class PatternExtractor(ABC):
    """ A super class for the different types of extractor classes.

    Parameters:
        pdf     pdfplumber.PDF      the PDF to parse.

    Methods:
        __init__(pdf):              creates a new instance of pattern extractor
                                    for the given PDF.
        get_rows(page_idx):         returns all the rows on the page_idx'th
                                    page of the PDF.
        extract_key(key_page_idx):  extracts the key from the provided page of
                                    the PDF.

    Static Methods:
        _rgb_from_img(pdf_image):   returns the colour in the image extracted
                                    from the PDF image stream.
    """

    def __init__(self, pdf):
        """ Creates a new instance of the pattern extractor for the given PDF.

        Parameters:
            pdf     pdfplumber.PDF      the PDF to parse.
        """
        self.pdf = pdf

    @abstractmethod
    def get_rows(self, page_idx):
        """ Returns the rows extracted from the given page number.

        Parameters:
            page_idx    (int)   the page to extract rows from.

        Returns:
            ?? type??
        """
        pass

    @abstractmethod
    def extract_pattern(self, *args, **kwargs):
        """ Extracts the pattern.

        Returns:
            ???
        """
        pass

    @abstractmethod
    def extract_key(self, key_page_idx):
        """ Extracts the key which is found on the key_page_idx'th page of the
            PDF.

        Parameters:
            key_page_idx: the index of the page that contains the key.

        Returns:
            ??
        """
        pass

    @staticmethod
    def _rgb_from_img(pdf_img):
        """ Returns the colour in the image extracted from the PDF image
            stream.

        Parameters:
            pdf_image   pdfplumber.Image    the image to extract colours from.

        Returns:
            ??? (what is the type??
        """
        return Image.open(
            BytesIO(pdf_img["stream"].get_data())).getpixel((0, 0))
