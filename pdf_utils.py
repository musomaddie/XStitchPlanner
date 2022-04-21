""" This file contains any common utility functions that are required by
multiple PDF extractors regardless of mode and type.

Functions are found in alphabetical order.
"""

import csv

DMC_KEY = "dmc"
DESC_KEY = "desc"
HEX_KEY = "hex"

def bbox_to_ident(page, bbox):
    """ Given a symbol in the PDF made up of lines and curves and
    transforms it into a string that will be consistently recognised as an
    identifier across the pattern.

    Parameters:
        page:   pdfplumber.Page     the page we are interested in.
        bbox:                       the bounding box containing the symbol.
    Returns:
        ident:  string      the string identifier generated from the list
                            of lines and curves.
    """
    def objs_ident(objs, prefix):
        return [
            prefix + "".join(sorted(
                [f"x{int(x - obj['x0'])}y{int(y - obj['y0'])}"
                    for x, y in obj['pts']])) for obj in objs]
    page_sect = page.within_bbox(bbox)
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
        list[dict]      a list of all the dmc threads as a dictionary with the
                        following keys: `dmc, desc, hex`.

    Raises:
        FileNotFoundError   if file cannot be found.
        KeyError            if the file is missing a required column name
    """
    resulting_rows = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            resulting_rows.append({DMC_KEY: row["Floss#"],
                                   DESC_KEY: row["Description"],
                                   HEX_KEY: row["Hex"]})

    return resulting_rows

def verbose_print(message, verbose=True):
    """ Prints the given message if verbose is set to true. """
    if verbose:
        print(message)
