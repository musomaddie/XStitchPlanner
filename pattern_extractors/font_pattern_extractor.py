from pattern_extractors.pattern_extractor import PatternExtractor

class FontPatternExtractor(PatternExtractor):

    """ A class for extracting from the pdf when it is in font mode.
    """
    def __init__(self, pdf):
        super().__init__(pdf)

    def get_rows(self, page_idx):
        # TODO: add similar check here as is in shapes: need to make sure all
        # of them are valid identifiers.
        return self.pdf.pages[page_idx].extract_table(
            {"vertical_strategy": "lines_strict"})

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method. """
        return self.extract_pattern_given_pages(
            self.get_rows, *args, **kwargs)
