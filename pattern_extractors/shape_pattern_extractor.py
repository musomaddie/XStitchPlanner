from pattern_extractors.pattern_extractor import PatternExtractor
from pdf_utils import bbox_to_ident

class ShapePatternExtractor(PatternExtractor):

    """ A class to handle extracting a pattern from the pdf when it is created
    using shapes.

    Parameters:
        ident_map: maps every pdf shape to an ascii letter or punctuation.
    """

    PATTERN_TABLE_SETTINGS = {
        "join_tolerance": 0,
        "snap_tolerance": 0,
        "intersection_tolerance": 0.1,
        "horizontal_strategy": "lines_strict",
        "vertical_strategy": "lines_strict",
        # Hard-coded min edge length which should stop us from including stitch
        # symbols
        "edge_min_length": 200
    }

    def __init__(self, pdf):
        super().__init__(pdf)
        self.ident_map = None

    def get_rows(self, page_idx, verbose=False):
        """ Implementing abstract method.

        Raises:
            AssertionError if it finds a shape not found in key.
        """
        def get_symbol(page, cell):
            ident = bbox_to_ident(page, cell, verbose)
            assert ident in self.ident_map, (
                f"Encountered unknown identifier '{ident}' not found in key.")
            return self.ident_map[ident]

        page = self.pdf.pages[page_idx]
        table = page.find_tables(self.PATTERN_TABLE_SETTINGS)[0]
        return [[get_symbol(page, cell) for cell in row.cells]
                for row in table.rows]

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method.
        """
        if not self.ident_map:
            raise ValueError("Cannot extract pattern before generating or "
                             "loading a key.")
        return self.extract_pattern_given_pages(self.get_rows, *args, **kwargs)

    def load_ident_map(self, key):
        """ Given a list of threads this loads the values into the ident map.
        """
        # TODO: I don't think this is actually being used anywhere.
        self.ident_map = {t.identifier: t.symbol for t in key}
