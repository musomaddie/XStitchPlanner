import pdfplumber

import resources.strings as s
from extractors.pattern_extractors.pattern_extractor import PatternExtractor
from utils import read_key


class FontPatternExtractor(PatternExtractor):
    """ A class for extracting from the pdf when it is in font mode.

    Parameters:
        symbols(list[str]):     a list of every symbol that appears in the key once the key is
            loaded
    """

    def __init__(self, pdf: pdfplumber.PDF, pattern_name: str):
        super().__init__(pdf, pattern_name)
        self.symbols = []

    def get_rows(
            self,
            page_idx: int,
            withkey: bool = False,
            verbose: bool = False) -> list[list[str]]:
        """ Implements abstract method """

        result = self.pdf.pages[page_idx].extract_table(
            {"vertical_strategy": "lines_strict"})

        if withkey:
            for row in result:
                for cell in row:
                    if cell not in self.symbols:
                        raise ValueError(s.symbol_not_in_key(cell))

        return result

    def load_key(self):
        """ Implementing abstractmethod. """
        self.symbols = [t.symbol for t in read_key(self.key_filename)]

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method. """
        self.extract_pattern_given_pages(self.get_rows, *args, **kwargs)
