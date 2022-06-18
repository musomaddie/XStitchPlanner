from unittest.mock import MagicMock

import pytest

import resources.strings as s
import utils
from floss_thread import Thread

BOUNDING_BOX = [0, 0, 10, 10]


class MockPage:
    def __init__(self, curves, lines, rects):
        self.curves = curves
        self.lines = lines
        self.rects = rects


def make_page_mock_for_bbox(lines, curves, rects):
    bbox_mock = MagicMock()
    bbox_mock.lines = lines
    bbox_mock.curves = curves
    bbox_mock.rects = rects

    page_mock = MagicMock()
    page_mock.height = 10
    page_mock.within_bbox.return_value = bbox_mock
    return page_mock


""" bbox_to_ident """


@pytest.mark.parametrize(
    ("page_mock", "expected_string"),
    [
        [make_page_mock_for_bbox(  # One line object
            [{"fill": False, "pts": [(3, 4), (10, 10)]}], [], []),
            "c-lx3y6x10y0"],
        [make_page_mock_for_bbox(  # Two line objects
            [{"fill": False, "pts": [(3, 4), (10, 10)]},
             {"fill": True, "pts": [(1, 2), (3, 4), (5, 6)]}], [], []),
            "c-lx3y6x10y0x1y8x3y6x5y4f"],
        [make_page_mock_for_bbox(  # One curve object
            [], [{"fill": False, "pts": [(1, 1), (2, 2), (3, 4)]}], []),
            "cx1y9x2y8x3y6-l"],
        [make_page_mock_for_bbox(  # One line, one curve
            [{"fill": False, "pts": [(1, 2), (3, 4)]}],
            [{"fill": True, "pts": [(5, 6), (7, 8), (9, 10)]}], []),
            "cx5y4x7y2x9y0f-lx1y8x3y6"],
        [make_page_mock_for_bbox(  # One rect
            [], [], [{"x0": 2, "y0": 2, "fill": True,
                      "pts": [(2, 2), (2, 4), (4, 4), (4, 2)]}]),
            "rx2y8x2y6x4y6x4y8f"],
    ])
def test_bbox_to_ident_valid(page_mock, expected_string):
    """ Scenarios tested:
        One of each line curve rect
        Two of each line (will be the same logic for rects and curves)
        Combo one line one curve
    """
    assert utils.bbox_to_ident(page_mock, BOUNDING_BOX) == expected_string


def test_bbox_to_ident_rect_matches_bbox(capsys):
    page_mock = MagicMock()
    page_mock.within_bbox.return_value = MockPage([], [], [{"x0": 0, "y0": 0}])
    result = utils.bbox_to_ident(page_mock, BOUNDING_BOX, verbose=True)

    out = capsys.readouterr().out

    assert result == ""
    assert out == s.warning_no_symbol_found(BOUNDING_BOX) + "\n"


""" determine_pages """


@pytest.mark.parametrize(
    ("s_idx", "e_idx", "se_idx", "ee_idx"),
    [(None, None, 0, 0), (1, None, 1, 1), (1, 10, 1, 10)]
)
def test_determine_page_both_none(s_idx, e_idx, se_idx, ee_idx):
    assert utils.determine_pages(s_idx, e_idx) == (se_idx, ee_idx)


""" divide_row """


def test_divide_row_even():
    row_to_divide = ["1", "2", "3", "4", "5", "6", "7", "8"]

    assert utils.divide_row(row_to_divide, 2) == [
        ["1", "2", "3", "4"], ["5", "6", "7", "8"]]

    assert utils.divide_row(row_to_divide, 4) == [
        ["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"]]


def test_divide_row_doesnt_divide():
    row_to_divide = ["1", "2", "3", "4", "5", "6", "7", "8"]
    with pytest.raises(ValueError) as e:
        utils.divide_row(row_to_divide, 3)
    assert str(e.value) == s.multikey_row_not_divided_evenly()


""" load_dmc_data """


def test_load_dmc_data_simple():
    result = utils.load_dmc_data(filename="tests/resources/dmc_data_testing.csv")
    assert len(result) == 10
    for num, key in enumerate(result.keys()):
        assert str(num + 1) == key


""" make thread """


def test_make_thread():
    dmc = "310"
    ident = "#"
    symbol = "@"
    created_thread = utils.make_thread(dmc, ident, symbol)
    assert created_thread == Thread(dmc, ident, symbol, "Black", "0")


def test_make_thread_non_database(capsys):
    dmc = "AAAA"
    ident = "#"
    symbol = "@"
    created_thread = utils.make_thread(dmc, ident, symbol)
    out = capsys.readouterr().out

    assert created_thread == Thread(dmc, ident, symbol, "Black", "0")
    assert out == s.warning_dmc_not_found(dmc) + "\n"


""" read_key """


def test_read_key():
    result = utils.read_key("tests/resources/existing_key_file.key")
    ideal_dmcs = ["152", "153", "154", "155", "159"]

    assert len(result) == 5
    for actual, expected in zip([t.dmc_value for t in result], ideal_dmcs):
        assert actual == expected
