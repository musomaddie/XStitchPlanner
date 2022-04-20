from pattern_extractor import PatternExtractor

class FontPatternExtractor(PatternExtractor):

    """ A class for extracting from the pdf when it is in font mode.
    """

    def __init__(self, pdf):
        super().__init__(pdf)

    def get_rows(self, page_idx):
        return self.pdf.pages[page_idx].extract_table(
            {"vertical_strategy": "lines_strict"})

    def extract_pattern(self, *args, **kwargs):
        """ Implementing abstract method. """
        return self.extract_pattern_given_pages(
            self.get_rows, *args, **kwargs)

    def extract_key(self, key_page_idx):
        """ Implementing abstract method. """
        key_page = self.pdf.pages[key_page_idx]
        # TODO: what about cases where the key takes up > 1 page?
        colour_imgs = key_page.images
        colour_data = []
        # TODO: I'm worried about the case where the key table isn't in this
        # form.
        # TODO: doesn't currently work on Disney pattern as the key is not in
        # a table.
        for row in key_page.extract_table()[1:]:
            colour_data.append(row[2:5])
            colour_data.append(row[7:])

        return [[*row, *self._rgb_from_img(img)]
                for row, img in zip(colour_data, colour_imgs)]
