""" Cross Stitch Pattern Extractor.
Credit for the original of this goes to Kelly Stewart:
    https://gitlab.com/miscoined/critchpat

Usage:
  extract_pattern [-v] [-k] [-m MODE] [-o OVERLAP] PDF WIDTH HEIGHT [STARTPAGE] [ENDPAGE]

Arguments:
  PDF         input pdf path
  WIDTH       width of pattern in stitches
  HEIGHT      height of pattern in stitches
  STARTPAGE   page number of the first page of the pattern to parse.
              [default: 1]
  ENDPAGE     page number of the last page of the pattern to parse. If not
              provided and STARTPAGE is provided, parse only one page. If
              neither this nor STARTPAGE is provided, parse the whole PDF file.

Options:
  -h  -help                       show this help message and exit
  -v --verbose                    print status messages
  -k --withkey                    whether to enforce that every symbol found in
                                  the pattern is also found in the key found at
                                  pdf_name.key. [default: False]
  -o OVERLAP --overlap=OVERLAP    number of rows/columns of overlap on each
                                  page to trim before concatenating pages
  -m MODE --mode=MODE             extraction mode can either be "font" or
                                  "shape". [default: font]

  MODE:
    font:  The default extraction mode if MODE is not given. Identifies symbols
           in the pattern by extracting the text from the PDF.
    shape: Extract symbols from the PDF by attempting to identify and match
           reoccuring lines and shapes on the page. These identifiers are then
           matched up with arbitrary symbols for displaying the pattern.

Notes:
  - The page numbers start at 1 NOT 0 (i.e, if the pattern starts on page 2,
    pass 2 for start page.
  - STARTPAGE, ENDPAGE range is inclusive. The values 2, 5 will parse page 2,
    3, 4, and 5.
  - A general guideline for determining the mode is to open the pattern in a
    PDF browser. If you can select the pattern symbols and copy them it is
    probably best to use 'font'.
"""
import pdfplumber
from docopt import docopt

import resources.strings as s
from extractors.extractor_mode import ExtractorMode
from extractors.pattern_extractors.font_pattern_extractor import \
    FontPatternExtractor
from extractors.pattern_extractors.shape_pattern_extractor import \
    ShapePatternExtractor
from utils import verbose_print


def extract_from_pdf(pdf_name,
                     extractor_mode,
                     width,
                     height,
                     start_page_idx=None,
                     end_page_idx=None,
                     overlap=0,
                     withkey=False,
                     verbose=False):
    """ Extracts the pattern information from the provided PDF.

    Parameters:
        pdf_name        (str)               the name of the pdf from which to
                                            export the pattern.
        extractor_mode  (ExtractorMode)     determines how the pattern is to be
                                            read from the PDF.
        width           (int)               the width of the pattern in
                                            stitches.
        height          (int)               the height of the pattern in
                                            stitches.
        start_page_idx  (int)               the index of first page containing
                                            the pattern. [default: None]
        end_page_idx    (int)               the index of the last page
                                            containing the pattern. [default
                                            None]
        overlap         (int)               the number of cells that overlap
                                            between pattern pages. [default 0]
        withkey         (bool)              whether to ensure that every symbol
                                            found also exists in the key.
        verbose         (bool)              whether to print detailed debugging
                                            statements. [default: False]
    Raises:
        FileNotFoundError       if the pdf_name does not exist.
        FileNotFoundError       if there is no associated key file (found at
                                pdf_name.replace('pdf', 'key).
        ValueError              if the extractor_mode is unknown.
        ValueError              if no key files exists and no key page provided
    """
    if extractor_mode == ExtractorMode.UNKNOWN:
        raise ValueError(s.extractor_error())
    with pdfplumber.open(pdf_name) as pdf:
        if not pdf:
            raise ValueError

        if extractor_mode == ExtractorMode.FONT:
            extractor = FontPatternExtractor(
                pdf, pdf_name.replace(".pdf", ""))
        elif extractor_mode == ExtractorMode.SHAPE:
            extractor = ShapePatternExtractor(
                pdf, pdf_name.replace(".pdf", ""))
        verbose_print(s.extractor_load_success(), verbose)

        if withkey:
            extractor.load_key()
            verbose_print(s.key_load_success(), verbose)

        extractor.extract_pattern(
            width, height,
            start_page_idx, end_page_idx, overlap,
            withkey=withkey,
            verbose=verbose)

        extractor.save_pattern()


if __name__ == "__main__":
    def make_zero(value):
        return value if value else 0


    def subtract_one(value):
        return value - 1 if value else None


    def make_int(string):
        if not string:
            return None
        try:
            return int(string)
        except ValueError:
            raise ValueError(s.page_number_error(string)) from None


    args = docopt(__doc__)
    extract_from_pdf(args["PDF"],
                     ExtractorMode.from_string(args["--mode"]),
                     int(args["WIDTH"]),
                     int(args["HEIGHT"]),
                     start_page_idx=subtract_one(make_int(args["STARTPAGE"])),
                     end_page_idx=subtract_one(make_int(args["ENDPAGE"])),
                     overlap=make_zero(make_int(args["--overlap"])),
                     withkey=bool(args["--withkey"]),
                     verbose=bool(args["--verbose"]))
