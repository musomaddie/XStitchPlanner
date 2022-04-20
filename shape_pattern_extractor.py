from pattern_extractor import PatternExtractor
from string import ascii_letters, punctuation

import Counter

class ShapePatternExtractor(PatternExtractor):

    """ A class to handle extracting a pattern from the pdf when it is created
    using shapes.

    Parameters:
        ident_map: maps every pdf shape to an ascii letter or punctuation.

    Static Methods:
        bbox_to_ident(page, bbox): does some magic I don't understand yet.
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

    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}
    PLACEHOLDERS = ascii_letters + punctuation

    def __init__(self, pdf):
        super().__init__(pdf)
        self.ident_map = None

    @staticmethod
    def bbox_to_ident(page, bbox):
        """ ?>???

        Parameters:
            page:   pdfplumber.Page     the page we are interested in.
            bbox:                       the bounding box.
        Returns:
            ???
        """
        def objs_ident(objs, prefix):
            return [prefix + "".join(sorted(
                [f"x{int(x - obj['x0'])}y{int(y - obj['y0'])}"
                 for x, y in obj["pts"]])) for obj in objs]
            page_sect = page.within_bbox(bbox)
            return "-".join(sorted(
                objs_ident(page_sect.curves, "c")
                + objs_ident(page_sect.lines, "l")))

    def get_rows(self, page_idx):
        """ Implementing abstract method.

        Raises:
            AssertionError if it finds a shape not found in key.
        """
        def get_symbol(page, cell):
            ident = self.bbox_to_ident(page, cell)
            assert ident in self.ident_map, (
                f"Encountered unknown identifier '{ident} not found in key.")
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
        return PatternExtractor.extract_pattern_given_pages(self.get_rows,
                                                            *args, **kwargs)

    def load_ident_map(self, path):
        ident_map = {}
        with open(path) as f:
            for row in f:
                symbol, *_, ident = row.split("\t")
                ident_map[ident] = symbol
        self.ident_map = ident_map

    def extract_key(self, key_page_idx):
        """ Implementing abstract method. """

        def filter_majority_rects(rects):
            """ Return the rects with the majority size to try and guess at
            which rects hold the right key components. """
            majority_width, majority_height = Counter(
                [(int(r["width"]), int(r["height"])) for r in rects]
            ).most_common(1)[0][0]
            return [
                r for r in rects
                if int(r["width"]) == majority_width
                and int(r["height"]) == majority_height]

        key_page = self.pdf.pages[key_page_idx]

        idents = filter_majority_rects(
            [r for r in key_page.rects if not r["fill"]])
        idents = [self.bbox_to_ident(key_page,
                                     (r["x0"], r["top"], r["x1"], r["bottom"])
                                     ) for r in idents]
        assert len(idents) <= len(self.PLACEHOLDERS), (
            "Too many symbols to automatically generate all symbols")

        colors = filter_majority_rects(
            [r for r in key_page.rects if r["fill"]])
        colors = [[int(c*255) for c in r["non_stroking_color"]]
                  for r in colors]
        assert len(idents) == len(colors), (
            "Number of colors extracted does not equal number of symbols "
            f"extracted ({len(colors)} vs {len(idents)})")

        key_table = key_page.extract_table(self.COLOR_TABLE_SETTINGS)
        stitches = []
        last_col_stitches = []
        for row in key_table:
            if row[2] and row[1]:
                stitches.append({"name": row[2], "dmc_num": row[1]})
            if row[3] and row[4]:
                last_col_stitches.append({"name": row[5], "dmc_num": row[4]})
        stitches += last_col_stitches
        assert len(stitches) == len(idents), (
            "Number of rows extracted does not equal number of colors "
            f"extracted ({len(stitches)} vs {len(colors)})")

        symbols = list(self.PLACEHOLDERS)
        for stitch in stitches:
            stitch["symbol"] = symbols.pop(0)
            stitch["color"] = colors.pop(0)
            stitch["ident"] = idents.pop(0)

        self.ident_map = {s["ident"]: s["symbol"] for s in stitches}

        return [(s["symbol"], s["dmc_num"], s["name"], *s["color"], s["ident"])
                for s in stitches]
