from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from extractors.key_extractors.shape_key_extractor import ShapeKeyExtractor
from unittest.mock import MagicMock
from utils import divide_row

import pytest
import resources.strings as s

DIR = "tests/resources/"
SINGLE_CONFIG_FILE = f"{DIR}test_key_layout_single_config.json"
SINGLE_CONFIG_2COLOURS_FILE = (
    f"{DIR}test_key_layout_single_2colours_config.json")
MULTI_CONFIG_FILE = f"{DIR}test_key_layout_config.json"

SINGLE_LINE = {
    "x0": 2,
    "y0": 3,
    "fill": False,
    "pts": [(3, 4), (10, 10)]
}
SINGLE_LINE_2 = {
    "x0": 2,
    "y0": 3,
    "fill": True,
    "pts": [(3, 4), (10, 10)]
}
SINGLE_LINE_STR = "c-lx1y1x8y7"
SINGLE_LINE_STR_2 = "c-lx1y1x8y7f"

SINGLE_CURVE = {
    "x0": 1,
    "y0": 1,
    "fill": False,
    "pts": [(1, 1), (2, 2), (3, 4)]
}
SINGLE_CURVE_2 = {
    "x0": 1,
    "y0": 1,
    "fill": True,
    "pts": [(1, 1), (2, 2), (3, 4)]
}
SINGLE_CURVE_STR = "cx0y0x1y1x2y3-l"
SINGLE_CURVE_STR_2 = "cx0y0x1y1x2y3f-l"
SINGLE_LINE_CURVE_STR = (f"{SINGLE_CURVE_STR.split('-')[0]}"
                         f"-{SINGLE_LINE_STR.split('-')[1]}")

SINGLE_RECT = {
    "x0": 2,
    "y0": 2,
    "fill": False,
    "pts": [(2, 2), (2, 4), (4, 4), (4, 2)]
}
SINGLE_RECT_2 = {
    "x0": 2,
    "y0": 2,
    "fill": True,
    "pts": [(2, 2), (2, 4), (4, 4), (4, 2)]
}
SINGLE_RECT_STR = "rx0y0x0y2x2y2x2y0"
SINGLE_RECT_STR_2 = "rx0y0x0y2x2y2x2y0f"

EXAMPLE_KEY_TABLE_1 = [
    [SINGLE_LINE_STR, "310", "Black"],
    [SINGLE_CURVE_STR, "550", "Violet Very Dark"],
    [SINGLE_RECT_STR, "666", "Bright Red"],
    [SINGLE_LINE_CURVE_STR, "904", "Parrot Green Very Dark"],
]

EXAMPLE_KEY_TABLE_2 = [
    [SINGLE_LINE_STR, "310", "Black",
     SINGLE_LINE_STR_2, "776", "Pink Medium"],
    [SINGLE_CURVE_STR, "550", "Violet Very Dark",
     SINGLE_CURVE_STR_2, "3747", "Blue Violet Very Light"],
    [SINGLE_RECT_STR, "666", "Bright Red",
     SINGLE_RECT_STR_2, "743", "Yellow Medium"],
    [SINGLE_LINE_CURVE_STR, "904", "Parrot Green Very Dark",
     "", "", ""]
]

colour_2_table = []
for r in [divide_row(row, 2) for row in EXAMPLE_KEY_TABLE_2]:
    colour_2_table.append(r[0])
    colour_2_table.append(r[1])
colour_2_table = colour_2_table[:-1]

def _make_mock_bbox_page(lines, curves, rects):
    page = MagicMock()
    page.lines = lines
    page.curves = curves
    page.rects = rects
    return page

def mock_within_bbox(*args, **kwargs):
    bbox = args[0]
    if bbox == (10, 10, 20, 20):
        return _make_mock_bbox_page([SINGLE_LINE], [], [])
    elif bbox == (90, 10, 100, 20):
        return _make_mock_bbox_page([SINGLE_LINE_2], [], [])
    elif bbox == (20, 20, 30, 30):
        return _make_mock_bbox_page([], [SINGLE_CURVE], [])
    elif bbox == (80, 20, 90, 30):
        return _make_mock_bbox_page([], [SINGLE_CURVE_2], [])
    elif bbox == (30, 30, 40, 40):
        return _make_mock_bbox_page([], [], [SINGLE_RECT])
    elif bbox == (70, 30, 80, 40):
        return _make_mock_bbox_page([], [], [SINGLE_RECT_2])
    elif bbox == (40, 40, 50, 50):
        return _make_mock_bbox_page([SINGLE_LINE], [SINGLE_CURVE], [])
    elif bbox == (60, 40, 70, 50):
        return _make_mock_bbox_page([SINGLE_LINE_2], [SINGLE_CURVE_2], [])
    return _make_mock_bbox_page([], [], [])

def make_bbox(x0, top, x1, bottom):
    return {"fill": False, "width": 100, "height": 100,
            "x0": x0, "top": top, "x1": x1, "bottom": bottom}

@pytest.fixture
def extractor(num_pages, num_colours, is_full_table):
    extractor = ShapeKeyExtractor(MagicMock(), "test")
    # Manually setting up the extractor params as some of the functions under
    # test expect them to exist and its faster than reading from the config
    # file again.

    if num_pages == 1:
        extractor.key_config_filename = SINGLE_CONFIG_FILE
        extractor.layout_params = KeyLayout(
            KeyForm.FULL_LINES, 1,
            1 if is_full_table else 2,
            0, 0,
            num_colours, ["Symbol", "Number", "Colour"])

    elif num_pages == 2:
        extractor.layout_params = KeyLayout(
            KeyForm.FULL_LINES, 1,
            1 if is_full_table else 2,
            1 if is_full_table else 2,
            1, num_colours, ["Symbol", "Number", "Colour"])
        extractor.key_config_filename = MULTI_CONFIG_FILE

    return extractor

@pytest.fixture
def page_mock(num_colours):

    page_mock = MagicMock()

    if num_colours == 1:
        page_mock.rects = [
            make_bbox(10, 10, 20, 20),
            make_bbox(20, 20, 30, 30),
            make_bbox(30, 30, 40, 40),
            make_bbox(40, 40, 50, 50)
        ]
        page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    elif num_colours == 2:
        page_mock.rects = [
            make_bbox(10, 10, 20, 20), make_bbox(90, 10, 100, 20),
            make_bbox(20, 20, 30, 30), make_bbox(80, 20, 90, 30),
            make_bbox(30, 30, 40, 40), make_bbox(70, 30, 80, 40),
            make_bbox(40, 40, 50, 50), make_bbox(60, 40, 70, 50)
        ]
        page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_2

    page_mock.within_bbox.side_effect = mock_within_bbox
    return page_mock

# TODO: I think there were some more cases around the behaviour of filter
# majority rects I wanted to test but that's a later thing.
# TODO: add a test (both here and font) when there are multiple colours per row
# and it is not the full table. I'm expected it to fail as the start / end
# indicies are not calculated correctly in this case.
@pytest.mark.parametrize(
    "num_pages,num_colours,is_full_table,expected_key_table,is_first_page",
    [(1, 1, True, EXAMPLE_KEY_TABLE_1, True),
     (1, 1, False, EXAMPLE_KEY_TABLE_1[:-1], True),
     (2, 1, True, EXAMPLE_KEY_TABLE_1, True),
     (2, 1, False,
      [[EXAMPLE_KEY_TABLE_1[idx - 1][0],
        EXAMPLE_KEY_TABLE_1[idx][1],
        EXAMPLE_KEY_TABLE_1[idx][2]]
       for idx in range(1, len(EXAMPLE_KEY_TABLE_1))], False),
     (1, 2, True, colour_2_table, True),
     (2, 2, True, colour_2_table, True),
     ])
def test_ExtractKeyFromPage_Passes(extractor,
                                   page_mock,
                                   expected_key_table,
                                   is_first_page):
    result, count = extractor._extract_key_from_page(
        page_mock, is_first_page, 0)

    assert len(result) == len(expected_key_table)
    symbols = ["a", "b", "c", "d", "e", "f", "g", "h"][:len(
        expected_key_table)]

    for actual, expected, symbol in zip(result, expected_key_table, symbols):
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol

def test_ExtractKeyFromPage_TooManyIdents():
    # Mock extractor
    extractor = ShapeKeyExtractor(MagicMock(), "test")
    extractor.key_config_filename = SINGLE_CONFIG_FILE
    extractor.layout_params = KeyLayout(KeyForm.FULL_LINES,
                                        1, 1, 0, 0, 1,
                                        ["Symbol", "Number", "Colour"])
    # Mock page
    page_mock = MagicMock()
    page_mock.rects = [make_bbox(0, 10, 10, 20) for _ in range(100)]

    with pytest.raises(NotImplementedError) as e:
        extractor._extract_key_from_page(page_mock, True, 0)
    assert str(e.value) == s.too_many_symbols()


@pytest.mark.parametrize("single_page", ([True, False]))
def test_extractKey_Passes(single_page):
    # Set up page mock
    page_mock = MagicMock()
    page_mock.rects = [make_bbox(10, 10, 20, 20), make_bbox(20, 20, 30, 30),
                       make_bbox(30, 30, 40, 40), make_bbox(40, 40, 50, 50)]
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    page_mock.within_bbox.side_effect = mock_within_bbox
    pdf_mock = MagicMock()
    if single_page:
        pdf_mock.pages = [page_mock]
    else:
        page_mock_2 = MagicMock()
        # TODO: these rects are cursed!
        page_mock_2.rects = [
            make_bbox(90, 10, 100, 20), make_bbox(80, 20, 90, 30),
            make_bbox(70, 30, 80, 40), make_bbox(60, 30, 80, 50)]
        page_mock_2.extract_table.return_value = (
            EXAMPLE_KEY_TABLE_1 + EXAMPLE_KEY_TABLE_1)
        page_mock_2.within_bbox.side_effect = mock_within_bbox
        pdf_mock.pages = [page_mock, page_mock_2]

    # Set up the expected table
    expected_table = (EXAMPLE_KEY_TABLE_1[:-1]
                      if single_page
                      else [
                          [SINGLE_LINE_STR, "310", "Black"],
                          [SINGLE_CURVE_STR, "550", "Violet Very Dark"],
                          [SINGLE_RECT_STR, "666", "Bright Red"],
                          [SINGLE_LINE_STR_2, "666", "Bright Red"],
                          [SINGLE_CURVE_STR_2, "904",
                           "Parrot Green Very Dark"],
                          [SINGLE_RECT_STR_2, "310", "Black"]]
                      )

    symbols = ["a", "b", "c", "d", "e", "f", "g", "h"][:len(expected_table)]

    # Set up extractor
    extractor = ShapeKeyExtractor(pdf_mock, "test")
    extractor.key_config_filename = (
        SINGLE_CONFIG_FILE if single_page else MULTI_CONFIG_FILE)

    # Call the method
    if single_page:
        extractor.extract_key(0)
    else:
        extractor.extract_key(0, 1)

    assert len(extractor.key) == len(expected_table)

    for actual, expected, symbol in zip(extractor.key,
                                        expected_table, symbols):
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol

@pytest.mark.parametrize(
    "num_colours,expected_table",
    [(2, colour_2_table)]
)
def test_ExtractKey_TwoColours(page_mock, expected_table):
    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock]

    symbols = ["a", "b", "c", "d", "e", "f", "g", "h"][:len(expected_table)]
    extractor = ShapeKeyExtractor(pdf_mock, "test")
    extractor.key_config_filename = SINGLE_CONFIG_2COLOURS_FILE

    extractor.extract_key(0)

    assert len(extractor.key) == len(expected_table)

    for actual, expected, symbol in zip(extractor.key,
                                        expected_table, symbols):
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol
