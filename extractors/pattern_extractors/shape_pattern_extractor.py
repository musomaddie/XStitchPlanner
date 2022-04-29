from extractors.pattern_extractors.pattern_extractor import PatternExtractor
from utils import PLACEHOLDERS, bbox_to_ident, read_key, verbose_print

import resources.strings as s

class ShapePatternExtractor(PatternExtractor):

    """ A class to handle extracting a pattern from the pdf when it is created
    using shapes.

    Parameters:
        ident_map       dict[str:str]   maps every shape in the key to an
                                        ident. Populated by the key if it is
                                        loaded otherwise generated as the
                                        cells are read.
        _used_symbols   list            a list of symbols already used in the
                                        pattern. Only populated if no key is
                                        provided.
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

    def __init__(self, pdf, pattern_name):
        super().__init__(pdf, pattern_name)
        self.ident_map = {}
        self._used_symbols = []

    def get_rows(self, page_idx, withkey=False, verbose=False):
        """ Implementing abstract method.  """
        def find_next_placeholder():
            assert len(self._used_symbols) <= len(PLACEHOLDERS), (
                s.too_many_symbols())
            for x in PLACEHOLDERS:
                if x not in self._used_symbols:
                    self._used_symbols.append(x)
                    return x

        def get_symbol(page, cell):
            ident = bbox_to_ident(page, cell, verbose)
            if withkey:
                assert ident in self.ident_map, s.ident_unknown(ident)
            else:
                # If this ident hasn't already been seen we should add it to
                # the ident map.
                if ident not in self.ident_map:
                    verbose_print(s.ident_doesnt_already_exist(ident), verbose)
                    self.ident_map[ident] = find_next_placeholder()

            return self.ident_map[ident]

        page = self.pdf.pages[page_idx]
        # page.to_image().save("????.png")
        table = page.find_tables(self.PATTERN_TABLE_SETTINGS)[0]
        return [[get_symbol(page, cell) for cell in row.cells]
                for row in table.rows]

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method.
        """
        if kwargs["withkey"] and not self.ident_map:
            raise ValueError(s.extract_pattern_no_key())
        self.extract_pattern_given_pages(self.get_rows, *args, **kwargs)

    def load_key(self):
        """ Implements the abstractmethod """
        self.ident_map = {t.identifier: t.symbol
                          for t in read_key(self.key_filename)}
