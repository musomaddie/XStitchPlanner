import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.starting_corner import PatternGenerator, TOP_LEFT, BOTTOM_LEFT, TOP_RIGHT, BOTTOM_RIGHT


# TODO: move to overall test file and import?
def create_stitching_cell(value: str):
    return StitchingCell(PatternCell(value, value, [], ""))


@pytest.fixture
def pattern():
    return [
        [create_stitching_cell("a"), create_stitching_cell("b"), create_stitching_cell("c")],
        [create_stitching_cell("d"), create_stitching_cell("e"), create_stitching_cell("f")],
        [create_stitching_cell("g"), create_stitching_cell("h"), create_stitching_cell("i")]
    ]


def test_pattern_generator_row_top_left(pattern):
    gen = PatternGenerator(TOP_LEFT, pattern)
    result = [cell for cell in gen.move_through_row()]
    assert len(result) == 3
    assert result[0] == pattern[0][0]
    assert result[1] == pattern[0][1]
    assert result[2] == pattern[0][2]

    assert gen.current_y == 1
    assert gen.current_x == 0


def test_pattern_generator_row_top_left_second_row(pattern):
    gen = PatternGenerator(TOP_LEFT, pattern)
    result = [cell for cell in gen.move_through_row()]
    # Repeating the call to iterate through the second row.
    result = [cell for cell in gen.move_through_row()]
    assert len(result) == 3
    assert result[0] == pattern[1][0]
    assert result[1] == pattern[1][1]
    assert result[2] == pattern[1][2]
    assert gen.current_y == 2
    assert gen.current_x == 0


def test_pattern_generator_row_bottom_left(pattern):
    gen = PatternGenerator(BOTTOM_LEFT, pattern)
    result = [cell for cell in gen.move_through_row()]
    assert len(result) == 3
    assert result[0] == pattern[2][0]
    assert result[1] == pattern[2][1]
    assert result[2] == pattern[2][2]

    assert gen.current_y == 1
    assert gen.current_x == 0


def test_pattern_generator_row_top_right(pattern):
    gen = PatternGenerator(TOP_RIGHT, pattern)
    result = [cell for cell in gen.move_through_row()]
    assert len(result) == 3
    assert result[0] == pattern[0][2]
    assert result[1] == pattern[0][1]
    assert result[2] == pattern[0][0]

    assert gen.current_y == 1
    assert gen.current_x == 2


def test_pattern_generator_row_bottom_right(pattern):
    gen = PatternGenerator(BOTTOM_RIGHT, pattern)
    result = [cell for cell in gen.move_through_row()]
    assert len(result) == 3
    assert result[0] == pattern[2][2]
    assert result[1] == pattern[2][1]
    assert result[2] == pattern[2][0]

    assert gen.current_y == 1
    assert gen.current_x == 2
