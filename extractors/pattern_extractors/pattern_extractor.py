from abc import abstractmethod
from typing import Callable

from pdfplumber import PDF

import resources.strings as s
from extractors.extractor import Extractor, PatternFormatError
from utils import verbose_print


class PatternExtractor(Extractor):
    """ A super class for the different types of pattern extractor classes.

    Parameters:
        pdf: the PDF to parse
        pattern: the extracted pattern once the extract methods have run

    Methods:
        __init__(pdf, pattern_name)
        get_rows(page_idx): returns all the rows on the page_idx'th page of the PDF.
        extract_pattern(*args, **kwargs): extracts the pattern
        extract_key(key_page_idx): extracts the key from the provided page of the PDF.
        extract_pattern_given_pages(get_rows_fn, width, height, start_page_idx=None,
            end_page_idx=None, overlap=0, verbose=False): Does the work of actually extracting the
                pattern.

    """
    pdf: PDF
    pattern: list[list[str]]

    def __init__(self, pdf: PDF, pattern_name: str):
        super().__init__(pdf, pattern_name)
        self.pattern = []

    @abstractmethod
    def get_rows(
            self, page_idx: int, withkey: bool = False, verbose: bool = False) -> list[list[str]]:
        """ Returns all the rows on the given page

        Args:
            page_idx: the index of the page to extract the pattern from
            withkey: have we already extracted the key?
            verbose: whether to print detailed debugging statements

        Returns:
            list[list[str]]: a list of all the information on the pattern in the format of
                rows[column]

        Raises:
            PatternFormatError  if withkey is true and a symbol is identified that's not found in
                the key
        """
        pass

    @abstractmethod
    def extract_pattern(self, *args, **kwargs):
        """ Extracts the pattern.

        Returns:
            list[list[str]]: a list of lists containing all the symbols translated from the pdf
            pattern maintaining the rows and columns
        """
        pass

    @abstractmethod
    def load_key(self):
        """ Loads the key from the given file.

        Raises:
            FileNotFoundError   if the given file cannot be found.
        """
        pass

    def extract_pattern_given_pages(
            self,
            get_rows_fn: Callable,
            width: int,
            height: int,
            start_page_idx: int = None,
            end_page_idx: int = None,
            overlap: int = 0,
            withkey: bool = False,
            verbose: bool = False):
        """
        Returns the pattern extracted from the PDF across all provided pages

        Args:
            get_rows_fn: the function that determines how every pattern row (and by extension)
                columns are extracted from the PDF
            width: the width of the pattern in stitches
            height: the height of the pattern in stitches
            start_page_idx: the index of the page where the pattern starts
            end_page_idx: the index of the page where the pattern ends
            overlap: the number of cells that overlap on each page edge of the pattern
            withkey: whether to ensure that each symbol is also found in the key
            verbose: whether progress statements should be printed

        Raises:
            PatternFormatError: if the pattern has an uneven width on any page
            PatternFormatError: if the pattern has an unexpected height on any page
            PatternFormatError: if a pattern page exceeds the expected size
            PatternFormatError: if the pattern is not the expected height
            PatternFormatError: if the pattern is not the expected width
        """
        verbose_print(s.row_extract("pattern"), verbose)
        all_pages = end_page_idx is None and start_page_idx is None
        if end_page_idx is None and start_page_idx is not None:
            end_page_idx = start_page_idx
        if all_pages:
            start_page_idx = 0
            end_page_idx = len(self.pdf.pages) - 1
        verbose_print(s.pages_found(start_page_idx, end_page_idx), verbose)

        cur_x = 0
        cur_y = 0
        expected_page_height = 0

        for page_idx in range(start_page_idx, end_page_idx + 1):
            rows = get_rows_fn(page_idx, withkey=withkey, verbose=verbose)
            cur_x, cur_y, expected_page_height = self._extract_from_this_page(
                page_idx, rows,
                cur_x, cur_y, expected_page_height, height, width,
                overlap, verbose)

        if len(self.pattern) != height:
            raise PatternFormatError(s.pattern_wrong_size("high", len(self.pattern), height))
        if len(self.pattern[0]) != width:
            raise PatternFormatError(s.pattern_wrong_size("wide", len(self.pattern[0]), width))

    def _extract_from_this_page(
            self,
            page_idx,
            rows,
            cur_x, cur_y,
            expected_page_height,
            height, width,
            overlap,
            verbose):
        """ A helper so that the method above is not quite as long.
            DO NOT USE on its own.

            Returns:
                (cur_x, cur_y, expected_page_height)
                All the other modified values that are passed by reference.
        """
        if cur_y > 0:
            rows = rows[overlap:]
        if cur_x > 0:
            rows = [row[overlap:] for row in rows]

        page_width = len(rows[0])
        page_height = len(rows)

        if cur_x == 0:
            expected_page_height = page_height

        cur_width = cur_x + page_width
        cur_height = cur_y + page_height

        height_check_1 = page_height == expected_page_height
        height_check_2 = cur_height == height

        pi_p = page_idx + 1

        if False in [len(row) == page_width for row in rows]:
            raise PatternFormatError(s.pattern_uneven_width(pi_p))
        if not (height_check_1 or height_check_2):
            raise PatternFormatError(s.pattern_uneven_height(
                pi_p, page_height, expected_page_height, height - cur_y))
        if cur_width > width or cur_height > height:
            raise PatternFormatError(
                s.pattern_size_too_big(pi_p, page_width, page_height,
                                       cur_width, cur_height, width, height))

        verbose_print(
            s.pattern_extracting_page(pi_p, page_width, page_height, cur_width, cur_height),
            verbose)

        if cur_x != 0 and self.pattern:
            # New columns, so just need to add these to the end of existing
            # rows
            for pat_row, page_row in zip(self.pattern[cur_y: cur_y + page_height], rows):
                pat_row += page_row
        else:
            # New rows, so just need to add them to the end of existing
            # pattern.
            self.pattern += rows
            verbose_print(s.new_row(rows), verbose)

        cur_x += len(rows[0])
        if cur_x == width:
            cur_x = 0
            cur_y += page_height

        return cur_x, cur_y, expected_page_height

    def save_pattern(self):
        """ Saves the pattern extracted by this class.

        Raises:
            PatternFormatError if the pattern is blank.
        """
        if len(self.pattern) == 0:
            raise ValueError(s.empty_on_save("pattern"))

        with open(self.pattern_filename, "w", encoding="utf-8") as f:
            print(*["".join(row) for row in self.pattern], sep="\n", file=f)
