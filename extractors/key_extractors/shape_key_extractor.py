from typing import Counter

from pdfplumber.page import Page

import resources.strings as s
from extractors.key_extractors.key_extractor import KeyExtractor
from floss_thread import Thread
from utils import (
    PLACEHOLDERS, bbox_to_ident, determine_pages, divide_row, make_thread, verbose_print)


class ShapeKeyExtractor(KeyExtractor):
    """ A class for extracting the key from a PDF when it can only be accessed in shape form.

    Extends KeyExtractor.

    Static Parameters:
        COLOUR_TABLE_SETTINGS: the dictionary specifying the params to look up the key in the
            PDF. If having trouble with reading the key on a new file, trying tweaking these.
    """
    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}

    def extract_key(
            self,
            key_start_page_idx: int,
            key_end_page_idx: int = None,
            verbose: bool = False) -> None:
        """ Implementing abstractmethod from KeyExtractor. """
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)
        self.get_layout_info()
        count = 0
        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(s.page_load("key", key_page_idx + 1), verbose)
            result, count = self._extract_key_from_page(
                self.pdf.pages[key_page_idx], key_page_idx == first_page, count, verbose)
            self.key += result

    def _extract_key_from_page(
            self, key_page: Page,
            is_first_page: bool,
            count: int,
            verbose: bool = False) -> (list[Thread], int):
        # TODO: extract to own method for testing
        def filter_majority_rects(rects):
            """ Return the rects with the majority size to try and guess at
            which rects hold the right key components. """
            majority_width, majority_height = Counter(
                [(int(r["width"]), int(r["height"])) for r in rects]).most_common(1)[0][0]
            return [r for r in rects
                    if int(r["width"]) == majority_width and int(r["height"]) == majority_height]

        idents = filter_majority_rects([r for r in key_page.rects if not r["fill"]])

        if len(idents) > len(PLACEHOLDERS):
            raise NotImplementedError(s.too_many_symbols())

        # TODO: pass a mock here for the test_shape_key_extractor_extract_key_from_page_passes,
        #  it will make my life a LOT easier
        idents = [bbox_to_ident(key_page, (r["x0"], r["top"], r["x1"], r["bottom"]), verbose)
                  for r in idents]
        verbose_print(s.number_of_identifiers(len(idents)), verbose)
        ref = self.layout_params.headings

        key_table = self.get_key_table(key_page)
        ref = self.layout_params.headings  # Variable for readability
        start_idx = (self.layout_params.n_rows_start - 1 if is_first_page
                     else self.layout_params.n_rows_start_pages - 1)
        end_idx = (self.layout_params.n_rows_end - 1 if is_first_page
                   else self.layout_params.n_rows_end_pages - 1)
        end_idx = len(key_table) - end_idx

        # TODO (issues/22): the ident boxes and numbers must line up.
        # TODO: split this into more logical methods and test them!!
        colour_columns = [[] for _ in range(self.layout_params.n_colours_per_row)]
        for row in key_table[start_idx:end_idx]:
            if self.layout_params.n_colours_per_row == 1:
                colour_columns[0].append(row[ref.index("Number")])
            else:
                colours_this_row = divide_row(row, self.layout_params.n_colours_per_row)
                # Skip blank rows
                if colours_this_row[0][0] == "":
                    continue
                for n, c in enumerate(colours_this_row):
                    if c[ref.index("Number")] == "":
                        continue
                    colour_columns[n].append(c[ref.index("Number")])

        all_colour_values = []
        for column in colour_columns:
            all_colour_values.extend(column)

        result = []
        for ident, colour in zip(idents, all_colour_values):
            result.append(make_thread(colour, ident, PLACEHOLDERS[count]))
            count += 1
        return result, count
