from extractors.key_extractors.font_key_extractor import FontKeyExtractor
from extractors.key_extractors.key_layout import KeyForm
from unittest.mock import MagicMock, patch

import json
import os
import pytest

DIR = "tests/resources/"

@pytest.fixture
def extractor():
    # The KeyExtractor requires the abstract methods to be initialised so I'm
    # using a font key extractor instead.
    return FontKeyExtractor(MagicMock(), "test")

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
def test_GetLayoutInfo_NoFileMultiPage(mock_input, extractor):
    filename = f"{DIR}key_layout_NO.json"
    mock_input.side_effect = ["full lines",
                              "1", "2", "3", "4", "1",
                              "Symbol", "Strands", "Type", "Number", "Colour",
                              ""]
    extractor.key_config_filename = filename
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
    with open(filename) as f:
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

    # Remove the created file so I can run this again.
    os.remove(filename)

@patch("extractors.key_extractors.key_extractor.input", create=True)
def test_GetLayoutInfo_NoFileSinglePage(mock_input, extractor):
    filename = f"{DIR}key_layout_NO.json"
    mock_input.side_effect = ["full lines",
                              "1", "2", "1",
                              "Symbol", "Strands", "Type", "Number", "Colour",
                              ""]
    extractor.key_config_filename = filename
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
    with open(filename) as f:
        created_config = json.load(f)
        assert created_config["key form"] == "full lines"
        assert created_config["row start first page"] == 1
        assert created_config["row end first page"] == 2
        assert created_config["number of colours per row"] == 1
        assert created_config["column headings"] == ["Symbol", "Strands",
                                                     "Type", "Number",
                                                     "Colour"]

    # Remove the created file so I can run this again.
    os.remove(filename)

# @patch("extractors.key_extractors.key_extractor.input", create=True)
# def test_GetLayoutInfo_NoFileSingePagePrint(mock_input, extractor, capsys):
#     filename = f"{DIR}key_layout_NO.json"
#     mock_input.side_effect = ["full lines",
#                               "1", "2", "1",
#                               "Symbol", "Strands", "Type", "Number", "Colour",
#                               ""]
#     extractor.key_config_filename = filename
#     extractor.multipage = False
#     extractor.get_layout_info()
#     assert False
