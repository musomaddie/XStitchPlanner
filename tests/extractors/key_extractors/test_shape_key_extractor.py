from unittest.mock import MagicMock, patch

import pytest

import resources.strings as s
from extractors.key_extractors.key_layout import KeyForm, KeyLayout
from extractors.key_extractors.shape_key_extractor import ShapeKeyExtractor

DIR = "tests/resources/"
SINGLE_CONFIG_FILE = f"{DIR}test_key_layout_single_config.json"
SINGLE_CONFIG_2COLOURS_FILE = f"{DIR}test_key_layout_single_2colours_config.json"
MULTI_CONFIG_FILE = f"{DIR}test_key_layout_config.json"

SINGLE_LINE = {
    "fill": False,
    "pts": [(13, 4), (20, 10)]
}
SINGLE_LINE_STR = "c-lx3y6x10y0"
SINGLE_LINE_2 = {
    "fill": True,
    "pts": [(93, 5), (100, 10)]
}
SINGLE_LINE_STR_2 = "c-lx3y5x10y0f"

SINGLE_CURVE = {
    "fill": False,
    "pts": [(21, 1), (22, 2), (23, 4)]
}
SINGLE_CURVE_STR = "cx1y9x2y8x3y6-l"
SINGLE_CURVE_2 = {
    "fill": True,
    "pts": [(81, 1), (82, 2), (83, 8)]
}
SINGLE_CURVE_STR_2 = "cx1y9x2y8x3y2f-l"
SINGLE_LINE_CURVE_STR = f"{SINGLE_CURVE_STR.split('-')[0]}-{SINGLE_LINE_STR.split('-')[1]}"

SINGLE_RECT = {
    "x0": 2,
    "fill": False,
    "pts": [(32, 2), (32, 4), (34, 4), (34, 2)]
}
SINGLE_RECT_STR = "rx2y8x2y6x4y6x4y8"
SINGLE_RECT_2 = {
    "x0": 2,
    "y0": 2,
    "fill": True,
    "pts": [(72, 2), (72, 4), (74, 4), (74, 2)]
}
SINGLE_RECT_STR_2 = "rx2y8x2y6x4y6xy8f"

EXAMPLE_KEY_TABLE_1 = [
    [SINGLE_LINE_STR, "310", "Black"],
    [SINGLE_CURVE_STR, "550", "Violet Very Dark"],
    [SINGLE_RECT_STR, "666", "Bright Red"],
    [SINGLE_LINE_CURVE_STR, "904", "Parrot Green Very Dark"],
]

EXAMPLE_KEY_TABLE_2 = [
    [SINGLE_LINE_STR, "310", "Black", SINGLE_LINE_STR_2, "776", "Pink Medium"],
    [SINGLE_CURVE_STR, "550", "Violet Very Dark", SINGLE_CURVE_STR_2, "3747",
     "Blue Violet Very Light"],
    [SINGLE_RECT_STR, "666", "Bright Red", SINGLE_RECT_STR_2, "743", "Yellow Medium"],
    [SINGLE_LINE_CURVE_STR, "904", "Parrot Green Very Dark", "", "", ""]
]

EXAMPLE_KEY_TABLE_COLOUR_2 = [
    [SINGLE_LINE_STR, "310", "Black"],
    [SINGLE_LINE_STR_2, "550", "Violet Very Dark"],
    [SINGLE_CURVE_STR, "666", "Bright Red"],
    [SINGLE_CURVE_STR_2, "904", "Parrot Green Very Dark"],
    [SINGLE_RECT_STR, "776", "Pink Medium"],
    [SINGLE_RECT_STR_2, "3747", "BLue Violet Very Light"],
    [SINGLE_LINE_CURVE_STR, "743", "Yellow Medium"]
]


def bbox_fake_return_values(*args):
    bbox = args[1]
    if bbox == (10, 10, 20, 20):
        return SINGLE_LINE_STR
    elif bbox == (90, 10, 100, 20):
        return SINGLE_LINE_STR_2
    elif bbox == (20, 20, 30, 30):
        return SINGLE_CURVE_STR
    elif bbox == (80, 20, 90, 30):
        return SINGLE_CURVE_STR_2
    elif bbox == (30, 30, 40, 40):
        return SINGLE_RECT_STR
    elif bbox == (70, 30, 80, 40):
        return SINGLE_RECT_STR_2
    elif bbox == (40, 40, 50, 50):
        return SINGLE_LINE_CURVE_STR
    return ""


def make_bbox(x0, top, x1, bottom):
    return {"fill": False, "width": 100, "height": 100, "x0": x0, "top": top, "x1": x1,
            "bottom": bottom}


@pytest.fixture
def extractor(num_pages, num_colours, is_full_table):
    extractor = ShapeKeyExtractor(MagicMock(), "test")
    # Manually setting up the extractor params as some of the functions under test expect them to
    # exist and its faster than reading from the config file again.

    if num_pages == 1:
        extractor.key_config_filename = SINGLE_CONFIG_FILE
        extractor.layout_params = KeyLayout(
            KeyForm.FULL_LINES, 1, 1 if is_full_table else 2, 0, 0,
            num_colours, ["Symbol", "Number", "Colour"])

    elif num_pages == 2:
        extractor.layout_params = KeyLayout(
            KeyForm.FULL_LINES, 1, 1 if is_full_table else 2, 1 if is_full_table else 2,
            1, num_colours, ["Symbol", "Number", "Colour"])
        extractor.key_config_filename = MULTI_CONFIG_FILE

    return extractor


@pytest.fixture
def page_mock(num_colours):
    page_mock = MagicMock()

    if num_colours == 1:
        page_mock.rects = [make_bbox(10, 10, 20, 20), make_bbox(20, 20, 30, 30),
                           make_bbox(30, 30, 40, 40), make_bbox(40, 40, 50, 50)]
        page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    elif num_colours == 2:
        page_mock.rects = [make_bbox(10, 10, 20, 20), make_bbox(90, 10, 100, 20),
                           make_bbox(20, 20, 30, 30), make_bbox(80, 20, 90, 30),
                           make_bbox(30, 30, 40, 40), make_bbox(70, 30, 80, 40),
                           make_bbox(40, 40, 50, 50), make_bbox(60, 40, 70, 50)]
        page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_2
    return page_mock


# TODO (issues/23): improve the test cases for extractKeyFromPage.
@pytest.mark.parametrize(
    ("num_pages", "num_colours", "is_full_table", "expected_key_table", "is_first_page"),
    [(1, 1, True, EXAMPLE_KEY_TABLE_1, True),
     (1, 1, False, EXAMPLE_KEY_TABLE_1[:-1], True),
     (2, 1, True, EXAMPLE_KEY_TABLE_1, True),
     (2, 1, False,
      [[EXAMPLE_KEY_TABLE_1[idx - 1][0],
        EXAMPLE_KEY_TABLE_1[idx][1],
        EXAMPLE_KEY_TABLE_1[idx][2]]
       for idx in range(1, len(EXAMPLE_KEY_TABLE_1))], False),
     (1, 2, True, EXAMPLE_KEY_TABLE_COLOUR_2, True),
     (2, 2, True, EXAMPLE_KEY_TABLE_COLOUR_2, True)]
)
@patch("extractors.key_extractors.shape_key_extractor.bbox_to_ident")
def test_extract_key_from_page_passes(
        bbox_to_ident_mock,
        extractor,
        page_mock,
        expected_key_table,
        is_first_page):
    bbox_to_ident_mock.side_effect = bbox_fake_return_values
    result, count = extractor._extract_key_from_page(page_mock, is_first_page, 0)

    assert len(result) == len(expected_key_table)
    symbols = ["a", "b", "c", "d", "e", "f", "g", "h"][:len(expected_key_table)]

    for actual, expected, symbol in zip(result, expected_key_table, symbols):
        assert actual.identifier == expected[0], f"non matching identifiers for expected " \
                                                 f"{expected[1]}"
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol


def test_extract_key_from_page_too_many_idents():
    # Mock extractor
    extractor = ShapeKeyExtractor(MagicMock(), "test")
    extractor.key_config_filename = SINGLE_CONFIG_FILE
    extractor.layout_params = KeyLayout(KeyForm.FULL_LINES, 1, 1, 0, 0, 1,
                                        ["Symbol", "Number", "Colour"])
    # Mock page
    page_mock = MagicMock()
    page_mock.rects = [make_bbox(0, 10, 10, 20) for _ in range(100)]

    with pytest.raises(NotImplementedError) as e:
        extractor._extract_key_from_page(page_mock, True, 0)
    assert str(e.value) == s.too_many_symbols()


@pytest.mark.parametrize("single_page", ([True, False]))
@patch("extractors.key_extractors.shape_key_extractor.bbox_to_ident")
def test_extract_key_passes(bbox_to_ident_mock, single_page):
    bbox_to_ident_mock.side_effect = bbox_fake_return_values
    # Set up page mock
    page_mock = MagicMock()
    page_mock.rects = [make_bbox(10, 10, 20, 20), make_bbox(20, 20, 30, 30),
                       make_bbox(30, 30, 40, 40), make_bbox(40, 40, 50, 50)]
    page_mock.extract_table.return_value = EXAMPLE_KEY_TABLE_1
    pdf_mock = MagicMock()
    if single_page:
        pdf_mock.pages = [page_mock]
    else:
        page_mock_2 = MagicMock()
        page_mock_2.rects = [
            make_bbox(90, 10, 100, 20), make_bbox(80, 20, 90, 30),
            make_bbox(70, 30, 80, 40), make_bbox(60, 30, 80, 50)]
        page_mock_2.extract_table.return_value = (EXAMPLE_KEY_TABLE_1 + EXAMPLE_KEY_TABLE_1)
        pdf_mock.pages = [page_mock, page_mock_2]

    # Set up the expected table
    expected_table = (EXAMPLE_KEY_TABLE_1[:-1] if single_page else [
        [SINGLE_LINE_STR, "310", "Black"],
        [SINGLE_CURVE_STR, "550", "Violet Very Dark"],
        [SINGLE_RECT_STR, "666", "Bright Red"],
        [SINGLE_LINE_STR_2, "666", "Bright Red"],
        [SINGLE_CURVE_STR_2, "904", "Parrot Green Very Dark"],
        [SINGLE_RECT_STR_2, "310", "Black"]])

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

    for actual, expected, symbol in zip(extractor.key, expected_table, symbols):
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol


@pytest.mark.parametrize(
    ("num_colours", "expected_table"), [(2, EXAMPLE_KEY_TABLE_COLOUR_2)]
)
@patch("extractors.key_extractors.shape_key_extractor.bbox_to_ident")
def test_extract_key_two_colours(bbox_to_ident_mock, page_mock, expected_table):
    bbox_to_ident_mock.side_effect = bbox_fake_return_values
    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock]

    symbols = ["a", "b", "c", "d", "e", "f", "g", "h"][:len(expected_table)]
    extractor = ShapeKeyExtractor(pdf_mock, "test")
    extractor.key_config_filename = SINGLE_CONFIG_2COLOURS_FILE

    extractor.extract_key(0)

    assert len(extractor.key) == len(expected_table)

    for actual, expected, symbol in zip(extractor.key, expected_table, symbols):
        assert actual.identifier == expected[0]
        assert actual.dmc_value == expected[1]
        assert actual.symbol == symbol
