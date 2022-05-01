from unittest.mock import MagicMock

import pytest
import resources.strings as s
import utils

class MockPage:
    def __init__(self, curves, lines, rects):
        self.curves = curves
        self.lines = lines
        self.rects = rects


SINGLE_CURVE_STR = "cx0y0x1y1x2y3"
SINGLE_LINE_STR = "lx1y1x8y7"
SINGLE_RECT_STR = "rx0y0x0y2x2y2x2y0f"
BOUNDING_BOX = [0, 0, 10, 10]

@pytest.fixture
def page_mock_lines_curves():
    """ Creates a mock of pdfplumber.Page containing lines and curves when
    bbox is called.
    """
    SINGLE_CURVE = {
        "x0": 1,
        "y0": 1,
        "fill": False,
        "pts": [(1, 1), (2, 2), (3, 4)]
    }
    SINGLE_LINE = {
        "x0": 2,
        "y0": 3,
        "fill": False,
        "pts": [(3, 4), (10, 10)]
    }
    page_mock = MagicMock()
    page_mock.within_bbox.return_value = MockPage(
        [SINGLE_CURVE], [SINGLE_LINE], [])

    return page_mock

@pytest.fixture
def page_mock_rects():
    """ Creates a mock of pdfplumber.Page containing a single rect. (not
    matching the bbox). """
    SINGLE_RECT = {
        "x0": 2,
        "y0": 2,
        "fill": True,
        "pts": [(2, 2), (2, 4), (4, 4), (4, 2)]
    }
    page_mock = MagicMock()
    page_mock.within_bbox.return_value = MockPage([], [], [SINGLE_RECT])
    return page_mock

@pytest.fixture
def page_mock_rect_matching_bbox():
    """ Creates a mock of pdfplumber.Page where the only rect matches the bbox.
    """
    page_mock = MagicMock()
    page_mock.within_bbox.return_value = MockPage(
        [], [], [{"x0": 0, "y0": 0}])
    return page_mock

@pytest.fixture
def row_to_divide():
    return ["1", "2", "3", "4", "5", "6", "7", "8"]

def test_bboxToIdent_LinesAndCurves(page_mock_lines_curves):
    result = utils.bbox_to_ident(page_mock_lines_curves, BOUNDING_BOX)
    assert result == f"{SINGLE_CURVE_STR}-{SINGLE_LINE_STR}"

def test_bboxToIdent_Rects(page_mock_rects):
    result = utils.bbox_to_ident(page_mock_rects, BOUNDING_BOX)
    assert result == SINGLE_RECT_STR

def test_bboxToIdent_RectMatchesBboxA(page_mock_rect_matching_bbox, capsys):
    result = utils.bbox_to_ident(
        page_mock_rect_matching_bbox, BOUNDING_BOX, verbose=True)

    out = capsys.readouterr().out

    assert result == ""
    assert out == s.warning_no_symbol_found(BOUNDING_BOX) + "\n"


def test_DeterminePage_BothNone():
    assert utils.determine_pages(None, None) == (0, 0)

def test_DeterminePage_EndNone():
    assert utils.determine_pages(1, None) == (1, 1)

def test_DeterminePage_BothValues():
    assert utils.determine_pages(1, 10) == (1, 10)

def test_DivideRow_Even(row_to_divide):

    assert utils.divide_row(row_to_divide, 2) == [
        ["1", "2", "3", "4"], ["5", "6", "7", "8"]]

    assert utils.divide_row(row_to_divide, 4) == [
        ["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"]]

def test_DivideRow_DoesntDivide(row_to_divide):
    with pytest.raises(AssertionError) as e:
        utils.divide_row(row_to_divide, 3)
        assert e == s.multikey_row_not_divided_evenly()
