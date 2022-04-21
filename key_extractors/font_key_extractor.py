from key_extractors.key_extractor import KeyExtractor

class FontKeyExtractor(KeyExtractor):
    """ A class for extracting the key when the PDF can be accessed via the
    text fields.

    Extends KeyExtractor
    """

    def __init__(self, pdf):
        super().__init__(pdf)

    def extract_key(self, key_start_page_idx, key_end_page_idx=None):
        """ Implementing abstractmethod from KeyExtractor.

        This differs to Kelly's version as I'm leaving out getting the RGB
        images from the PDF as that is proving painful.
        """
        # TODO: implement for multiple pages.
        # TODO: handle different forms --> probably have a way of defining it
        # or some helper function or something
        key_page = self.pdf.pages[key_start_page_idx]
        colour_data = []
        for row in key_page.extract_table()[1:]:
            colour_data.append(row[2:5])
            colour_data.append(row[7:])
        # TODO: remove blank rows
        return colour_data
