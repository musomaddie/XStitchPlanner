from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from unittest.mock import MagicMock
from utils import divide_row

import pytest
import resources.strings as s

DIR = "tests/resources/"
SINGLE_CONFIG_FILE = f"{DIR}test_key_layout_single_config.json"
MULTI_CONFIG_FILE = f"{DIR}test_key_layout_config.json"

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
        ["Symbol", "Number", "Colour"])
    extractor.key_config_filename = SINGLE_CONFIG_FILE
    return extractor

@pytest.fixture
def extractor_mp():
    extractor = FontKeyExtractor(MagicMock(), "test")
    extractor.layout_params = KeyLayout(
        KeyForm.FULL_LINES, 1, 2, 2, 1, 1, ["Symbol", "Number", "Colour"])
    extractor.key_config_filename = MULTI_CONFIG_FILE
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

def test_ExtractKeyFromPage_FullTable_1Colour(extractor_sp, page_mock_1):
    extractor_sp.layout_params.n_rows_end = 1
    result = extractor_sp._extract_key_from_page(page_mock_1, True)

    assert len(result) == len(EXAMPLE_KEY_TABLE_1)
    for actual, expected in zip(result, EXAMPLE_KEY_TABLE_1):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_FullTable_2Colour(extractor_sp, page_mock_2):
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
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_ShorterTable(extractor_sp, page_mock_1):
    result = extractor_sp._extract_key_from_page(page_mock_1, True)
    expected_table = EXAMPLE_KEY_TABLE_1[:-1]

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_Multi_1Colour(extractor_mp, page_mock_1):
    result = extractor_mp._extract_key_from_page(page_mock_1, False)
    expected_table = EXAMPLE_KEY_TABLE_1[1:]

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_Multi_2Colour(extractor_mp, page_mock_2):
    expected_table = []
    extractor_mp.layout_params.n_colours_per_row = 2

    for r in [divide_row(row, 2) for row in EXAMPLE_KEY_TABLE_2[1:]]:
        expected_table.append(r[0])
        expected_table.append(r[1])
    expected_table = expected_table[:-1]
    result = extractor_mp._extract_key_from_page(page_mock_2, False)

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKeyFromPage_1Colour_MissingSymbol(extractor_sp, capsys):
    expected_table = [["", "310", "Black"]]
    page_mock = MagicMock()
    page_mock.extract_table.return_value = expected_table
    extractor_sp.layout_params.n_rows_end = 1

    result = extractor_sp._extract_key_from_page(page_mock, True)

    assert len(result) == len(expected_table)
    assert result[0].symbol == expected_table[0][0]
    assert result[0].dmc_value == expected_table[0][1]

    assert capsys.readouterr().out == s.warning_no_symbol_found("310") + "\n"

def test_ExtractKeyFromPage_2Colour_MissingSymbol(extractor_sp, capsys):
    expected_table = [["1", "310", "Black"], ["", "550", "Purple"]]
    page_mock = MagicMock()
    page_mock.extract_table.return_value = [["1", "310", "Black",
                                             "", "550", "Purple"]]
    extractor_sp.layout_params.n_rows_end = 1
    extractor_sp.layout_params.n_colours_per_row = 2

    result = extractor_sp._extract_key_from_page(page_mock, True)

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

    assert capsys.readouterr().out == s.warning_no_symbol_found("550") + "\n"

def test_ExtractKey_SinglePage(extractor_sp):
    page_mock = MagicMock()
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1

    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock]

    extractor_sp.pdf = pdf_mock
    extractor_sp.extract_key(0)

    expected_table = EXAMPLE_KEY_TABLE_1[:-1]

    assert len(extractor_sp.key) == len(expected_table)
    for actual, expected in zip(extractor_sp.key, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

def test_ExtractKey_MultiPage(extractor_mp):
    page_mock_1 = MagicMock()
    page_mock_2 = MagicMock()
    page_mock_1.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    # Doubling the pages as the values returned for the second page will not
    # work with the smaller table.
    page_mock_2.extract_table.return_value = (
        EXAMPLE_KEY_TABLE_1 + EXAMPLE_KEY_TABLE_1)

    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock_1, page_mock_2]

    extractor_mp.pdf = pdf_mock
    extractor_mp.extract_key(0, 1)

    expected_table = [EXAMPLE_KEY_TABLE_1[0],
                      EXAMPLE_KEY_TABLE_1[1],
                      EXAMPLE_KEY_TABLE_1[2],
                      EXAMPLE_KEY_TABLE_1[2],
                      EXAMPLE_KEY_TABLE_1[3],
                      EXAMPLE_KEY_TABLE_1[0]]

    assert len(extractor_mp.key) == len(expected_table)
    for actual, expected in zip(extractor_mp.key, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]
