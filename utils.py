""" This file contains any common utility functions that are required by multiple PDF extractors
regardless of mode and type.

Functions are found in alphabetical order.
"""
import csv
from string import ascii_letters, punctuation

from pdfplumber.page import Page

import resources.strings as s
from floss_thread import Thread

DMC_KEY = "dmc"
DESC_KEY = "desc"
HEX_KEY = "hex"

PLACEHOLDERS = ascii_letters + punctuation.replace(",", "").replace(" ", "")


def bbox_to_ident(page: Page, bbox: tuple[int, int, int, int], verbose: bool = False) -> str:
    """
    Args:
        page: the page containing the symbol
        bbox: the bounding box containing the symbol (x0, top, x1, bottom)
        verbose: whether to print detailed messages

    Returns:
        str:  the string identifier generated from the list of lines and curves found within the
        bbox on the given page
    """

    left_edge = bbox[0]
    top_edge = page.height - bbox[1]  # TODO: figure out if top or bottom edge is better

    def objs_ident(objs, prefix):
        # Saving the fill as well as x and y as may need to differentiate between a blank circle
        # and a full circle.
        coords = []
        for obj in objs:
            string = ""
            for x, y in obj['pts']:
                string += s.ident_string(
                    int(x - left_edge), int(top_edge - y))
            string += "f" if obj["fill"] else ""
            coords.append(string)
        return [prefix + "".join(coords)]

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
            verbose_print(s.warning_no_symbol_found(bbox), verbose)
            return ""

        return "-".join(objs_ident(check_rects, "r"))

    return "-".join(objs_ident(page_sect.curves, "c") + objs_ident(page_sect.lines, "l"))


def determine_pages(page_start_idx: int, page_end_idx: int) -> tuple[int, int]:
    """
    Determines which page numbers to export. Both values can be None, but if
    page_end_idx is non None, so must page_start_idx

    Args:
        page_start_idx: the index of the first page
        page_end_idx: the index of the last page

    Returns:
        tuple[int, int]:  the determined pages to export from (inclusive)
    """
    if page_start_idx is None and page_end_idx is None:
        return 0, 0
    if not page_end_idx:
        return page_start_idx, page_start_idx
    return page_start_idx, page_end_idx


def divide_row(row: list[str], n: int) -> list[list[str]]:
    """
    Divides the given row into n rows and returns them as a list of lists.

    Args:
        row: the row to divide
        n: the number of divide the row by

    Returns:
        list[list[str]]: a list of lists containing the split lists

    Raises:
        ValueError:     if the provided list cannot be evenly divided.
    """
    if len(row) % n != 0:
        raise ValueError(s.multikey_row_not_divided_evenly())
    sub_size = len(row) // n
    return [row[i * sub_size:(i + 1) * sub_size] for i in range(n)]


def load_dmc_data(filename: str = "resources/dmc_data.csv") -> dict[str: dict[str: str]]:
    """
    Loads the additional data about all dmc colours from the given file.

    Args:
        filename: the filename containing the additional dmc data. The
        file: must have a header row with the following columns (exactly):
            `Foss#, Description, Hex` the order and additional columns do not matter. [default:
            dmc_data.csv]

    Returns:
        A dictionary of dmc_value to a dictionary containing the description and hex with the
        following keys: `desc, hex`.

    Raises:
        FileNotFoundError:  if the file cannot be found
        KeyError:           if the file is missing a required column name
    """
    resulting_dict = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            resulting_dict[row["Floss#"]] = {DESC_KEY: row["Description"], HEX_KEY: row["Hex"]}
    return resulting_dict


def make_thread(dmc_value: str, ident: str, symbol: str) -> Thread:
    """
    Returns a Thread object with the given dmc_value, ident and symbol.
    The hex-code colour and colour description are found from the dmc_data file.

    Args:
        dmc_value: the dmc_value of this thread
        ident: the unique identifier of this thread
        symbol: the unique symbol of this thread

    Returns:
        Thread: the newly constructed thread type with the given info
    """
    if dmc_value not in DMC_DATA:
        print(s.warning_dmc_not_found(dmc_value))
        return Thread(
            dmc_value, ident, symbol, DMC_DATA["310"][DESC_KEY], DMC_DATA["310"][HEX_KEY])

    return Thread(
        dmc_value, ident, symbol, DMC_DATA[dmc_value][DESC_KEY], DMC_DATA[dmc_value][HEX_KEY])


def read_key(filename: str) -> list[Thread]:
    """
    Reads the key from the given filename.

    Args:
        filename: the filename where the key can be found.

    Returns:
        list[Thread]:   a list of threads found in the key file

    Raises:
        FileNotFoundError:  if the file with the given filename doesn't exist
    """
    with open(filename) as key_file:
        reader = csv.reader(key_file, delimiter="\t")
        # For whatever reason unpacking the arguments using *row isn't working,
        # so I'm doing it the more manual way.
        return [Thread(row[0], row[1], row[2], row[3], row[4]) for row in reader]


def save_pattern(
        filename: str,
        pattern: list[list[str]],
        path: str = None) -> None:
    """Saves the given pattern to the given filename.

    Args:
        filename: the filename to save the pattern in. (Excluding the path)
        pattern: the pattern details to save
        path: (optional) only pass if the saved file should not be saved in patterns/
    """
    fn = f"{path}{filename}.pat" if path else f"patterns/{filename}.pat"
    with open(fn, "w", encoding="utf-8") as f:
        print(*["".join(row) for row in pattern], sep="\n", file=f)


def verbose_print(message: str, verbose: bool = True) -> None:
    """ Prints the given message if verbose is set to true.

    Args:
        message: message to print
        verbose: print if true
    """
    if verbose:
        print(message)


DMC_DATA = load_dmc_data()
