from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from floss_thread import Thread
from unittest.mock import MagicMock
from utils import divide_row

import pytest

DIR = "tests/resources/"

EXAMPLE_KEY_TABLE_1 = [
    ["1", "310", "Black"],
    ["2", "550", "Violet Very Dark"],
    ["3", "666", "Bright Red"],
    ["4", "904", "Parrot Green Very Dark"]
]

EXAMPLE_KEY_TABLE_2 = [
    ["1", "310", "Black", "5", "776", "Pink Medium"],
    ["2", "550", "Violet Very Dark", "6", "3747", "Blue Violet Very Light"],
    ["3", "666", "Bright Red", "7", "743", "Yellow Medium"],
    ["4", "904", "Parrot Green Very Dark", "", "", ""]
]

@pytest.fixture
def extractor_sp():
    extractor = FontKeyExtractor(MagicMock(), "test")
    # Manually providing layout params as get_key_table called in
    # extract_key_from_page expects them to be created.
    extractor.layout_params = KeyLayout(
        KeyForm.FULL_LINES, 1, 2, 0, 0, 1,
        ["Symbol", "Number", "Colour", "Hex"])
    return extractor

@pytest.fixture
def page_mock_1():
    page_mock = MagicMock()
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    return page_mock

@pytest.fixture
def page_mock_2():
    page_mock = MagicMock()
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_2
    return page_mock


def test_ExtractKeyFromPage_SinglePage_FullTable_1Colour(extractor_sp,
                                                         page_mock_1):
    extractor_sp.layout_params.n_rows_end = 1
    result = extractor_sp._extract_key_from_page(page_mock_1, True)

    assert len(result) == len(EXAMPLE_KEY_TABLE_1)
    for actual, expected in zip(result, EXAMPLE_KEY_TABLE_1):
        assert actual.symbol == expected[0]
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_SinglePage_FullTable_2Colour(extractor_sp,
                                                         page_mock_2):
    extractor_sp.layout_params.n_rows_end = 1
    extractor_sp.layout_params.n_colours_per_row = 2

    # I know divide row already works (thanks to test_util) so I can use it
    expected_table = []
    for r in [divide_row(row, 2) for row in EXAMPLE_KEY_TABLE_2]:
        expected_table.append(r[0])
        expected_table.append(r[1])
    expected_table = expected_table[:-1]

    result = extractor_sp._extract_key_from_page(page_mock_2, True)

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
