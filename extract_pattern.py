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
from extractor_mode import ExtractorMode
from docopt import docopt

import pdfplumber

"""
API DOCUMENATION: TODO: BETTER OPENING and use consistent language/ terms.


Methods:
    extract_pdf(pdf_name):        extracts the pattern from the given pdf.
"""

def _open_pdf(pdf_name):
    """ Helper method to open PDFs using pdfplumber.

    Parameters:
        pdf_name    (str)   the name of the pdf to open.

    Returns:
        pdfplumber.PDF      if a file exists with the name pdf_name.pdf
        None                if no file was found.

    """
    try:
        with pdfplumber.open(pdf_name) as pdf:
            return pdf
    except FileNotFoundError:
        print(f"The PDF {pdf_name} could not be found.")
        return None

def extract_pdf(pdf_name, extractor_mode):
    """ Extracts the pattern information from the provided PDF.

    Parameters:
        pdf_name        (str)               the name of the pdf from which to
                                            export the pattern.
        extractor_mode  (ExtractorMode)     determines how the pattern is to be
                                            read from the PDF.
    Returns:

    Raises:
        ValueError      if the pdf_name does not exist.
        ValueError      if the extractor_mode is unknown.
    """
    pdf = _open_pdf(pdf_name)
    if not pdf:
        raise ValueError(f"The file {pdf_name}.pdf does not exist.")

    if extractor_mode == ExtractorMode.UNKNOWN:
        raise ValueError("The extractor mode is unknown. It should either be"
                         '"font" or "shape"')


if __name__ == "__main__":
    args = docopt(__doc__)
    extract_pdf(args["PDF"],
                ExtractorMode.find_mode_from_string(args["--mode"])
                )
