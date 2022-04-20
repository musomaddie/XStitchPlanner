""" Cross Stitch Pattern Extractor.
As well as containing an API this extractor can be called from the command line
in which case it will save the result as a csv.

Credit for the original of this goes to Kelly Stewart:
    https://gitlab.com/miscoined/critchpat

Usage:
  extract_pattern [-v] [-m MODE] [-k PAGE | -K PATH] [-o OVERLAP] PDF WIDTH HEIGHT [STARTPAGE] [ENDPAGE]

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
  -k PAGE --keypage=PAGE          attempt to extract the key from the given
                                  page number.
  -K PATH --keypath=PATH          a file path to read the key from when
                                  extracting, used for shape mode only.
  -o OVERLAPH --overlap=OVERLAP   number of rows/columns of overlap on each
                                  page to trim before concatenating pages
  -m MODE --mode=MODE             extraction mode can either be "font" or
                                  "shape". [default: font]

  MODE:
    font:  The default extraction mode if MODE is not given. Identifies symbols
           in the pattern by extracting the text from the PDF.
    shape: Extract symbols from the PDF by attempting to identify and match
           reoccuring lines and shapes on the page. These identifiers are then
           matched up with arbitrary symbols for displaying the pattern. This
           mode requires either --keypage or --keypath to be given in order to
           generate the mapping of identifiers to symbols.
"""
from docopt import docopt
from extractor_mode import ExtractorMode
from font_pattern_extractor import FontPatternExtractor
from shape_pattern_extractor import ShapePatternExtractor

import pdfplumber

"""
API DOCUMENATION: TODO: BETTER OPENING and use consistent language/ terms.


Methods:
    extract_pdf(pdf_name):        extracts the pattern from the given pdf.
"""

def extract_from_pdf(pdf_name,
                     extractor_mode,
                     width,
                     height,
                     start_page_idx=None,
                     end_page_idx=None,
                     overlap=0,
                     verbose=False,
                     key_page=None,
                     key_path=None):
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
                                            between pattern pages. [default
                                            0]
        verbose         (bool)              whether to print detailed debugging
                                            statements. [default: False]
        key_page        (int)               the page that the key can be found
                                            on. [default: None]
        key_path        (str)               a file path to read the key from.
                                            [default: None]
    Returns:

    Raises:
        FileNotFoundError       if the pdf_name does not exist.
        ValueError              if the extractor_mode is unknown.
        ValueError              if no key files exists and no key page provided
    """
    with pdfplumber.open(pdf_name) as pdf:
        if not pdf:
            raise ValueError(f"The file {pdf_name} does not exist.")

        if extractor_mode == ExtractorMode.UNKNOWN:
            raise ValueError("The extractor mode is unknown. It should either "
                             'be "font" or "shape"')
        if extractor_mode == ExtractorMode.FONT:
            extractor = FontPatternExtractor(pdf)
        elif extractor_mode == ExtractorMode.SHAPE:
            extractor = ShapePatternExtractor(pdf)
            if not key_path and not key_page:
                try:
                    key_path = pdf_name.replace(".pdf", "_key.tsv")
                except FileNotFoundError:
                    raise ValueError(
                        "No key file exists and no key page provided.")

            if key_path:
                extractor.load_ident_map(key_path)

        if key_page:
            key = extractor.extract_key(key_page - 1)
            print(key)

        pat = extractor.extract_pattern(
            width, height, start_page_idx, end_page_idx, overlap, verbose)
        print(pat)
        print(type(pat))
        for x in pat:
            print(type(x))


if __name__ == "__main__":
    """ Bunch of random helper functions because I'm too lazy to write llambdas
    right now """
    def _make_int(string):
        """ Helper to turn all the CLI args to ints (if they exist) so that the
        extract method can take in sensible types.
        """
        if string:
            try:
                return int(string)
            except ValueError:
                return None
        return None


    def _subtract_one(v):
        """ Helper for the page idx as if they exist we need to subtract one. """
        if v:
            return v - 1
        return None

    def _make_zero(v):
        """ Helper that makes a None a 0. Again I'm lazy. """
        if not v:
            return 0
        return v

    args = docopt(__doc__)
    print(args)
    extract_from_pdf(args["PDF"],
                     ExtractorMode.find_mode_from_string(args["--mode"]),
                     int(args["WIDTH"]),
                     int(args["HEIGHT"]),
                     start_page_idx=_subtract_one(
                         _make_int(args["STARTPAGE"])),
                     end_page_idx=_subtract_one(
                         _make_int(args["ENDPAGE"])),
                     overlap=_make_zero(_make_int(args["--overlap"])),
                     verbose=bool(args["--verbose"]),
                     key_page=_make_int(args["--keypage"]),
                     key_path=args["--keypath"]
                )
