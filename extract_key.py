"""" Cross Stitch Key Extractor for Patterns.

TODO: need a way to specify how to extract the key since it seems very
pattern specific and I don't want to have to add a custom variation for ALL of
them.

This will save the key - with additional thread information (if it was
provided) as a .tsv for future use.

Usage:
  extract_key [-v] [-m MODE] PDF [STARTPAGE] [ENDPAGE]

Arguments:
  PDF           input pdf path
  STARTPAGE     page number of the first page containing the key.
                [default: 1]
  ENDPAGE       page number of the last page containing the key. If blank only
                the page specified by STARTPAGE will be used for the key.

Options:
  -h -help              show this help message and exit
  -v --verbose          print status messages
  -m MODE --mode=MODE   extract mode can either be "font" or "shape".
                        [default: font].
  MODE:
    font:   The default extraction mode if MODE is not given. Identifies
            symbols in the key by extracting the text from the PDF. A PDF can
            typically be read using font if you can copy the symbols from it by
            selecting them.
    shape:  Extract symbols in the key by attempting to identify and then match
            reoccuring lines and shapes. These identifiers are then matched up
            with arbitrary symbols for displaying. These identifiers may bear
            no resemblance to the original symbols.
"""
from docopt import docopt
from extractor_mode import ExtractorMode
from key_extractors.font_key_extractor import FontKeyExtractor
from key_extractors.shape_key_extractor import ShapeKeyExtractor
from pdf_utils import verbose_print

import csv
import pdfplumber

def save_key(key, filename, verbose=False):
    """ Save the given key in a file with the given name.

    Parameters:
        key         list(Thread)    a list of all the threads included in the
                                    key.
        filename    str             the file name of where to save this key.
        verbose     bool            whether to print detailed debugging
                                    statements. [default: False]
    """
    with open(filename, "w") as key_file:
        writer = csv.writer(key_file)
        [writer.writerow([t.dmc_value,
                          t.identifier,
                          t.symbol,
                          t.name,
                          t.hex_colour])
         for t in key]
    verbose_print(f"Successfully wrote to {filename}", verbose)

def extract_key_from_pdf(pdf_name,
                         extractor_mode,
                         start_page_idx=None,
                         end_page_idx=None,
                         verbose=False):
    """ Extracts the key from the provided PDF file and saves it as a .key
    file.

    Parameters:
        pdf_name        (str)               the name of the PDF to export the
                                            key from.
        extractor_mode  (ExtractorMode)     determines how the key is to be
                                            read from the PDF.
        start_page_idx  (int)               the index of the first page
                                            containing the key. [default: None]
        end_page_idx    (int)               the index of the last page
                                            containing the key. [default: None]
        verbose         (bool)              whether to print detailed debugging
                                            statements. [default: False]

    Raises:
        pdfminer.pdfparser.PDFSyntaxError   if the file found at pdf_name does
                                            exist but it isn't a PDF.
        FileNotFoundError                   if the pdf_name does not exist.
        ValueError                          if the extractor_mode is unkonwn.
    """
    with pdfplumber.open(pdf_name) as pdf:
        if extractor_mode == ExtractorMode.UNKNOWN:
            raise ValueError("The extractor mode is unknown. It should either "
                             "be 'font' or 'shape'")
        if extractor_mode == ExtractorMode.FONT:
            extractor = FontKeyExtractor(pdf)
        elif extractor_mode == ExtractorMode.SHAPE:
            extractor = ShapeKeyExtractor(pdf)

        if start_page_idx is None and end_page_idx is None:
            start_page_idx = 0
        save_key(
            extractor.extract_key(start_page_idx, end_page_idx, verbose),
            pdf_name.replace(".pdf", ".key"))


if __name__ == "__main__":
    def _make_int(string):
        if string:
            try:
                return int(string)
            except ValueError:
                raise ValueError(
                    f"'{string}' is not a valid page number as it is not a "
                    "number. Please provide a valid number.") from None
        return None

    def _subtract_one(value):
        return value - 1 if value else None
    args = docopt(__doc__)
    extract_key_from_pdf(args["PDF"],
                         ExtractorMode.find_mode_from_string(args["--mode"]),
                         start_page_idx=_subtract_one(
                             _make_int(args["STARTPAGE"])),
                         end_page_idx=_subtract_one(
                             _make_int(args["ENDPAGE"])),
                         verbose=bool(args["--verbose"]))
