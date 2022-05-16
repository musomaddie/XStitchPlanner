from extractors.key_extractors.key_extractor import KeyExtractor
from utils import PLACEHOLDERS, bbox_to_ident, determine_pages, divide_row
from utils import make_thread, verbose_print
from typing import Counter

import resources.strings as s

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
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor. """
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)
        self.get_layout_info()
        count = 0
        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(s.page_load("key", key_page_idx + 1), verbose)
            result, count = self._extract_key_from_page(
                self.pdf.pages[key_page_idx],
                key_page_idx == first_page,
                count, verbose)
            self.key += result

    def _extract_key_from_page(self,
                               key_page,
                               is_first_page,
                               count,
                               verbose=False):
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

        def read_row(row, count, page_count):
            """ Returns both the made row and the new count value """
            if self.layout_params.n_colours_per_row == 1:
                return ([make_thread(
                    row[ref.index("Number")],
                    idents[page_count],
                    PLACEHOLDERS[count],
                    verbose=verbose)], count + 1, page_count + 1)
            colours = divide_row(row, self.layout_params.n_colours_per_row)
            resulting_list = []
            for c in colours:
                if c[ref.index("Number")] == "":
                    continue
                resulting_list.append(make_thread(c[ref.index("Number")],
                                                  idents[page_count],
                                                  PLACEHOLDERS[count],
                                                  verbose=verbose))
                count += 1
                page_count += 1
            return (resulting_list, count, page_count)
        idents = filter_majority_rects(
            [r for r in key_page.rects if not r["fill"]])
        if len(idents) > len(PLACEHOLDERS):
            raise NotImplementedError(s.too_many_symbols())

        idents = [bbox_to_ident(key_page,
                                (r["x0"], r["top"], r["x1"], r["bottom"]),
                                verbose) for r in idents]
        verbose_print(s.number_of_identifiers(len(idents)), verbose)
        ref = self.layout_params.headings

        key_table = self.get_key_table(key_page)
        ref = self.layout_params.headings  # Variable for readability
        start_idx = (self.layout_params.n_rows_start - 1
                     if is_first_page
                     else self.layout_params.n_rows_start_pages - 1)
        end_idx = (self.layout_params.n_rows_end - 1
                   if is_first_page
                   else self.layout_params.n_rows_end_pages - 1)
        end_idx = len(key_table) - end_idx

        result = []
        # TODO (issues/22): the ident boxes and numbers must line up.
        page_count = 0
        for row in key_table[start_idx:end_idx]:
            formatted_row, count, page_count = read_row(row, count, page_count)
            result.extend(formatted_row)
        return result, count
