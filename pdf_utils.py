""" This file contains any common utility functions that are required by
multiple PDF extractors regardless of mode and type.

Functions are found in alphabetical order.
"""
from floss_thread import Thread
import csv

DMC_KEY = "dmc"
DESC_KEY = "desc"
HEX_KEY = "hex"


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
        # Will always at least have the bbox.
        if len(page_sect.rects) == 1:
            verbose_print(
                "This symbol has no curves lines or rects (besides the bbox) "
                "found at X", verbose)
            return ""
        return "-".join(sorted(
            objs_ident(page_sect.rects[1:], "r")))

    return "-".join(sorted(
        objs_ident(page_sect.curves, "c") + objs_ident(
            page_sect.lines, "l")))

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

def make_thread(dmc_value, ident, symbol, desc=None, verbose=False):
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
    return Thread(dmc_value,
                  ident,
                  symbol,
                  desc.title() if desc else DMC_DATA[dmc_value][DESC_KEY],
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
