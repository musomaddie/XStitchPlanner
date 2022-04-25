from key_extractors.key_extractor import KeyExtractor
from pdf_utils import PLACEHOLDERS, bbox_to_ident, determine_pages, divide_row
from pdf_utils import make_thread, verbose_print
from typing import Counter

class ShapeKeyExtractor(KeyExtractor):
    """ A class for extracting the key from a PDF when it can only be acessed
    in shape form.

    Extends KeyExtractor.

    Static Parameters:
        COLOUR_TABLE_SETTINGS   dict    the dictionary specifying the params to
                                        lookup the key in the PDF. If having
                                        trouble with reading the key on a new
                                        file, trying tweaking these.
    """
    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}

    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    layout_file_name=None,
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor. """
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)
        self.get_layout_info(layout_file_name)
        key = []
        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(f"Loading key on page {key_page_idx + 1}",
                          verbose)
            key += self._extract_key_from_page(
                self.pdf.pages[key_page_idx], verbose)

        return key

    def _extract_key_from_page(self, key_page, verbose=False):
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
        idents = filter_majority_rects(
            [r for r in key_page.rects if not r["fill"]])

        idents = [bbox_to_ident(key_page,
                                (r["x0"], r["top"], r["x1"], r["bottom"]),
                                verbose) for r in idents]
        assert len(idents) <= len(PLACEHOLDERS), (
            "Too many symbols to automatically generate all symbols, "
            "file a bug to generate more.")
        verbose_print(f"Found {len(idents)} identifiers.", verbose)
        ref = self.layout_params.headings

        def read_row(row, count):
            """ Returns both the made row and the new count value """
            if self.layout_params.n_colours_per_row == 1:
                return ([make_thread(
                    row[ref.index("Number")],
                    idents[count],
                    PLACEHOLDERS[count],
                    verbose=verbose)], count + 1)
            colours = divide_row(row, self.layout_params.n_colours_per_row)
            resulting_list = []
            for c in colours:
                if c[ref.index("Number")] == "":
                    continue
                resulting_list.append(make_thread(c[ref.index("Number")],
                                                  idents[count],
                                                  PLACEHOLDERS[count],
                                                  verbose=verbose))
                count += 1
            return (resulting_list, count)

        key_table = self.get_key_table(key_page)
        # TODO: worry about start / end indices here?? Probably should.
        result = []
        count = 0
        for row in key_table:
            formatted_row, count = read_row(row, count)
            result.extend(formatted_row)

        return result
