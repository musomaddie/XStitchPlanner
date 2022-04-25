from abc import abstractmethod
from extractors.extractor import Extractor
from key_layout import KeyForm, KeyLayout
from pdf_utils import TextFormat

import json

# Variables for JSON keys (just to make them obvious / consistent.
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
        pdf             pdfplumber.PDF  the PDF to extract the key from.
        pattern_name    str             the name of the pattern (filename with
                                        .pdf removed).
        multipage       bool            whether the key is spread over multiple
                                        pages. [default: False]
        layout_params   KeyLayout       how the columns for the key information
                                        are laid out. [default: None]

    Methods:
        __init__(pdf)                       creates a new instance of the key
                                            extractor for the given PDF
        get_key_table(page)                 return a table to extract the
                                            values from depending on the
                                            KeyForm in layout params
        read_from_layout_file(filename)     loads the layout params from the
                                            filename given or user input

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
        self.multipage = False
        self.layout_params = None

    @abstractmethod
    def extract_key(self,
                    key_start_page_idx,
                    key_end_page_idx=None,
                    layout_file_name=None,
                    verbose=False):
        """ Extracts the key which is found on the key page range provided.

        Parameters:
            key_start_page_idx  int     The first page where the key can be
                                        found.
            key_end_page_idx    int     The last page where the key can be
                                        found. If this is not passed only the
                                        page specified by key_start_page_idx is
                                        parsed. [default: None]
            layout_file_name    str     the name of the associated key_layout
                                        file if it exists (None otherwise)
                                        [default: None]
                                        associated layout file [default: False]
            verbose             bool    whether to print detailed messages
                                        [default: False]
        Returns:
            list(Thread)        a list of of all the threads contained in this
                                pattern.
        """
        pass

    def get_key_table(self, page):
        assert self.layout_params, ("The Layout Params must first be set up "
                                    "before attempting to extract a table.")
        assert self.layout_params.key_form != KeyForm.UNKNOWN, (
            "Please ensure that the key form is valid.")

        if self.layout_params.key_form == KeyForm.FULL_LINES:
            return page.extract_table()
        if self.layout_params.key_form == KeyForm.NO_LINES:
            return page.extract_table(self.COLOUR_TABLE_SETTINGS)
        if self.layout_params.key_form == KeyForm.ONLY_HEADER_LINE:
            # TODO: need an alternative way if the rect isn't a longer one.
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

    def get_layout_info(self, layout_file_name=None):
        """ Gets information on the layout of the key from the user.

        Parameters:
            layout_file_name    str     the name of the associated key_layout
                                        file if it exists (None otherwise)
                                        [default: None]
        """
        def read_from_layout_file(filename):
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
                with open(filename) as f:
                    config = json.load(f)
                    self.layout_params = KeyLayout(
                        KeyForm.from_string(config[JK_KF]),  # key form
                        config[JK_SF],  # row start first page
                        config[JK_EF],  # row end first page
                        config[JK_SO] if JK_SO in config else 0,  # row start
                        config[JK_EO] if JK_EO in config else 0,  # row end
                        config[JK_NC],
                        config[JK_H])
                    # TODO: what happens if it's a string??
            except FileNotFoundError:
                print(f"{TextFormat.RED}The layout file '{filename}' could "
                      f"not be found.{TextFormat.END} \nPrompting for user "
                      "input instead (or use <CTRL-C> to force quit).")
                read_from_user_input()

        def read_from_user_input():
            """ Reads from the user input.
            # TODO: I'm not sure if this is valuable or not. Might just leave
            it for now.
            # TODO: also might be worth trying to detect automatically.
            """
            key_form = input("What form is the key table in? (one of 'full "
                             "lines', 'only header line', 'no lines'")
            num_rows_start = int(
                input("On what row do the key values start? "))
            num_rows_end = int(input("How many rows from the bottom do the "
                                     "key values end? "))
            num_rows_end_pages = 1
            num_rows_start_pages = 1
            if self.multipage:
                num_rows_start_pages = int(input("On what row does it start "
                                                 "on other pages? "))
                num_rows_end_pages = int(input("How many rows from the bottom "
                                               "do they end on future pages? "
                                               ))
            num_colours_per_row = int(
                input("How many colours are there per row? "))
            print("Input the headings of the columns for the key followed by "
                  "a blank line.")
            headings = []
            heading = input("Heading? ")
            while heading:
                headings.append(heading)
                heading = input("Heading? ")
            headings = ["Symbol", "Strands", "Type", "Number", "Colour"]
            self.layout_params = KeyLayout(key_form,
                                           num_rows_start,
                                           num_rows_end,
                                           num_rows_start_pages,
                                           num_rows_end_pages,
                                           num_colours_per_row,
                                           headings)

        if layout_file_name:
            read_from_layout_file(layout_file_name)
        else:
            read_from_user_input()
