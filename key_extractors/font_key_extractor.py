from key_extractors.key_extractor import KeyExtractor
from pdf_utils import make_thread, verbose_print

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
        """ Implementing abstractmethod from KeyExtractor.
        """
        # TODO: implement for multiple pages.
        # TODO: handle different forms --> probably have a way of defining it
        # or some helper function or something
        key_page = self.pdf.pages[key_start_page_idx]
        colour_data = []
        for row in key_page.extract_table()[1:]:
            colour_data.append(row[2:5])
            colour_data.append(row[7:])
        verbose_print(f"Successfully loaded a maximum of {len(colour_data)} "
                      "threads", verbose)

        return [make_thread(colour[1],
                            colour[0],  # Identifier and symbol are the same in
                            colour[0],  # font mode.
                            colour[2],
                            verbose)
                for colour in colour_data
                if colour[0] != ""]  # Remove any blank lines.
