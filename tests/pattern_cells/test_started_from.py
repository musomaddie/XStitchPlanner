import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.starting_corner import PatternGenerator, TOP_LEFT, BOTTOM_RIGHT, TOP_RIGHT, BOTTOM_LEFT


# TODO: move to overall test file and import?
def create_stitching_cell(value: str):
    return StitchingCell(PatternCell(value, value, [], ""))


@pytest.fixture
def pattern_unique():
    return [
        [create_stitching_cell(x) for x in ["a", "b", "c"]],
        [create_stitching_cell(x) for x in ["d", "e", "f"]],
        [create_stitching_cell(x) for x in ["g", "h", "i"]]
    ]


@pytest.fixture
def pattern_dups():
    return [
        [create_stitching_cell(x) for x in ["a", "a", "b", "b"]],
        [create_stitching_cell(x) for x in ["b", "b", "b", "a"]],
        [create_stitching_cell(x) for x in ["b", "a", "a", "b"]]
    ]


@pytest.fixture
def pattern_4_by_4():
    return [
        [create_stitching_cell(x) for x in ["a", "b", "b", "a"]],
        [create_stitching_cell(x) for x in ["b", "a", "b", "a"]],
        [create_stitching_cell(x) for x in ["b", "b", "b", "a"]],
        [create_stitching_cell(x) for x in ["a", "a", "a", "b"]]
    ]


@pytest.mark.parametrize(
    ("current_y", "within_bounds"),
    [(0, True), (1, True), (2, True), (-1, False), (3, False)])
def test_within_bounds(current_y, within_bounds, pattern_unique):
    gen = PatternGenerator(TOP_LEFT, pattern_unique)
    gen.current_y = current_y
    assert gen._within_bounds() == within_bounds


@pytest.mark.parametrize(
    ("starting_corner", "expected_colour"),
    [(TOP_LEFT, "a"), (BOTTOM_RIGHT, "b")]
)
def test_find_current_colour_no_stitches(starting_corner, expected_colour, pattern_dups):
    gen = PatternGenerator(starting_corner, pattern_dups)
    assert gen._find_current_colour().dmc_value == expected_colour


@pytest.mark.parametrize(
    ("starting_corner", "expected_colour", "stitched_values"),
    [(TOP_LEFT, "b", [True, True, False, False]), (TOP_RIGHT, "a", [False, False, True, True])]
)
def test_find_current_colour_one_stitched(starting_corner, expected_colour, stitched_values, pattern_dups):
    for cell, stitch_v in zip(pattern_dups[0], stitched_values):
        cell.stitched = stitch_v
    gen = PatternGenerator(starting_corner, pattern_dups)
    assert gen._find_current_colour().dmc_value == expected_colour


@pytest.mark.parametrize(
    ("starting_corner", "expected_symbol_list"),
    [(TOP_LEFT, ["a", "b", "c"]),
     (TOP_RIGHT, ["c", "b", "a"]),
     (BOTTOM_LEFT, ["g", "h", "i"]),
     (BOTTOM_RIGHT, ["i", "h", "g"])]
)
def test_row_generator(starting_corner, expected_symbol_list, pattern_unique):
    gen = PatternGenerator(starting_corner, pattern_unique)
    assert [x.dmc_value for x in [cell for cell in gen._row_generator()]] == expected_symbol_list


@pytest.mark.parametrize(
    ("starting_corner", "expected_y_1", "expected_y_2"),
    [(TOP_LEFT, 1, 2), (BOTTOM_LEFT, 1, 0)]
)
def test_update_y(starting_corner, expected_y_1, expected_y_2, pattern_unique):
    gen = PatternGenerator(starting_corner, pattern_unique)
    gen._update_y()
    assert gen.current_y == expected_y_1
    gen._update_y()
    assert gen.current_y == expected_y_2


@pytest.mark.parametrize(
    ("starting_corner", "expected_horiz_idx"),
    [(TOP_LEFT, 0), (TOP_RIGHT, 2)]
)
def test_horizontal_idx_start(starting_corner, expected_horiz_idx, pattern_unique):
    gen = PatternGenerator(starting_corner, pattern_unique)
    assert gen._horizontal_idx_start() == expected_horiz_idx


@pytest.mark.parametrize(
    ("starting_corner", "starting_y", "expected_symbols", "next_y", "next_x"),
    [(TOP_LEFT, 0, ["a", "b", "c"], 1, 0),
     (TOP_RIGHT, 1, ["f", "e", "d"], 2, 2),
     (BOTTOM_LEFT, 2, ["g", "h", "i"], 1, 0),
     (BOTTOM_RIGHT, 0, ["c", "b", "a"], -1, 2)]
)
def test_move_through_row(starting_corner, starting_y, expected_symbols, next_y, next_x, pattern_unique):
    gen = PatternGenerator(starting_corner, pattern_unique)
    gen.current_y = starting_y
    assert [x.dmc_value for x in [cell for cell in gen.move_through_row()]] == expected_symbols
    assert gen.current_y == next_y
    assert gen.current_x == next_x


# TODO: add test for stop iteration exception.

@pytest.mark.parametrize(
    ("starting_corner", "starting_y", "expected_symbol", "expected_number"),
    [(TOP_LEFT, 0, "a", 2),
     (TOP_RIGHT, 0, "b", 2),
     (BOTTOM_RIGHT, 1, "a", 1),
     (BOTTOM_LEFT, 1, "b", 3)]
)
def test_move_through_colour_in_rows(starting_corner, starting_y, expected_symbol, expected_number, pattern_dups):
    gen = PatternGenerator(starting_corner, pattern_dups)
    gen.current_y = starting_y
    result = [cell for cell in gen.move_through_colour_in_rows()]
    assert result[0].dmc_value == expected_symbol
    assert len(result) == expected_number


@pytest.mark.parametrize(
    ("starting_corner", "expected_symbol", "expected_number"),
    [(TOP_LEFT, "b", 3),
     (BOTTOM_RIGHT, "a", 1)]
)
def test_move_through_colour_in_rows_change_row(starting_corner, expected_symbol, expected_number, pattern_dups):
    gen = PatternGenerator(starting_corner, pattern_dups)
    # Call move through colour twice and mark each returned cell as stitched to force a row change
    for _ in range(2):
        for cell in gen.move_through_colour_in_rows():
            cell.stitched = True

    result = [cell for cell in gen.move_through_colour_in_rows()]
    assert result[0].dmc_value == expected_symbol
    assert len(result) == expected_number


@pytest.mark.parametrize(
    ("starting_corner", "expected_symbols"),
    [(TOP_LEFT, ["b", "a", "b", "a", "b", "b", "b", "a"]),
     (TOP_RIGHT, ["a", "b", "a", "b", "a", "b", "b", "b"]),
     (BOTTOM_LEFT, ["b", "b", "b", "a", "b", "a", "b", "a"]),
     (BOTTOM_RIGHT, ["a", "b", "b", "b", "a", "b", "a", "b"])]
)
def test_iterate_over_limited_rows(starting_corner, expected_symbols, pattern_4_by_4):
    gen = PatternGenerator(starting_corner, pattern_4_by_4)
    result = [cell.dmc_value for cell in PatternGenerator.iterate_over_limited_rows(gen, 2)]
    assert result == expected_symbols


@pytest.mark.parametrize(
    ("starting_corner", "expected_symbols"),
    [(TOP_LEFT, ["b", "a", "b", "a", "b", "b", "b", "a", "a", "a", "a", "b"]),
     (TOP_RIGHT, ["a", "b", "a", "b", "a", "b", "b", "b", "b", "a", "a", "a"]),
     (BOTTOM_LEFT, ["b", "b", "b", "a", "b", "a", "b", "a", "a", "b", "b", "a"]),
     (BOTTOM_RIGHT, ["a", "b", "b", "b", "a", "b", "a", "b", "a", "b", "b", "a"])]
)
def test_iterate_over_limited_rows_to_edges(starting_corner, expected_symbols, pattern_4_by_4):
    gen = PatternGenerator(starting_corner, pattern_4_by_4)
    result = [cell.dmc_value for cell in PatternGenerator.iterate_over_limited_rows(gen, 3)]
    assert result == expected_symbols

# TODO: test edges of pattern.
