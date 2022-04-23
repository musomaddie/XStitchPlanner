from key_extractors.key_extractor import KeyExtractor
from pdf_utils import determine_pages, make_thread, verbose_print

class FontKeyExtractor(KeyExtractor):
    """ A class for extracting the key when the PDF can be accessed via the
    text fields.

    Extends KeyExtractor
    """

    def __init__(self, pdf):
        super().__init__(pdf)

    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor.  """
        # TODO: handle different forms --> probably have a way of defining it
        # or some helper function or something
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)
        key = []
        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(f"Loading key on page {key_start_page_idx + 1}",
                          verbose)
            key += self._extract_key_from_page(
                self.pdf.pages[key_page_idx], verbose)

    def _extract_key_from_page(self, key_page, verbose=False):
        colour_data = []
        for row in key_page.extract_table()[1:]:
            colour_data.append(row[2:5])
            colour_data.append(row[-3:])
        verbose_print(f"Successfully loaded a maximum of {len(colour_data)} "
                      "threads", verbose)

        # Checking that every dmc colour has a symbol to go along with it. For
        # some reason the testing pdf isn't picking up every symbol.
        for colour in colour_data:
            if colour[0] == "":
                print(
                    "WARNING: will need to manually add symbol for "
                    f"{colour[1]}")

        return [make_thread(colour[1],
                            colour[0],  # Identifier and symbol are the same in
                            colour[0],  # font mode.
                            colour[2],
                            verbose)
                for colour in colour_data
                if colour[1] != ""]  # Remove any blank lines.
