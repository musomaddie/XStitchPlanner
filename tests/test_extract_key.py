from extract_key import extract_key_from_pdf
from extractors.extractor_mode import ExtractorMode
from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from unittest.mock import ANY, patch, MagicMock, call

import pytest
import resources.strings as s

def test_ExtractKeyFromPdf_InvalidKey():
    with pytest.raises(ValueError) as e:
        extract_key_from_pdf("Testing", ExtractorMode.UNKNOWN)
        assert e == s.extractor_error()

@patch("extract_key.FontKeyExtractor")
@patch("extract_key.pdfplumber.open")
def test_ExtractKeyFromPdf_FontPdf(pdfplumber_mock,
                                   font_key_extractor_mock):
    extract_key_from_pdf("Testing.pdf", ExtractorMode.FONT)

    extractor_expected_calls = [call(ANY, "Testing"),  # Not asserting exact
                                # PDf here because it's covered by calls below
                                call().extract_key(None, None),
                                call().save_key()]
    pdfplumber_expected_calls = [call("Testing.pdf"),
                                 call().__enter__(),
                                 call().__exit__(None, None, None)]

    assert font_key_extractor_mock.mock_calls == extractor_expected_calls
    assert pdfplumber_mock.mock_calls == pdfplumber_expected_calls
