"""" Cross Stitch Key Extractor for Patterns.
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
import pdfplumber
from docopt import docopt

import resources.strings as s
from extractors.extractor_mode import ExtractorMode
from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.shape_key_extractor import ShapeKeyExtractor


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
        extractor_mode  (ExtractorMode)     determines how the symbols in the
                                            key are to be read from the PDF.
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
        ValueError                          if the extractor_mode is unknown.
        ValueError                          if the key_form is unknown.
    """
    if extractor_mode == ExtractorMode.UNKNOWN:
        raise ValueError(s.extractor_error())
    with pdfplumber.open(pdf_name) as pdf:
        if extractor_mode == ExtractorMode.FONT:
            extractor = FontKeyExtractor(pdf, pdf_name.replace(".pdf", ""))
        elif extractor_mode == ExtractorMode.SHAPE:
            extractor = ShapeKeyExtractor(pdf, pdf_name.replace(".pdf", ""))

        extractor.extract_key(start_page_idx, end_page_idx)
        extractor.save_key()


if __name__ == "__main__":
    def _make_int(string):
        if string:
            try:
                return int(string)
            except ValueError:
                raise ValueError(s.page_number_error(string))
        return None


    def _subtract_one(value):
        return value - 1 if value else None


    args = docopt(__doc__)
    extract_key_from_pdf(args["PDF"],
                         ExtractorMode.from_string(args["--mode"]),
                         start_page_idx=_subtract_one(
                             _make_int(args["STARTPAGE"])),
                         end_page_idx=_subtract_one(
                             _make_int(args["ENDPAGE"])),
                         verbose=bool(args["--verbose"]))
