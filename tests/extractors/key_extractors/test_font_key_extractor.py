from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from unittest.mock import MagicMock
from utils import divide_row

import pytest
import resources.strings as s

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

EXPECTED_TABLE_2 = [
    ["1", "310", "Black"],
    ["5", "776", "Pink Medium"],
    ["2", "550", "Violet Very Dark"],
    ["6", "3747", "Blue Violet Very Light"],
    ["3", "666", "Bright Red"],
    ["7", "743", "Yellow Medium"],
    ["4", "904", "Parrot Green Very Dark"]
]

MISSING_SYMBOL_T1 = [["", "310", "Black"]]
MISSING_SYMBOL_T2 = [["1", "310", "Black", "", "550", "Purple"]]

ARGUMENTS = [
    "is_multi_page", "num_colours", "extracted_table",   # fixtures
    "using_first_page", "expected_table"  # results
]

@pytest.fixture
def extractor(is_multi_page, num_colours):
    extractor = FontKeyExtractor(MagicMock(), "test")
    extractor.layout_params = KeyLayout(
        KeyForm.FULL_LINES, 1, 2,
        2 if is_multi_page else 0,
        1 if is_multi_page else 0,
        num_colours, ["Symbol", "Number", "Colour"])
    extractor.multipage = is_multi_page
    prefix = "tests/resources/test_key_layout_"
    extractor.key_config_filename = (
        f"{prefix}config.json" if is_multi_page
        else f"{prefix}single_config.json")
    return extractor

@pytest.fixture
def page_mock(num_colours, extracted_table):
    page_mock = MagicMock()
    page_mock.extract_table.return_value = extracted_table
    return page_mock

@pytest.fixture
def pdf_mock(is_multi_page):
    pdf_mock = MagicMock()
    page_mock = MagicMock()
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    pdf_mock.pages = [page_mock]

    if is_multi_page:
        page_mock_2 = MagicMock()
        # Doubling the table returned for the second page as the layout params
        # from the config file will have the start / end overlap with the
        # smaller table.
        page_mock_2.extract_table.return_value = (
            EXAMPLE_KEY_TABLE_1 + EXAMPLE_KEY_TABLE_1)
        pdf_mock.pages.append(page_mock_2)

    return pdf_mock


@pytest.mark.parametrize(
    ",".join(ARGUMENTS),
    [(False, 1, EXAMPLE_KEY_TABLE_1, True, EXAMPLE_KEY_TABLE_1),
     (False, 2, EXAMPLE_KEY_TABLE_2, True, EXPECTED_TABLE_2),
     (True, 1, EXAMPLE_KEY_TABLE_1, False, EXAMPLE_KEY_TABLE_1[1:]),
     (True, 2, EXAMPLE_KEY_TABLE_2, False, EXPECTED_TABLE_2[2:])]
)
def test_ExtractKeyFromPage_FullTable(extractor,
                                      page_mock,
                                      using_first_page,
                                      expected_table):
    extractor.layout_params.n_rows_end = 1
    result = extractor._extract_key_from_page(page_mock, using_first_page)

    assert len(result) == len(expected_table)
    for actual, expected in zip(result, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]

# def test_ExtractKeyFromPage_ShorterTable(extractor, page_mock_1):
    # result = extractor_sp._extract_key_from_page(page_mock_1, True)
    # expected_table = EXAMPLE_KEY_TABLE_1[:-1]

    # assert len(result) == len(expected_table)
    # for actual, expected in zip(result, expected_table):
        # assert actual.symbol == expected[0]
        # assert actual.dmc_value == expected[1]

@pytest.mark.parametrize(
    ",".join(ARGUMENTS + ["missing_symbol"]),
    [(False, 1, MISSING_SYMBOL_T1, True, MISSING_SYMBOL_T1, "310"),
     (False, 2, MISSING_SYMBOL_T2, True,
      [MISSING_SYMBOL_T2[0][:3], MISSING_SYMBOL_T2[0][3:]], "550"),
     (True, 1,  [["2", "550", "Purple"], MISSING_SYMBOL_T1[0]], False,
      MISSING_SYMBOL_T1, "310"),
     (True, 2,
      [["2", "666", "Red", "3", "904", "Green"], MISSING_SYMBOL_T2[0]],
      False, [MISSING_SYMBOL_T2[0][:3], MISSING_SYMBOL_T2[0][3:]], "550")]
)
def test_ExtractKeyFromPage_MissingSymbol(extractor,
                                          page_mock,
                                          capsys,
                                          using_first_page,
                                          expected_table,
                                          missing_symbol):
     extractor.layout_params.n_rows_end = 1

     result = extractor._extract_key_from_page(page_mock, using_first_page)

     assert len(result) == len(expected_table)
     for actual, expected in zip(result, expected_table):
         assert actual.symbol == expected[0]
         assert actual.dmc_value == expected[1]
     assert capsys.readouterr().out == s.warning_no_symbol_found(
         missing_symbol) + "\n"


# def test_ExtractKeyFromPage_2Colour_MissingSymbol(extractor_sp, capsys):
    # expected_table = [["1", "310", "Black"], ["", "550", "Purple"]]
    # page_mock = MagicMock()
    # page_mock.extract_table.return_value = [["1", "310", "Black",
                                             # "", "550", "Purple"]]
    # extractor_sp.layout_params.n_rows_end = 1
    # extractor_sp.layout_params.n_colours_per_row = 2

    # result = extractor_sp._extract_key_from_page(page_mock, True)

    # assert len(result) == len(expected_table)
    # for actual, expected in zip(result, expected_table):
        # assert actual.symbol == expected[0]
        # assert actual.dmc_value == expected[1]

    # assert capsys.readouterr().out == s.warning_no_symbol_found("550") + "\n"

@pytest.mark.parametrize(
    ",".join(["is_multi_page", "num_colours",
              "expected_table", "ek_arguments"]),
    [(False, 1, EXAMPLE_KEY_TABLE_1[:-1], (0,)),
     (True, 1, [EXAMPLE_KEY_TABLE_1[0], EXAMPLE_KEY_TABLE_1[1],
                EXAMPLE_KEY_TABLE_1[2], EXAMPLE_KEY_TABLE_1[2],
                EXAMPLE_KEY_TABLE_1[3], EXAMPLE_KEY_TABLE_1[0]], (0, 1))]
)
def test_ExtractKey_Valid(extractor, pdf_mock,
                          expected_table, ek_arguments):
    extractor.pdf = pdf_mock
    if len(ek_arguments) == 1:
        extractor.extract_key(ek_arguments[0])
    else:
        extractor.extract_key(ek_arguments[0], ek_arguments[1])


    assert len(extractor.key) == len(expected_table)
    for actual, expected in zip(extractor.key, expected_table):
        assert actual.symbol == expected[0]
        assert actual.dmc_value == expected[1]
