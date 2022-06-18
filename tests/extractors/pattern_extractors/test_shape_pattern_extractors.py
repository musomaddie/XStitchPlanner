from unittest.mock import MagicMock, call, patch

import pytest

import resources.strings as s
from extractors.pattern_extractors.shape_pattern_extractor import ShapePatternExtractor
from floss_thread import Thread
from utils import PLACEHOLDERS

IDENT_1 = "c-lx1y1x8y7"
IDENT_2 = "cx0y0x1y1-l"


@pytest.fixture
def extractor():
    extractor = ShapePatternExtractor(MagicMock(), "test")
    row1_mock = MagicMock()
    row1_mock.cells = [1, 2, 1]
    row2_mock = MagicMock()
    row2_mock.cells = [2, 1, 1]

    table_mock = MagicMock()
    table_mock.rows = [row1_mock, row2_mock]
    page_mock = MagicMock()
    page_mock.find_tables.return_value = [table_mock]

    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock, page_mock]

    extractor.pdf = pdf_mock
    return extractor


def setup_bbox_mock(bbox_mock):
    def fake_bbox_to_ident(page, bbox, verbose):
        if bbox == 1:
            return IDENT_1
        elif bbox == 2:
            return IDENT_2
        return ""

    bbox_mock.side_effect = fake_bbox_to_ident


@pytest.mark.parametrize(
    ("starting_placeholders", "expected_placeholders"),
    [([], PLACEHOLDERS[0]), (PLACEHOLDERS[:40], PLACEHOLDERS[40])]
)
def test_find_next_placeholder(
        extractor,
        starting_placeholders,
        expected_placeholders):
    extractor._used_symbols = [s for s in starting_placeholders]
    orig_len = len(extractor._used_symbols)
    next_placeholder = extractor._find_next_placeholder()
    assert next_placeholder == expected_placeholders
    assert len(extractor._used_symbols) == orig_len + 1
    assert extractor._used_symbols[-1] == expected_placeholders


def test_find_next_placeholder_raises_error(extractor):
    extractor._used_symbols = [s for s in PLACEHOLDERS]
    with pytest.raises(NotImplementedError) as e:
        extractor._find_next_placeholder()
    assert str(e.value) == s.too_many_symbols()


@patch("extractors.pattern_extractors.shape_pattern_extractor.bbox_to_ident")
def test_get_symbol_without_key(bbox_mock, extractor):
    # Set up bbox mock
    setup_bbox_mock(bbox_mock)

    symb = extractor._get_symbol(MagicMock(), 1)
    assert symb == PLACEHOLDERS[0]
    assert len(extractor.ident_map) == 1
    assert IDENT_1 in extractor.ident_map
    assert extractor.ident_map[IDENT_1] == symb

    # checking a second symbol
    symb = extractor._get_symbol(MagicMock(), 2)
    assert symb == PLACEHOLDERS[1]
    assert len(extractor.ident_map) == 2
    assert IDENT_2 in extractor.ident_map
    assert extractor.ident_map[IDENT_2] == symb

    # Checking it will still return it alright a second time.
    symb = extractor._get_symbol(MagicMock(), 1)
    assert symb == PLACEHOLDERS[0]
    assert len(extractor.ident_map) == 2
    assert IDENT_1 in extractor.ident_map

    symb = extractor._get_symbol(MagicMock(), 2)
    assert symb == PLACEHOLDERS[1]
    assert len(extractor.ident_map) == 2
    assert IDENT_2 in extractor.ident_map


@patch("extractors.pattern_extractors.shape_pattern_extractor.bbox_to_ident")
def test_get_symbol_with_key(bbox_mock, extractor):
    setup_bbox_mock(bbox_mock)

    extractor.ident_map[IDENT_1] = "1"
    extractor.ident_map[IDENT_2] = "2"

    symb = extractor._get_symbol(MagicMock(), 1, True)
    assert symb == "1"

    symb = extractor._get_symbol(MagicMock(), 2, True)
    assert symb == "2"


@patch("extractors.pattern_extractors.shape_pattern_extractor.bbox_to_ident")
def test_get_symbol_with_key_raises_error(bbox_mock, extractor):
    setup_bbox_mock(bbox_mock)
    expected_ident = "c-lx1y1x8y7"
    with pytest.raises(ValueError) as e:
        extractor._get_symbol(MagicMock(), 1, True)
    assert str(e.value) == s.ident_unknown(expected_ident)


@patch("extractors.pattern_extractors.shape_pattern_extractor.bbox_to_ident")
def test_get_rows(bbox_mock, extractor):
    setup_bbox_mock(bbox_mock)
    rows = extractor.get_rows(0)
    assert len(rows) == 2
    for actual, expected in zip(rows, [["a", "b", "a"], ["b", "a", "a"]]):
        assert actual == expected


@patch("extractors.pattern_extractors.shape_pattern_extractor.bbox_to_ident")
def test_extract_pattern(bbox_mock, extractor):
    setup_bbox_mock(bbox_mock)
    # I need this to work for every page / row.
    extractor.extract_pattern(3, 4, withkey=False)
    assert len(extractor.pattern) == 4

    for actual, expected in zip(extractor.pattern,
                                [["a", "b", "a"], ["b", "a", "a"],
                                 ["a", "b", "a"], ["b", "a", "a"]]):
        assert actual == expected


def test_extract_pattern_with_key_raises_error(extractor):
    with pytest.raises(ValueError) as e:
        extractor.extract_pattern(withkey=True)
    assert str(e.value) == s.extract_pattern_no_key()


@patch("extractors.pattern_extractors.shape_pattern_extractor.read_key")
def test_load_key(read_key_mock, extractor):
    read_key_mock.return_value = [
        Thread("310", IDENT_1, PLACEHOLDERS[0], "Black", "f"),
        Thread("550", IDENT_2, PLACEHOLDERS[1], "Purple", "")]
    extractor.load_key()

    assert len(extractor.ident_map) == 2
    assert IDENT_1 in extractor.ident_map
    assert IDENT_2 in extractor.ident_map
    assert extractor.ident_map[IDENT_1] == PLACEHOLDERS[0]
    assert extractor.ident_map[IDENT_2] == PLACEHOLDERS[1]

    assert read_key_mock.mock_calls == [call("test.key")]
