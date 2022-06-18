import csv
import json
from abc import abstractmethod

from pdfplumber.page import Page
from pdfplumber.pdf import PDF

import floss_thread
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

    Methods:
        __init__(pdf)
        get_key_table(page): returns a table to extract the thread values from if required by the
            KeyForm.
        read_from_layout_file(): loads the layout params
        save_key(): saves the key that has been extracted

    Abstract Methods:
        extract_key(start_page_idx, end_page_idx): extracts the key from the given pages of the PDF.
    """
    key_config_filename: str
    multipage: bool
    layout_params: KeyLayout
    key: list[floss_thread.Thread]

    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}

    def __init__(self, pdf: PDF, pattern_name: str):
        super().__init__(pdf, pattern_name)
        self.key_config_filename = s.filename_key_config(pattern_name)
        self.multipage = False
        self.layout_params = None
        self.key = []

    @abstractmethod
    def extract_key(
            self,
            key_start_page_idx: int,
            key_end_page_idx: int = None,
            verbose: bool = False) -> None:
        """
        Extracts the key which is found on the page range provided and saves it to self.key

        Args:
            key_start_page_idx: the first page where the key can be found
            key_end_page_idx:   the last page where the key can be found
            verbose: whether to print detailed messages
        """
        pass

    def get_key_table(self, page: Page) -> list[list[str]]:
        """
        Returns the table containing the key on the given page to be used as part of the extraction
        process.

        Args:
            page: the page the key is on

        Returns:
            list[list[str]]: a list of lists where the contents of the list is the text found in
                that row of the table.

        Raises:
            ValueError:     if the key has no layout params
            ValueError:     if the key form is not recognised
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
            # Getting all the rects in this vertical line in case they weren't all grabbed
            starting_rects = [rect for rect in page.rects if rect["y0"] == starting_line["y0"]]
            bbox[0] = min([rect["x0"] for rect in starting_rects])
            bbox[1] = starting_line["top"]
            return page.crop(bbox).extract_table(
                self.COLOUR_TABLE_SETTINGS)

    def get_layout_info(self):
        """ Gets information on the layout of the key from the user. First attempts to read the
        layout params from the config file and if it doesn't exist get it from user input and
        save it.
        """

        def read_from_layout_file():
            """ Reads from a layout file, if there are any issues reverts to prompting for user
            input.
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
            """ Reads from the user input and saves it as a JSON file for future use. """
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
