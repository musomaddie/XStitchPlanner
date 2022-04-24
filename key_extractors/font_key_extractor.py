from key_extractors.key_extractor import KeyExtractor
from pdf_utils import TextFormat, determine_pages, make_thread, verbose_print

class FontKeyExtractor(KeyExtractor):
    """ A class for extracting the key when the PDF can be accessed via the
    text fields.

    Extends KeyExtractor
    """

    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    layout_file_name=None,
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor.  """
        # Set up
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)

        self.multipage = first_page != last_page
        self.get_layout_info(layout_file_name)

        key = []
        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(f"Loading key on page {key_start_page_idx + 1}",
                          verbose)
            key.extend(self._extract_key_from_page(
                self.pdf.pages[key_page_idx],
                key_page_idx == key_start_page_idx,
                verbose))
            return key
        return key

    def _extract_key_from_page(self, key_page, is_first_page, verbose=False):
        ref = self.layout_params.headings  # Variable for readability
        start_idx = (self.layout_params.n_rows_start
                     if is_first_page
                     else self.layout_params.n_rows_start_pages)
        end_idx = (self.layout_params.n_rows_end - 1
                   if is_first_page
                   else self.layout_params.n_rows_end_pages - 1)

        def read_row(row):
            """ Turns a given row into a thread """
            # Handling multiple keys per row
            if self.layout_params.n_colours_per_row == 1:
                # Returning a list for consistency with multiple colours per
                # row
                return [make_thread(
                    row[ref.index("Number")],
                    row[ref.index("Symbol")],  # symbol and ident are the same
                    row[ref.index("Symbol")],  # in font extractor.
                    verbose=verbose)]

            # Break up the row into n distinct sections: it should evenly
            # divide -- if it doesn't COMPLAIN!
            # Assume colour square is there - consider this when dividing
            assert len(row) % self.layout_params.n_colours_per_row == 0, (
                "The row does not evenly divide into the number of colours "
                "provided.")
            # The "colour square" fills two columns of the table per colour in
            # row as it takes up the cell its in and the square is counted as
            # another cell. assuming this is the first two cells.
            # TODO: I can probably add another assert in here with a request
            # for a bug if there is a pattern where this doesn't occur.

            # Vars for readability
            sub_size = len(row) // self.layout_params.n_colours_per_row
            colours = [
                row[n * sub_size:(n + 1) * sub_size]
                for n in range(self.layout_params.n_colours_per_row)]

            # Ensure that the colour has a symbol and print a warning
            symb_idx = ref.index("Symbol")
            num_idx = ref.index("Number")
            for c in colours:
                if c[num_idx] != "":
                    if c[symb_idx] == "":
                        print(f"{TextFormat.BRIGHT_RED}WARNING: no associated "
                              f"symbol could be found for '{c[num_idx]}'. You "
                              "will need to add this manually."
                              f"{TextFormat.END}")

            return [make_thread(
                c[num_idx],
                c[symb_idx],  # Symbol and ident are the same for for font
                c[symb_idx],  # extractors.
                verbose=verbose) for c in colours
                if c[num_idx] != ""]

        rows = self.get_key_table(key_page)

        # Special case for end_idx being 0 because trying to loop to -0
        # does not loop at all.
        result = []
        if end_idx == 0:
            for row in rows[start_idx:]:
                result.extend(read_row(row))
        else:
            for row in rows[start_idx:end_idx]:
                result.extend(read_row(row))

        return result
