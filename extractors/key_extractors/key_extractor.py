import csv
import json
from abc import abstractmethod

import resources.strings as s
from extractors.extractor import Extractor
from extractors.key_extractors.key_layout import KeyForm, KeyLayout

# Variables for JSON keys (just to make them obvious / consistent).
JK_KF = "key form"
JK_RS = "row start"
JK_RE = "row end"
JK_OP = "other pages"
JK_FP = "first page"
JK_SF = f"{JK_RS} {JK_FP}"
JK_EF = f"{JK_RE} {JK_FP}"
JK_SO = f"{JK_RS} {JK_OP}"
JK_EO = f"{JK_RE} {JK_OP}"
JK_NC = "number of colours per row"
JK_H = "column headings"


class KeyExtractor(Extractor):
    """ A super class for the different types of key extractor classes.

    Parameters:
        pdf             pdfplumber.PDF              the PDF to extract the key
                                                    from
        pattern_name    str                         the name of the pattern
                                                    (filename with .pdf
                                                    removed).
        multipage       bool                        whether the key is spread
                                                    over multiple pages.
                                                    [default: False]
        layout_params   KeyLayout                   how the columns for the key
                                                    information are laid out.
                                                    [default: None]
        key             list[floss_thread.Thread]   a list containing all the
                                                    thread details for every
                                                    thread found in the pattern
                                                    [default: []]

    Methods:
        __init__(pdf)                       creates a new instance of the key
                                            extractor for the given PDF
        get_key_table(page)                 return a table to extract the
                                            values from depending on the
                                            KeyForm in layout params
        read_from_layout_file()             loads the layout params
        save_key()                          saves the key that has been
                                            extracted by this extractor.

    Abstract Methods:
        extract_key(start_page_idx, end_page_idx): extracts the key from the
                                                   given pages of the PDF.
    """

    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}

    def __init__(self, pdf, pattern_name):
        """ Creates a new instance of the key extractor for the given PDF.

        Parameters:
            pdf             pdfplumber.PDF      the PDF to read the key from.
            pattern_name    str                 the name of the pattern (pdf
                                                filename without the extension)
        """
        super().__init__(pdf, pattern_name)
        self.key_config_filename = s.filename_key_config(pattern_name)
        self.multipage = False
        self.layout_params = None
        self.key = []

    @abstractmethod
    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    verbose=False):
        """ Extracts the key which is found on the key page range provided.

        Parameters:
            key_start_page_idx  int     The first page where the key can be
                                        found.
            key_end_page_idx    int     The last page where the key can be
                                        found. If this is not passed only the
                                        page specified by key_start_page_idx is
                                        parsed. [default: None]
            verbose             bool    whether to print detailed messages
                                        [default: False]
        Returns:
            list(Thread)        a list of of all the threads contained in this
                                pattern.
        """
        pass

    def get_key_table(self, page):
        """ Helper for returning the table containing the key on a given page
        depending on the layout params.
        """
        if not self.layout_params:
            raise ValueError(s.no_key_layout_params())
        if self.layout_params.key_form == KeyForm.UNKNOWN:
            raise ValueError(s.key_form_invalid())

        if self.layout_params.key_form == KeyForm.FULL_LINES:
            return page.extract_table()
        if self.layout_params.key_form == KeyForm.NO_LINES:
            return page.extract_table(self.COLOUR_TABLE_SETTINGS)
        if self.layout_params.key_form == KeyForm.ONLY_HEADER_LINE:
            # TODO (issues/21): need an alternative approach if this breaks.
            bbox = [0, 0, page.width, page.height]
            starting_line = page.rects[0]
            for rect in page.rects:
                if rect["width"] > starting_line["width"]:
                    starting_line = rect
            # Getting all the rects in this vertical line in case they weren't
            # all grabbed
            starting_rects = [rect for rect in page.rects
                              if rect["y0"] == starting_line["y0"]]
            bbox[0] = min([rect["x0"] for rect in starting_rects])
            bbox[1] = starting_line["top"]
            return page.crop(bbox).extract_table(
                self.COLOUR_TABLE_SETTINGS)

    def get_layout_info(self):
        """ Gets information on the layout of the key from the user. First
        attempts to read the layout params from the config file and if it
        doesn't exist get it from user input and save it.
        """

        def read_from_layout_file():
            """ Reads from a layout file, if there are any issues reverts to
            prompting for user input.

            Parameters:
                filename    str     the filename of containing the layout
                                    details if it exists. Prompt for manual
                                    user input when None.
            Returns:
                no return value     assigns the result to self.layout_params
            """
            try:
                with open(self.key_config_filename) as f:
                    config = json.load(f)
                    self.layout_params = KeyLayout(
                        KeyForm.from_string(config[JK_KF]),  # key form
                        config[JK_SF],  # row start first page
                        config[JK_EF],  # row end first page
                        config[JK_SO] if JK_SO in config else 0,  # row start
                        config[JK_EO] if JK_EO in config else 0,  # row end
                        config[JK_NC],
                        config[JK_H])
            except FileNotFoundError:
                read_from_user_input()

        def read_from_user_input():
            """ Reads from the user input.
            """
            key_form = input(s.input_key_table_form())
            num_rows_start = int(input(s.input_key_rows_start()))
            num_rows_end = int(input(s.input_key_rows_end()))
            num_rows_start_pages = 0
            num_rows_end_pages = 0
            if self.multipage:
                num_rows_start_pages = int(input(
                    s.input_key_rows_start_pages()))
                num_rows_end_pages = int(input(s.input_key_rows_end_pages()))
            num_colours_per_row = int(input(s.input_key_colours_per_row))
            print(s.input_key_headings_desc())
            headings = []
            heading = input(s.input_key_headings())
            while heading:
                headings.append(heading)
                heading = input(s.input_key_headings())

            # Save JSON file
            with open(self.key_config_filename, "w",
                      encoding="utf-8") as f:
                json.dump({JK_KF: key_form,
                           JK_SF: num_rows_start,
                           JK_EF: num_rows_end,
                           JK_SO: num_rows_start_pages,
                           JK_EO: num_rows_end_pages,
                           JK_NC: num_colours_per_row,
                           JK_H: headings}, f, indent=4)
            self.layout_params = KeyLayout(KeyForm.from_string(key_form),
                                           num_rows_start,
                                           num_rows_end,
                                           num_rows_start_pages,
                                           num_rows_end_pages,
                                           num_colours_per_row,
                                           headings)

        read_from_layout_file()

    def save_key(self):
        """ Saves the key extracted by this extractor.

        Raises:
            ValueError  if the key is empty (i.e. there is nothing to save).

        """
        if len(self.key) <= 0:
            raise ValueError(s.empty_on_save("key"))

        with open(self.key_filename, "w") as key_file:
            writer = csv.writer(key_file, delimiter="\t")
            [writer.writerow([t.dmc_value,
                              t.identifier,
                              t.symbol,
                              t.name,
                              t.hex_colour])
             for t in self.key]
