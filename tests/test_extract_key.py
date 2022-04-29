from extract_key import extract_key_from_pdf
from extractors.extractor_mode import ExtractorMode
from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from unittest.mock import ANY, patch, MagicMock, call

import pytest
import resources.strings as s

TESTING_PDF = "Testing.pdf"
TESTING_PATTERN_NAME = "Testing"

PDFPLUMBER_EXPECTED_CALLS = [call(TESTING_PDF),
                             call().__enter__(),
                             call().__exit__(None, None, None)]

def test_ExtractKeyFromPdf_InvalidKey():
    with pytest.raises(ValueError) as e:
        extract_key_from_pdf(TESTING_PATTERN_NAME, ExtractorMode.UNKNOWN)
        assert e == s.extractor_error()

@patch("extract_key.FontKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_ExtractKeyFromPdf_FontPdf(pdfplumber_mock,
                                   font_key_extractor_mock):
    extract_key_from_pdf(TESTING_PDF, ExtractorMode.FONT)

    extractor_expected_calls = [call(ANY, TESTING_PATTERN_NAME),
                                # Not asserting exactPDf here because it's
                                # covered by pdfplumber asserts
                                call().extract_key(None, None),
                                call().save_key()]

    assert pdfplumber_mock.mock_calls == PDFPLUMBER_EXPECTED_CALLS
    assert font_key_extractor_mock.mock_calls == extractor_expected_calls

@patch("extract_key.ShapeKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_ExtractKeyFromPdf_ShapePdf(pdfplumber_mock, shape_key_extractor_mock):
    extract_key_from_pdf(TESTING_PDF, ExtractorMode.SHAPE)

    extractor_expected_calls = [call(ANY, TESTING_PATTERN_NAME),
                                call().extract_key(None, None),
                                call().save_key()]

    assert pdfplumber_mock.mock_calls == PDFPLUMBER_EXPECTED_CALLS
    assert shape_key_extractor_mock.mock_calls == extractor_expected_calls

@patch("extract_key.FontKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_ExtractKeyFromPdf_CorrectPageNumbers(pdfplumber_mock, extractor_mock):
    start_page = 2
    end_page = 100
    extract_key_from_pdf(TESTING_PDF, ExtractorMode.FONT, start_page, end_page)

    extractor_expected_calls = [call(ANY, ANY),
                                call().extract_key(start_page, end_page),
                                call().save_key()]

    assert extractor_mock.mock_calls == extractor_expected_calls
