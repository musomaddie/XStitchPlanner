from unittest.mock import MagicMock

import pytest

import resources.strings as s
from extractors.pattern_extractors.font_pattern_extractor import FontPatternExtractor

EXAMPLE_PATTERN_TABLE_1 = [
    ["1", "1", "1", "1", "2"],
    ["1", "1", "1", "2", "1"],
    ["1", "1", "2", "1", "1"],
    ["1", "2", "1", "1", "1"],
    ["2", "1", "1", "1", "1"]
]


@pytest.fixture
def extractor():
    # Using a FontPatternExtractor as the PatternExtractor is an abstract class
    extractor = FontPatternExtractor(MagicMock(), "test")
    pdf_mock = MagicMock()
    page_mock = MagicMock()
    page_mock.extract_table.return_value = EXAMPLE_PATTERN_TABLE_1
    pdf_mock.pages = [page_mock]
    extractor.pdf = pdf_mock
    extractor.key_filename = "tests/resources/existing_key_file.key"
    return extractor


@pytest.mark.parametrize("withkey", [True, False])
def test_get_row(extractor, withkey):
    extractor.symbols = ["1", "2"]
    for actual, expected in zip(extractor.get_rows(0, withkey), EXAMPLE_PATTERN_TABLE_1):
        assert actual == expected


def test_get_row_with_key_missing_symbol(extractor):
    with pytest.raises(ValueError) as e:
        extractor.get_rows(0, True)
    assert str(e.value) == s.symbol_not_in_key("1")


# TODO: I think this is broken on windows
# def test_load_key(extractor):
#     extractor.load_key()
#     result_key = ["H", "Û", "é", "*", "Y"]
#     for actual, expected in zip(extractor.symbols, result_key):
#         assert actual == expected


def test_extract_pattern(extractor):
    extractor.extract_pattern(5, 5)
    for actual, expected in zip(extractor.pattern, EXAMPLE_PATTERN_TABLE_1):
        assert actual == expected
