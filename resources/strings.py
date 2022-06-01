""" This is a file to store all the strings used throughout the program.
They are all being saved as a method so that I can use f strings easily.
"""


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


def empty_on_save(item):
    return (f"No {item} to save, please ensure the {item} has first been "
            "extracted.")


def extract_pattern_no_key():
    return "Cannot extract pattern before generating or loading a key."


def extractor_load_success():
    return "Successfully loaded the extractor"


def extractor_error():
    return ("The extractor mode is unknown. It should either be 'font' or "
            "'shape'")


def filename_key_config(pattern_name):
    return f"{pattern_name}_key_layout_config.json"


def ident_string(x_value, y_value):
    return f"x{x_value}y{y_value}"


def ident_doesnt_already_exist(ident):
    return "The ident {ident} does not already exist in this pattern."


def ident_unknown(ident):
    return f"Encountered unknown identifier '{ident}' not found in key."


def input_key_colours_per_row():
    return "How many colours are there per row? "


def input_key_headings_desc():
    return ("Input the headings of the columns for the key followed by a "
            "blank line.")


def input_key_headings():
    return "Heading? "


def input_key_rows_end():
    return "How many rows from the bottom do the key values end? "


def input_key_rows_end_pages():
    return ("How many rows from the bottom do the key values end on pages "
            "besides the first one? ")


def input_key_rows_start():
    return "On what row do the key values start? "


def input_key_rows_start_pages():
    return ("On what row do the key values start on pages besides the first "
            "one? ")


def input_key_table_form():
    return ("What form is the key table in? (one of 'full lines' 'only "
            "header line', 'no lines')? ")


def key_form_invalid():
    return "Please ensure that the key form is valid."


def key_load_success():
    return "Successfully loaded the key"


def multikey_row_not_divided_evenly():
    return ("The row does not evenly divide into the number of colours "
            "provided.")


def new_row(row):
    return f"\tnew row: {row}"


def no_key_layout_params():
    return ("The key layout params must first be set up before attempting to "
            "extract a key.")


def number_of_identifiers(count):
    return f"Found {count} identifiers"


def page_load(item, idx):
    return f"Loading {item} on page {idx}"


def pages_found(si, ei):
    return f"Pages set up starting from {si} to {ei}"


def page_number_error(string):
    return (f"'{string}' is not a valid page number as it is not a number. "
            "Please provide a valid number.")


def pattern_extracting_page(idx, page_w, page_h, cur_w, cur_h):
    return (f"Extracting page {idx} ({page_w}x{page_h}), pat size {cur_w}x"
            f"{cur_h}")


def pattern_size_too_big(idx, pw, ph, cw, ch, width, height):
    return (f"Page {idx} ({pw}x{ph}) results in exceeded pattern dimensions "
            f"({cw}x{ch} vs {width}x{height}")


def pattern_uneven_height(idx, actual, expected, other_option):
    return (f"Pattern {actual} tall on page {idx} when expected {expected} or "
            f"{other_option}")


def pattern_uneven_width(idx):
    return f"Pattern uneven width on page {idx}"


def pattern_wrong_size(dimension, actual, expected):
    return (f"{actual} stitches {dimension} but expected {expected} after "
            "parsing whole pattern.")


def row_extract(item):
    return f"Starting to extract rows from {item}"


def symbol_empty(bbox):
    return ("This symbol has no curves, lines or rects (besides the bbox) "
            f"found at {bbox}")


def symbol_not_in_key(symbol):
    return f"Encounted a symbol ({symbol}) not found in the key"


def too_many_symbols():
    return ("Too many colours to automatically generated all symbols, file a "
            "bug to generate more.")


def warning_dmc_not_found(value):
    return (f"{TextFormat.BRIGHT_RED}WARNING: DMC '{value}' is not found in "
            "our database. Default (black) description and hex code have "
            f"been assigned instead.{TextFormat.END}")


def warning_no_symbol_found(number):
    return (f"{TextFormat.BRIGHT_RED}WARNING: no associated symbol could be "
            f"found for the DMC value associated with {number}. You will need "
            f"to add this to the key file manually.{TextFormat.END}")
