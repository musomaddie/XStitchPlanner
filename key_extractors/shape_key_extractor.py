from key_extractors.key_extractor import KeyExtractor
from pdf_utils import bbox_to_ident, verbose_print, make_thread
from typing import Counter
from string import ascii_letters, punctuation

class ShapeKeyExtractor(KeyExtractor):
    """ A class for extracting the key from a PDF when it can only be acessed
    in shape form.

    Extends KeyExtractor.

    Static Parameters:
        PLACEHOLDERS    list (string)   a list of symbols that will be used
                                        as identifiers for each colour stitch
                                        throughout the program. These will not
                                        necessarily match with the original
                                        symbol nor the displayed one.
        COLOUR_TABLE_SETTINGS   dict    the dictionary specifying the params to
                                        lookup the key in the PDF. If having
                                        trouble with reading the key on a new
                                        file, trying tweaking these.

    Parameters:
        ident_map:  maps every pdf shape to an ascii letter or punctuation
                    which acts as its identifier

    """
    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}
    PLACEHOLDERS = ascii_letters + punctuation

    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor. """
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
        key_page = self.pdf.pages[key_start_page_idx]
        verbose_print(f"Loading key on page {key_start_page_idx + 1}", verbose)
        idents = filter_majority_rects(
            [r for r in key_page.rects if not r["fill"]])

        idents = [bbox_to_ident(key_page,
                                (r["x0"], r["top"], r["x1"], r["bottom"]),
                                verbose) for r in idents]
        assert len(idents) <= len(self.PLACEHOLDERS), (
            "Too many symbols to automatically generate all symbols, "
            "file a bug to generate more.")
        verbose_print(f"Found {len(idents)} identifiers.", verbose)

        colors = filter_majority_rects(
            [r for r in key_page.rects if r["fill"]])
        colors = [[int(c*255) for c in r["non_stroking_color"]]
                  for r in colors]
        assert len(idents) == len(colors), (
            "Number of colors extracted does not equal number of symbols "
            f"extracted ({len(colors)} vs {len(idents)})")

        key_table = key_page.extract_table(self.COLOUR_TABLE_SETTINGS)
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

        verbose_print(f"Successfully extracted {len(stitches)} stitches",
                      verbose)

        symbols = list(self.PLACEHOLDERS)
        for stitch in stitches:
            stitch["symbol"] = symbols.pop(0)
            stitch["color"] = colors.pop(0)
            stitch["ident"] = idents.pop(0)

        self.ident_map = {s["ident"]: s["symbol"] for s in stitches}
        verbose_print(f"Successfully created an ident map of {self.ident_map}",
                      verbose)

        return [make_thread(s["dmc_num"], s["ident"], s["symbol"], s["name"],
                            verbose) for s in stitches]
