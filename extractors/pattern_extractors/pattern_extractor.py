from abc import abstractmethod
from extractors.extractor import Extractor
from pdf_utils import verbose_print

class PatternExtractor(Extractor):
    """ A super class for the different types of pattern extractor classes.

    Parameters:
        pdf         pdfplumber.PDF      the PDF to parse.

    Methods:
        __init__(pdf):              creates a new instance of pattern extractor
                                    for the given PDF.
        get_rows(page_idx):         returns all the rows on the page_idx'th
                                    page of the PDF.
        extract_pattern(*args, **kwargs):   extracts the pattern
        extract_key(key_page_idx):  extracts the key from the provided page of
                                    the PDF.
        extract_pattern_given_pages(get_rows_fn, width, height,
            start_page_idx=None, end_page_idx=None, overlap=0, verbose=False)
                                    Does the work of actually extracting the
                                    pattern.

    """

    def __init__(self, pdf, pattern_name):
        super().__init__(pdf, pattern_name)
        self.pattern = []

    @abstractmethod
    def get_rows(self, page_idx, withkey=False, verbose=False):
        """ Returns the rows extracted from the given page number.

        Parameters:
            page_idx    int     the page to extract rows from.
            verbose     bool    whether to print detailed debugging.

        Returns:
            list[list[str]]     a list of lists containing all the symbols
                                translated from the pdf pattern maintaining the

        Raises:
            AssertionError      if withkey is true and a symbol is identified
                                thats not found in the key.
        """
        pass

    @abstractmethod
    def extract_pattern(self, *args, **kwargs):
        """ Extracts the pattern.

        Returns:
            list[list[str]]     a list of lists containing all the symbols
                                translated from the pdf pattern maintaining the
                                rows and columns.
        """
        pass

    @abstractmethod
    def load_key(self, filename):
        """ Loads the key from the given file.

        Parameters:
            filename    str     the filename containing the key as a tsv.

        Returns:
            None    the key is saved as a class variable.

        Raises:
            FileNotFoundError   if the given file cannot be found.
        """
        pass

    def extract_pattern_given_pages(self,
                                    get_rows_fn,
                                    width,
                                    height,
                                    start_page_idx=None,
                                    end_page_idx=None,
                                    overlap=0,
                                    withkey=False,
                                    verbose=False):
        """ Returns a list of symbols extracted from the pdf pattern.

        Parameters:
            get_rows_fn     (function)  A function that returns the rows of a
                                        given page.
            width           (int)       the width of the pattern in stitches.
            height          (int)       the height of the pattern in stitches.
            start_page_idx  (int)       the index of the page where the pattern
                                        starts.
            end_page_idx    (int)       the index of the page where the pattern
                                        ends.
            overlap         (int)       the number of cells that overlap on
                                        each page edge of the pattern.
            withkey         (key)       whether to ensure that each symbol in
                                        the pattern is also found in the
                                        associated key.
            verbose         (bool)      whether progress statements should be
                                        printed.

        Returns:
            list[list[str]]     a list of lists containing all the symbols
                                translated from the pdf pattern maintaining the
                                rows and columns.
        Raises:
            AssertionError  if the pattern has an uneven width on any page.
            AssertionError  if the pattern has an unexpected height on any
                            page.
            AssertionError  if a pattern page exceeds the expected size.
            AssertionError  if the pattern is not the expected height
            AssertionError  if the pattern is not the expected width
        """
        verbose_print("Starting to extract pattern from rows.", verbose)
        all_pages = end_page_idx is None and start_page_idx is None
        if end_page_idx is None and start_page_idx is not None:
            end_page_idx = start_page_idx
        if all_pages:
            start_page_idx = 0
            end_page_idx = len(self.pdf.pages) - 1
        verbose_print(f"Pages set up starting from {start_page_idx} to "
                      f"{end_page_idx} ({all_pages})", verbose)

        cur_x = 0
        cur_y = 0
        expected_page_height = 0
        pattern = []

        for page_idx in range(start_page_idx, end_page_idx+1):
            rows = get_rows_fn(page_idx, withkey=withkey, verbose=verbose)
            cur_x, cur_y, expected_page_height = self._extract_from_this_page(
                pattern,
                page_idx, rows,
                cur_x, cur_y, expected_page_height, height, width,
                overlap, verbose)

        if all_pages:
            assert len(pattern) == height, (
                f"{len(pattern)} stitches high but expected {height} "
                "after parsing whole pattern")
            assert len(pattern[0] == width), (
                f"{len(pattern[0])} stitches but expected {width} after "
                "parsing whole pattern")

        self.pattern = pattern

    def save_pattern(self):
        """ Saves the pattern extracted by this class.

        Raises:
            AssertionError if the pattern is blank.
        """
        assert len(self.pattern) > 0, (
            "No pattern has been extracted. Make sure you've run "
            "extract pattern.")

        with open(self.pattern_filename, "w", encoding="utf-8") as f:
            print(*["".join(row) for row in self.pattern], sep="\n", file=f)

    def _extract_from_this_page(self,
                                pattern,
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

        pi_p = page_idx + 1

        assert all(len(row) == page_width for row in rows), (
            f"Pattern uneven width on page {pi_p}")
        assert (
            page_height == expected_page_height or cur_height == height), (
                f"Pattern {page_height} tall on page {pi_p} when "
                f"expected {expected_page_height} or {height - cur_y}")
        assert cur_width <= width and cur_height <= height, (
            f"Page {page_idx + 1} ({page_width}x{page_height} results in "
            f"exceeded pattern dimensions ({cur_width}x{cur_height}) vs "
            f"{width}x{height})")

        verbose_print(
            f"Extracting page {pi_p} ({page_width}x{page_height} ), pat size "
            f"{cur_width}x{cur_height}", verbose)

        if cur_x != 0 and pattern:
            # New columns, so just need to add these to the end of existing
            # rows
            for pat_row, page_row in zip(
                    pattern[cur_y: cur_y + page_height], rows):
                pat_row += page_row
        else:
            # New rows, so just need to add them to the end of existing
            # pattern.
            pattern += rows
            verbose_print(f"\t(new rows) {rows}", verbose)

        cur_x += len(rows[0])
        if cur_x == width:
            cur_x = 0
            cur_y += page_height

        return (cur_x, cur_y, expected_page_height)
