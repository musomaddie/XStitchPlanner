from extractors.key_extractors.key_extractor import KeyExtractor
from utils import determine_pages, divide_row, make_thread, verbose_print

import resources.strings as s

class FontKeyExtractor(KeyExtractor):
    """ A class for extracting the key when the PDF can be accessed via the
    text fields.

    Extends KeyExtractor
    """

    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    verbose=False):
        """ Implementing abstractmethod from KeyExtractor.  """
        # Set up
        first_page, last_page = determine_pages(key_start_page_idx,
                                                key_end_page_idx)
        self.multipage = first_page != last_page
        self.get_layout_info()

        for key_page_idx in range(first_page, last_page + 1):
            verbose_print(s.page_load("key", key_page_idx + 1), verbose)
            self.key.extend(self._extract_key_from_page(
                self.pdf.pages[key_page_idx],
                key_page_idx == first_page,
                verbose))

    def _extract_key_from_page(self, key_page, is_first_page, verbose=False):
        # TODO: assert that the headings contains the correct keys (Number and
        # Symbol).
        ref = self.layout_params.headings  # Variable for readability

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
            # Vars for readability
            colours = divide_row(row, self.layout_params.n_colours_per_row)

            # Ensure that the colour has a symbol and print a warning
            symb_idx = ref.index("Symbol")
            num_idx = ref.index("Number")
            for c in colours:
                if c[num_idx] != "":
                    if c[symb_idx] == "":
                        print(s.warning_no_symbol_found(c[num_idx]))

            return [make_thread(
                c[num_idx],
                c[symb_idx],  # Symbol and ident are the same for for font
                c[symb_idx],  # extractors.
                verbose=verbose) for c in colours
                if c[num_idx] != ""]
        rows = self.get_key_table(key_page)
        # TODO: if this returns None print the warning and ask to double
        # check if page num passed.

        # TODO: add this index getting to shared method.
        start_idx = (self.layout_params.n_rows_start - 1
                     if is_first_page
                     else self.layout_params.n_rows_start_pages - 1)
        end_idx = (self.layout_params.n_rows_end - 1
                   if is_first_page
                   else self.layout_params.n_rows_end_pages - 1)
        end_idx = len(rows) - end_idx

        result = []
        for row in rows[start_idx:end_idx]:
            result.extend(read_row(row))

        return result
