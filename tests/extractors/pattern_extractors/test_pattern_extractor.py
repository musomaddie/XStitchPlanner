from extractors.pattern_extractors.font_pattern_extractor import FontPatternExtractor
from extractors.extractor import PatternFormatError
from unittest.mock import MagicMock

import pytest
import resources.strings as s

EXAMPLE_ROWS_BASIC = [
    ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
    ["20", "21", "22", "23", "24", "25", "26", "27", "28", "29"],
    ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"],
    ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49"],
    ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
]

def fake_rows_fn(page_idx, withkey=False, verbose=False):
    return EXAMPLE_ROWS_BASIC

@pytest.fixture
def extractor():
    # Using a FontPatternExtractor as the PatternExtractor is an abstract class
    extractor = FontPatternExtractor(MagicMock(), "test")
    return extractor

def test_init(extractor):
    assert len(extractor.pattern) == 0


@pytest.mark.parametrize(
    "cur_x,cur_y,expected_page_height,height,width,overlap," +
    "result_pattern,result_x,result_y,result_page_height",
    # Simple example
    [(0, 0, 5, 5, 10, 0, EXAMPLE_ROWS_BASIC, 0, 5, 5),
     # Different starting x and y
     (10, 5, 5, 10, 20, 0, EXAMPLE_ROWS_BASIC, 0, 10, 5),
     # x not wrapping
     (0, 0, 5, 5, 11, 0, EXAMPLE_ROWS_BASIC, 10, 0, 5),
     # With some overlap
     (10, 0, 5, 5, 18, 2,
      [row[2:] for row in EXAMPLE_ROWS_BASIC], 0, 5, 5)]
)
def test_ExtractPatternFromThisPage(
        extractor, cur_x, cur_y, expected_page_height, height, width, overlap,
        result_pattern, result_x, result_y, result_page_height):
    actual_rx, actual_ry, actual_rph = extractor._extract_from_this_page(
        0, EXAMPLE_ROWS_BASIC, cur_x, cur_y, expected_page_height, height,
        width, overlap, False)

    assert extractor.pattern == result_pattern
    assert actual_rx == result_x
    assert actual_ry == result_y
    assert actual_rph == result_page_height

@pytest.mark.parametrize(
    "cur_x,cur_y,expected_ph,height,width,rows,expected_error_message",
    [(0, 0, 5, 5, 10, EXAMPLE_ROWS_BASIC + ["1", "2", "3"],
      s.pattern_uneven_width(1)),
     (2, 2, 7, 5, 10, EXAMPLE_ROWS_BASIC, s.pattern_uneven_height(1, 5, 7, 3)),
     (2, 2, 5, 7, 10, EXAMPLE_ROWS_BASIC,
      s.pattern_size_too_big(1, 10, 5, 12, 7, 10, 7))]
)
def test_ExtractPatternFromThisPage_Invalid(
        extractor, cur_x, cur_y, expected_ph, height, width, rows,
        expected_error_message):

    with pytest.raises(PatternFormatError) as e:
        extractor._extract_from_this_page(
            0, rows, cur_x, cur_y, expected_ph, height, width, 0, False)
    assert str(e.value) == expected_error_message

@pytest.mark.parametrize(
    "width,height,start_page,end_page,expected_pattern",
    [(10, 5, 0, 0, EXAMPLE_ROWS_BASIC),
     (10, 10, 0, 1, EXAMPLE_ROWS_BASIC + EXAMPLE_ROWS_BASIC)]
)
def test_ExtractPatternGivenPages_Valid(
        extractor, width, height, start_page, end_page, expected_pattern):
    # TODO: I need to make sure that I test that patterns spread over multiple
    # pages are combined in the expected way.
    extractor.extract_pattern_given_pages(
        fake_rows_fn, width, height, start_page, end_page)
    assert extractor.pattern == expected_pattern

@pytest.mark.parametrize(
    "width,height,expected_error_message",
    [(12, 5, s.pattern_wrong_size("wide", 10, 12)),
     (10, 7, s.pattern_wrong_size("high", 5, 7))]
)
def test_ExtractPatternGivenPages_Invalid(
        extractor, width, height, expected_error_message):
    extractor.pdf.pages = ["example"]
    with pytest.raises(PatternFormatError) as e:
        extractor.extract_pattern_given_pages(
            fake_rows_fn, width, height)
    assert str(e.value) == expected_error_message

def test_SavePattern(extractor):
    pattern_filename = "tests/resources/test.pat"
    extractor.pattern = [["@", "!", "@"],
                         ["!", "@", "@"],
                         ["@", "!", "@"]]
    extractor.pattern_filename = pattern_filename
    extractor.save_pattern()

    resulting_lines = ["@!@\n", "!@@\n", "@!@\n"]
    with open(pattern_filename, "r") as f:
        for actual, expected in zip(f.readlines(), resulting_lines):
            assert actual == expected

def test_SavePattern_EmptyKey(extractor):
    with pytest.raises(ValueError) as e:
        extractor.save_pattern()
    assert str(e.value) == s.empty_on_save("pattern")
