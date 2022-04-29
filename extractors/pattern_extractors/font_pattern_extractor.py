from extractors.pattern_extractors.pattern_extractor import PatternExtractor
from utils import read_key

import resources.strings as s

class FontPatternExtractor(PatternExtractor):

    """ A class for extracting from the pdf when it is in font mode.
    Parameters:
        symbols:    a list of every symbol that appears in the key (if the key
                    is loaded).
    """
    def __init__(self, pdf, pattern_name):
        super().__init__(pdf, pattern_name)
        self.symbols = []

    def get_rows(self, page_idx, withkey=False, verbose=False):
        result = self.pdf.pages[page_idx].extract_table(
            {"vertical_strategy": "lines_strict"})

        if withkey:
            for row in result:
                for cell in row:
                    print(cell)
                    assert cell in self.symbols, s.symbol_not_in_key(cell)

        return result

    def load_key(self, filename):
        """ Implementing abstractmethod. """
        self.symbols = [t.symbol for t in read_key(filename)]
        print(self.symbols)

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method. """
        self.extract_pattern_given_pages(self.get_rows, *args, **kwargs)
