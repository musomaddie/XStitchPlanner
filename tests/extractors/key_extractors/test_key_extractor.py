from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.key_extractor import KeyExtractor
from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from floss_thread import Thread
from unittest.mock import MagicMock, call, patch

import json
import os
import pytest
import resources.strings as s

DIR = "tests/resources/"
FILENAME_NO = f"{DIR}key_layout_NO.json"

@pytest.fixture
def extractor():
    # The KeyExtractor requires the abstract methods to be initialised so I'm
    # using a font key extractor instead.
    return FontKeyExtractor(MagicMock(), "test")

@pytest.fixture
def extractor_w_lp():
    extractor = FontKeyExtractor(MagicMock(), "test")
    extractor.layout_params = KeyLayout(
        KeyForm.UNKNOWN, 1, 2, 3, 4, 1, ["Symbol", "Number", "Colour"])
    return extractor

@pytest.fixture
def remove_file():
    # This is a fixture so that I can ensure the created JSON file is removed
    # for the tests where I expect no JSON file to exist.
    yield
    os.remove(FILENAME_NO)

def test_Init(extractor):
    assert extractor.key_config_filename == "test_key_layout_config.json"
    assert not extractor.multipage
    assert extractor.layout_params is None
    assert len(extractor.key) == 0

def test_GetLayoutInfo_FromFileMultipage(extractor):
    extractor.key_config_filename = f"{DIR}test_key_layout_config.json"
    extractor.multipage = True
    extractor.get_layout_info()
    assert extractor.layout_params.key_form == KeyForm.FULL_LINES
    assert extractor.layout_params.n_rows_start == 1
    assert extractor.layout_params.n_rows_end == 2
    assert extractor.layout_params.n_rows_start_pages == 3
    assert extractor.layout_params.n_rows_end_pages == 4
    assert extractor.layout_params.headings == [
        "Symbol", "Strands", "Type", "Number", "Colour"]

def test_GetLayoutInfo_FromFileSinglePage(extractor):
    extractor.key_config_filename = f"{DIR}test_key_layout_single_config.json"
    extractor.get_layout_info()
    assert extractor.layout_params.key_form == KeyForm.FULL_LINES
    assert extractor.layout_params.n_rows_start == 1
    assert extractor.layout_params.n_rows_end == 2
    assert extractor.layout_params.n_rows_start_pages == 0
    assert extractor.layout_params.n_rows_end_pages == 0
    assert extractor.layout_params.headings == [
        "Symbol", "Strands", "Type", "Number", "Colour"]

@patch("extractors.key_extractors.key_extractor.input", create=True)
def test_GetLayoutInfo_NoFileMultiPage(mock_input, extractor, remove_file):
    mock_input.side_effect = ["full lines",
                              "1", "2", "3", "4", "1",
                              "Symbol", "Strands", "Type", "Number", "Colour",
                              ""]
    extractor.key_config_filename = FILENAME_NO
    extractor.multipage = True

    extractor.get_layout_info()

    assert extractor.layout_params.key_form == KeyForm.FULL_LINES
    assert extractor.layout_params.n_rows_start == 1
    assert extractor.layout_params.n_rows_end == 2
    assert extractor.layout_params.n_rows_start_pages == 3
    assert extractor.layout_params.n_rows_end_pages == 4
    assert extractor.layout_params.headings == [
        "Symbol", "Strands", "Type", "Number", "Colour"]

    # Look at the file created!
    with open(FILENAME_NO) as f:
        created_config = json.load(f)
        assert created_config["key form"] == "full lines"
        assert created_config["row start first page"] == 1
        assert created_config["row end first page"] == 2
        assert created_config["row start other pages"] == 3
        assert created_config["row end other pages"] == 4
        assert created_config["number of colours per row"] == 1
        assert created_config["column headings"] == ["Symbol", "Strands",
                                                     "Type", "Number",
                                                     "Colour"]

@patch("extractors.key_extractors.key_extractor.input", create=True)
def test_GetLayoutInfo_NoFileSinglePage(mock_input, extractor, remove_file):
    mock_input.side_effect = ["full lines",
                              "1", "2", "1",
                              "Symbol", "Strands", "Type", "Number", "Colour",
                              ""]
    extractor.key_config_filename = FILENAME_NO
    extractor.multipage = False

    extractor.get_layout_info()

    assert extractor.layout_params.key_form == KeyForm.FULL_LINES
    assert extractor.layout_params.n_rows_start == 1
    assert extractor.layout_params.n_rows_end == 2
    assert extractor.layout_params.n_rows_start_pages == 0
    assert extractor.layout_params.n_rows_end_pages == 0
    assert extractor.layout_params.headings == [
        "Symbol", "Strands", "Type", "Number", "Colour"]

    # Look at the file created!
    with open(FILENAME_NO) as f:
        created_config = json.load(f)
        assert created_config["key form"] == "full lines"
        assert created_config["row start first page"] == 1
        assert created_config["row end first page"] == 2
        assert created_config["number of colours per row"] == 1
        assert created_config["column headings"] == ["Symbol", "Strands",
                                                     "Type", "Number",
                                                     "Colour"]

# Deliberately not testing the output printed by input() as this has become
# surpsingly annoying to do. (input("x? ") does not send x to stdout in a way
# that pytest will nicely detect.

def test_SaveKey(extractor):
    # Manually create a key to save myself
    key_filename = "tests/resources/test.key"
    extractor.key = [Thread("310", "a", "a", "Black", "0"),
                     Thread("666", "R", "R", "Bright Red", "E31D42"),
                     Thread("550", "!", "!", "Violet Very Dark", "5C184E")]
    extractor.key_filename = key_filename
    extractor.save_key()

    resulting_lines = ["310\ta\ta\tBlack\t0\n",
                       "666\tR\tR\tBright Red\tE31D42\n",
                       "550\t!\t!\tViolet Very Dark\t5C184E\n"]

    with open(key_filename, "r") as f:
        for actual, expected in zip(f.readlines(), resulting_lines):
            assert actual == expected

def test_SaveKey_EmptyKey(extractor):
    with pytest.raises(AssertionError) as e:
        extractor.save_key()
        assert e == s.empty_on_save("key")

def test_GetKeyTable_NoLayoutParams(extractor_w_lp):
    with pytest.raises(AssertionError) as e:
        extractor_w_lp.get_key_table(MagicMock())
        assert e == s.no_key_layout_params()

def tets_GetKeyTable_InvalidKeyForm(extractor):
    extractor.layout_params = KeyLayout(
        "NOTHING", 0, 0, 0, 0, 0, ["Hello"])
    with pytest.raises(AssertionError) as e:
        extractor.get_key_table(MagicMock())
        assert e == s.key_form_invalid()

def test_GetKeyTable_FullLines(extractor_w_lp):
    extractor_w_lp.layout_params.key_form = KeyForm.FULL_LINES
    page_mock = MagicMock()

    extractor_w_lp.get_key_table(page_mock)

    assert len(page_mock.mock_calls) == 1
    assert page_mock.mock_calls[0] == call.extract_table()

def test_GetKeyTable_NoLines(extractor_w_lp):
    extractor_w_lp.layout_params.key_form = KeyForm.NO_LINES
    page_mock = MagicMock()

    extractor_w_lp.get_key_table(page_mock)

    assert len(page_mock.mock_calls) == 1
    assert page_mock.mock_calls[0] == call.extract_table(
        KeyExtractor.COLOUR_TABLE_SETTINGS)

def test_GetKeyTable_HeaderLine(extractor_w_lp):
    extractor_w_lp.layout_params.key_form = KeyForm.ONLY_HEADER_LINE
    page_mock = MagicMock()
    page_mock.width = 100
    page_mock.height = 100
    # I'm keeping this simple although I would like to test this more
    # thoroughly later but that will involve refactoring the get_key_table
    # method and moving the rect finder to somewhere else (probably utils).
    page_mock.rects = [
        {"width": 2, "x0": 20, "y0": 0, "top": 30},
        {"width": 20, "x0": 2, "y0": 0, "top": 30},
    ]

    extractor_w_lp.get_key_table(page_mock)

    assert len(page_mock.mock_calls) == 2
    assert page_mock.mock_calls[0] == call.crop([2, 30, 100, 100])
    assert page_mock.mock_calls[1] == call.crop().extract_table(
        KeyExtractor.COLOUR_TABLE_SETTINGS)
