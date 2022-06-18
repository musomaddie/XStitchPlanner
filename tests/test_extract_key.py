from unittest.mock import ANY, call, patch

import pytest

import resources.strings as s
from extract_key import extract_key_from_pdf
from extractors.extractor_mode import ExtractorMode

TESTING_PDF = "Testing.pdf"
TESTING_PATTERN_NAME = "Testing"


def test_extract_key_from_pdf_invalid_key():
    with pytest.raises(ValueError) as e:
        extract_key_from_pdf(TESTING_PATTERN_NAME, ExtractorMode.UNKNOWN)
    assert str(e.value) == s.extractor_error()


@pytest.mark.parametrize("extractor_mode", [ExtractorMode.FONT, ExtractorMode.SHAPE])
@patch("extract_key.FontKeyExtractor")
@patch("extract_key.ShapeKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_extract_key_from_pdf_valid(
        pdfplumber_mock,
        shape_key_extractor_mock,
        font_key_extractor_mock,
        extractor_mode):
    extractor_expected_calls = [call(ANY, TESTING_PATTERN_NAME),
                                call().extract_key(None, None, False),
                                call().save_key()]
    pdfplumber_expected_calls = [call(TESTING_PDF),
                                 call().__enter__(),
                                 call().__exit__(None, None, None)]

    extract_key_from_pdf(TESTING_PDF, extractor_mode)

    assert pdfplumber_mock.mock_calls == pdfplumber_expected_calls
    if extractor_mode == ExtractorMode.FONT:
        assert font_key_extractor_mock.mock_calls == extractor_expected_calls
    elif extractor_mode == ExtractorMode.SHAPE:
        assert shape_key_extractor_mock.mock_calls == extractor_expected_calls


@patch("extract_key.FontKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_extract_key_from_pdf_correct_page_numbers(pdfplumber_mock, extractor_mock):
    start_page = 2
    end_page = 100
    extract_key_from_pdf(TESTING_PDF, ExtractorMode.FONT, start_page, end_page)

    extractor_expected_calls = [call(ANY, ANY),
                                call().extract_key(start_page, end_page, False),
                                call().save_key()]

    assert extractor_mock.mock_calls == extractor_expected_calls
