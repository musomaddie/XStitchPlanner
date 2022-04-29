from extract_pattern import extract_from_pdf
from extractors.extractor_mode import ExtractorMode
from unittest.mock import ANY, call, patch

import pytest
import resources.strings as s

HEIGHT = 300
TESTING_PDF = "Testing.pdf"
TESTING_PATTERN_NAME = "Testing"
WIDTH = 300

PDFPLUMBER_EXPECTED_CALLS = [call(TESTING_PDF),
                             call().__enter__(),
                             call().__enter__().__bool__(),
                             call().__exit__(None, None, None)]

def test_ExtractFromPdf_InvalidKey():
    with pytest.raises(ValueError) as e:
        extract_from_pdf(TESTING_PATTERN_NAME, ExtractorMode.UNKNOWN,
                         WIDTH, HEIGHT)
        assert e == s.extractor_error()

@patch("extract_pattern.FontPatternExtractor")
@patch("extract_pattern.pdfplumber.open")
def test_ExtractFromPdf_FontPdf(pdfplumber_mock,
                                font_pattern_extractor_mock):
    extract_from_pdf(TESTING_PDF, ExtractorMode.FONT, WIDTH, HEIGHT)

    extractor_expected_calls = [
        # Not asserting exact PDF as its covered by pdfplumber asserts
        call(ANY, TESTING_PATTERN_NAME),
        call().extract_pattern(WIDTH, HEIGHT,
                               None,  # start_page_idx
                               None,  # end_page_idx
                               0,  # overlap
                               withkey=False, verbose=False),
        call().save_pattern()]

    assert pdfplumber_mock.mock_calls == PDFPLUMBER_EXPECTED_CALLS
    assert font_pattern_extractor_mock.mock_calls == extractor_expected_calls

@patch("extract_pattern.ShapePatternExtractor")
@patch("extract_pattern.pdfplumber.open")
def test_ExtractFromPdf_ShapePdf(pdfplumber_mock,
                                 shape_pattern_extractor_mock):
    extract_from_pdf(TESTING_PDF, ExtractorMode.SHAPE, WIDTH, HEIGHT)

    extractor_expected_calls = [
        call(ANY, TESTING_PATTERN_NAME),
        call().extract_pattern(WIDTH, HEIGHT,
                               None,  # start_page_idx
                               None,  # end_page_idx
                               0,  # overlap
                               withkey=False, verbose=False),
        call().save_pattern()]

    assert pdfplumber_mock.mock_calls == PDFPLUMBER_EXPECTED_CALLS
    assert shape_pattern_extractor_mock.mock_calls == extractor_expected_calls

@patch("extract_pattern.FontPatternExtractor")
@patch("extract_pattern.pdfplumber.open")
def test_ExtractFromPdf_CorrectArguments(pdfplumber_mock,
                                         font_pattern_extractor_mock):
    start_page_idx = 1
    end_page_idx = 100
    overlap = 3
    withkey = True
    verbose = True
    extract_from_pdf(TESTING_PDF, ExtractorMode.FONT, WIDTH, HEIGHT,
                     start_page_idx, end_page_idx, overlap,
                     withkey=withkey, verbose=verbose)

    extractor_expected_calls = [
        call(ANY, TESTING_PATTERN_NAME),
        call().load_key(),
        call().extract_pattern(WIDTH, HEIGHT,
                               start_page_idx, end_page_idx, overlap,
                               withkey=withkey, verbose=verbose),
        call().save_pattern()]

    assert font_pattern_extractor_mock.mock_calls == extractor_expected_calls
