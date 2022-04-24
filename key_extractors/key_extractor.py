from abc import ABC, abstractmethod
from key_layout import KeyLayout
from pdf_utils import TextFormat

class KeyExtractor(ABC):
    """ A super class for the different types of key extractor classes.

    Parameters:
        pdf             pdfplumber.PDF  the PDF to extract the key from.
        key_form        KeyForm         how to read they key from the PDF.
        multipage       bool            whether the key is spread over multiple
                                        pages. [default: False]
        layout_params   KeyLayout       how the columns for the key information
                                        are laid out. [default: None]

    Methods:
        __init__(pdf)                       creates a new instance of the key
                                            extractor for the
        read_from_layout_file(filename)     loads the layout params from the
                                            filename given or user input

    Abstract Methods:
        extract_key(start_page_idx, end_page_idx): extracts the key from the
                                                   given pages of the PDF.
    """

    COLOUR_TABLE_SETTINGS = {"horizontal_strategy": "text",
                             "vertical_strategy": "text",
                             "keep_blank_chars": True}

    def __init__(self, pdf, key_form):
        """ Creates a new instance of the key extractor for the given PDF.

        Paramaters:
            pdf         pdfplumber.PDF      the PDF to read the key from.
            key_form    KeyForm             how to read the key from the PDF.
        """
        self.pdf = pdf
        self.key_form = key_form
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
                    try:
                        self.layout_params = KeyLayout(
                            int(f.readline().strip()),  # Rows start
                            int(f.readline().strip()),  # Rows end
                            # Pages for the above
                            int(f.readline().strip()) if self.multipage else 0,
                            int(f.readline().strip()) if self.multipage else 0,
                            int(f.readline()),
                            [row.strip() for row in f.readlines()])
                    except ValueError as ve:
                        print(f"{TextFormat.RED}Layout file '{filename}' was "
                              f"formmatted incorrectly causing{TextFormat.END}"
                              f"\n{ve}.")
                        read_from_user_input()
            except FileNotFoundError:
                print(f"{TextFormat.RED}The layout file '{filename}' could "
                      f"not be found.{TextFormat.END} \nPrompting for user "
                      "input instead (or use <CTRL-C> to quit).")
                read_from_user_input()

        def read_from_user_input():
            """ Reads from the user input.
            # TODO: I'm not sure if this is valuable or not. Might just leave
            it for now.
            # TODO: also might be worth trying to detect automatically.
            """
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
            self.layout_params = KeyLayout(num_rows_start,
                                           num_rows_end,
                                           num_rows_start_pages,
                                           num_rows_end_pages,
                                           num_colours_per_row,
                                           headings)

        if layout_file_name:
            read_from_layout_file(layout_file_name)
        else:
            read_from_user_input()
