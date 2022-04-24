""" This file contains any common utility functions that are required by
multiple PDF extractors regardless of mode and type.

Functions are found in alphabetical order.
"""
from floss_thread import Thread
from string import ascii_letters, punctuation

import csv

DMC_KEY = "dmc"
DESC_KEY = "desc"
HEX_KEY = "hex"

PLACEHOLDERS = ascii_letters + punctuation.replace(",", "").replace(" ", "")


class TextFormat:
    # PURPLE = '\033[95m'
    # CYAN = '\033[96m'
    # DARKCYAN = '\033[36m'
    # BLUE = '\033[94m'
    # GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    RED = '\033[91m'
    BRIGHT_RED = '\033[31;1m'

    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'
    END = '\033[0m'

def bbox_to_ident(page, bbox, verbose=False):
    """ Given a symbol in the PDF made up of lines and curves and
    transforms it into a string that will be consistently recognised as an
    identifier across the pattern.

    Parameters:
        page:   pdfplumber.Page     the page we are interested in.
        bbox:                       the bounding box containing the symbol.
        verbose: bool               whether to print detailed messages.
                                    [default: False]
    Returns:
        ident:  string      the string identifier generated from the list
                            of lines and curves.
    """
    def objs_ident(objs, prefix):
        # Saving the fill as well as x and y as may need to differinate between
        # a blank circle and a full circle.
        coords = []
        for obj in objs:
            string = ""
            for x, y in obj['pts']:
                string += f"x{int(x - obj['x0'])}y{int(y - obj['y0'])}"
            string += "f" if obj["fill"] else ""
            coords.append(string)
        return [prefix + "".join(sorted(coords))]
    page_sect = page.within_bbox(bbox)

    # If there are no lines and curves we can try using rects instead.
    if len(page_sect.curves) == 0 and len(page_sect.lines) == 0:
        # Make sure that the rect it has doesn't match the bbox by checking the
        # x0 coordinate with the given bbox. This is required as there are some
        # cases where the bbox is not passed.
        check_rects = []
        for rect in page_sect.rects:
            if rect["x0"] != bbox[0]:
                check_rects.append(rect)

        if len(check_rects) == 0:
            verbose_print(
                "This symbol has no curves lines or rects (besides the bbox) "
                f"found at {bbox}", verbose)
            return ""
        return "-".join(sorted(
            objs_ident(check_rects, "r")))

    return "-".join(sorted(
        objs_ident(page_sect.curves, "c") + objs_ident(
            page_sect.lines, "l")))

def determine_pages(page_start_idx, page_end_idx):
    """ Determines which page numbers are we are interested in exporting. Both
    values can be None but page_start_idx must have a value if page_end_idx
    does.

    Parameters:
        page_start_idx      int     the index of the first page
        page_end_idx        int     the index of the last page

    Returns:
        tuple[int, int]         the determined pages to export from (inclusive)
    """
    if page_start_idx is None and page_end_idx is None:
        return (0, 0)
    if not page_end_idx:
        return (page_start_idx, page_start_idx)
    return (page_start_idx, page_end_idx)

def divide_row(row, n):
    """ Divides the given row into n rows and returns them as a list of lists.

    Paramaters:
        row     list[str]   the row to divide
        n       int         the number to divide the row by.

    Returns:
        list[list[str]]     a list of lists containing the split lists.

    Raises:
        AssertionError      if the list cannot be evenly divided.
    """
    assert len(row) % n == 0, ("The row does not evenly divide into the "
                               "number of colours provided.")
    sub_size = len(row) // n
    return [row[i * sub_size:(i + 1) * sub_size] for i in range(n)]

def load_dmc_data(filename="dmc_data.csv"):
    """ Loads the additional data about all dmc colours from the given file.

    Parameters:
        filename    str     the filename containing the additional dmc data
                            the file must have a header row with the following
                            columns (exactly): `Foss#, Description, Hex`
                            the order and additional columns do not matter.
                            [default: dmc_data.csv]
    Returns:
        dict[str: dict[str: str]]       a dictionary of dmc_value to a
                                        dictionary containing the description
                                        and hex, with the following keys:
                                        `desc, hex`.

    Raises:
        FileNotFoundError   if file cannot be found.
        KeyError            if the file is missing a required column name
    """
    resulting_dict = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            resulting_dict[row["Floss#"]] = {DESC_KEY: row["Description"],
                                             HEX_KEY: row["Hex"]}
    return resulting_dict

def make_thread(dmc_value, ident, symbol, verbose=False):
    """ Returns a Thread constructed by the given parameters with additional
    detail from the dmc data passed. TODO: improve description its BAD

    Parameters:
        dmc_value   str                 the dmc_value of this thread
        ident       str                 the unique identifier of this thread
        symbol      str                 the unique symbol of this thread
        desc        str                 the description of this thread colour
                                        [default: None]
        verbose     bool                whether to print additional information
                                        [default: False]

    Returns:
        Thread      the newly constructed thread type containing the given
                    information.
    """
    if dmc_value not in DMC_DATA:
        print(f"{TextFormat.BRIGHT_RED}WARNING '{dmc_value}' is not found in "
              "our database. Default (black) description and hex code have "
              f"been assigned instead.{TextFormat.END}")
        return Thread(dmc_value,
                      ident,
                      symbol,
                      DMC_DATA["310"][DESC_KEY],
                      DMC_DATA["310"][HEX_KEY])

    return Thread(dmc_value,
                  ident,
                  symbol,
                  DMC_DATA[dmc_value][DESC_KEY],
                  DMC_DATA[dmc_value][HEX_KEY])

def read_key(filename, verbose=False):
    """ Reads the key from the given filename.

    Parameters:
        filename    str     the filename where the key can be found.
        verbose     bool    whether to print detailed debug messages.

    Returns:
        list[thread]    a list of threads that are found in this pattern.

    Raises:
        FileNotFoundError   if the file with the given filename doesn't exist.
    """
    with open(filename) as key_file:
        reader = csv.reader(key_file, delimiter="\t")
        # For whatever reason unpacking the arguments using *row isn't working
        # so I'm doing it the more manual way.
        return [Thread(row[0], row[1], row[2], row[3], row[4])
                for row in reader]

def verbose_print(message, verbose=True):
    """ Prints the given message if verbose is set to true. """
    if verbose:
        print(message)


DMC_DATA = load_dmc_data()
