from copy import copy, deepcopy

import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitched_cell import StartedFrom, StitchedCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.OLD_full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import (
    BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT, VerticalDirection)

FILE_LOC = "stitchers.full_parking"

SC_A = StitchingCell(PatternCell("a", "310", [], ""))
SC_B = StitchingCell(PatternCell("b", "550", [], ""))
SC_C = StitchingCell(PatternCell("c", "666", [], ""))
PATTERN = [[copy(SC_A), copy(SC_B), copy(SC_B), copy(SC_A), copy(SC_C)],
           [copy(SC_B), copy(SC_A), copy(SC_B), copy(SC_A), copy(SC_C)],
           [copy(SC_C), copy(SC_C), copy(SC_C), copy(SC_B), copy(SC_A)],
           [copy(SC_B), copy(SC_B), copy(SC_A), copy(SC_A), copy(SC_A)],
           [copy(SC_A), copy(SC_A), copy(SC_C), copy(SC_C), copy(SC_C)]]

""" Pattern is: 
a b b a c
b a b a c
b b a a a
a a c c c
"""


@pytest.fixture
def parking(starting_corner):
    return FullParkingStitcher(PATTERN, starting_corner, config={"skippable-columns": 1})


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT))
def test_init(parking, starting_corner):
    assert parking.num_skippable_rows == 1
    if starting_corner.vertical == VerticalDirection.TOP:
        assert parking.next_row_to_stitch == PATTERN[0]
    else:
        assert parking.next_row_to_stitch == PATTERN[len(PATTERN) - 1]

    # Test no config
    parking = FullParkingStitcher(PATTERN, starting_corner)
    assert parking.num_skippable_rows == 0


""" get_next_stitchable_row """


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_get_next_stitchable_row_partway(starting_corner):
    parking = FullParkingStitcher(PATTERN, starting_corner)
    if starting_corner == TOP_LEFT:
        parking.stitched_pattern = [PATTERN[0], PATTERN[1]]
    if starting_corner == BOTTOM_LEFT:
        parking.stitched_pattern = [PATTERN[len(PATTERN) - 1], PATTERN[len(PATTERN) - 2]]

    result = parking.get_next_stitchable_row()
    assert result == parking.original_pattern[2]


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_get_next_stitchable_row_finished(starting_corner):
    parking = FullParkingStitcher(PATTERN, starting_corner)
    parking.stitched_pattern = parking.original_pattern

    result = parking.get_next_stitchable_row()
    assert result is None


""" stitch_this_colour """


def test_stitch_this_colour_one():
    row = [StitchingCell(PatternCell("a", "310", [], ""))]
    cc_cell = StitchingCell(PatternCell("a", "310", [], ""))

    result, num_stitched = FullParkingStitcher.stitch_this_colour(cc_cell, row, 0)
    assert len(result) == 2
    assert num_stitched == 2
    assert result[0].started_from == StartedFrom.STARTED_NEW
    assert result[1].started_from == StartedFrom.CONTINUED_FROM_ROW
    assert cc_cell.stitched
    assert row[0].stitched


def test_stitch_this_colour_empty_row():
    row = []
    cc_cell = StitchingCell(PatternCell("a", "310", [], ""))
    result, num_stitched = FullParkingStitcher.stitch_this_colour(cc_cell, row, 0)
    assert len(result) == 1
    assert num_stitched == 1
    assert result[0].started_from == StartedFrom.STARTED_NEW
    assert cc_cell.stitched


def test_stitch_this_colour_no_matches():
    row = [StitchingCell(PatternCell("b", "666", [], "")),
           StitchingCell(PatternCell("b", "666", [], "")),
           StitchingCell(PatternCell("c", "550", [], ""))]
    cc_cell = StitchingCell(PatternCell("a", "310", [], ""))
    result, num_stitched = FullParkingStitcher.stitch_this_colour(cc_cell, row, 0)
    assert len(result) == 1
    assert num_stitched == 1
    assert result[0].started_from == StartedFrom.STARTED_NEW
    assert cc_cell.stitched
    for r in row:
        assert not r.stitched


def test_stitch_this_colour_multiple_matches():
    row = [StitchingCell(PatternCell("a", "310", [], "")),
           StitchingCell(PatternCell("b", "666", [], "")),
           StitchingCell(PatternCell("a", "310", [], ""))]
    cc_cell = StitchingCell(PatternCell("a", "310", [], ""))
    result, num_stitched = FullParkingStitcher.stitch_this_colour(cc_cell, row, 0)
    assert len(result) == 3
    assert num_stitched == 3
    assert result[0].started_from == StartedFrom.STARTED_NEW
    assert result[1].started_from == StartedFrom.CONTINUED_FROM_ROW
    assert result[2].started_from == StartedFrom.CONTINUED_FROM_ROW
    assert cc_cell.stitched
    assert row[0].stitched
    assert not row[1].stitched
    assert row[2].stitched


def test_stitch_this_colour_already_stitched():
    row = []
    cc_cell = StitchingCell(PatternCell("a", "310", [], ""))
    cc_cell.stitched = True
    result, num_stitched = FullParkingStitcher.stitch_this_colour(cc_cell, row, 0)
    assert len(result) == 0
    assert num_stitched == 0


""" park_colour """


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT))
def test_park_colour_in_one_possible_row(starting_corner, parking):
    # Otherwise future calls will have changes from original.
    this_row = [deepcopy(parking.original_pattern[0])]
    result = parking.park_colour(
        StitchedCell("a", "550", [], "", StartedFrom.STARTED_NEW, 1), this_row)
    assert result
    parked_idx = 0 if starting_corner == TOP_LEFT else 3
    for index, cell in enumerate(this_row[0]):
        if index == parked_idx:
            assert cell.parked
        else:
            assert not cell.parked


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT))
def test_park_colour_no_position(parking):
    this_row = [deepcopy(parking.original_pattern[3])]
    result = parking.park_colour(
        StitchedCell("c", "200", [], "", StartedFrom.STARTED_NEW, 1), this_row)
    assert not result
    for cell in this_row[0]:
        assert not cell.parked


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT))
def test_park_colour_multiple_rows(starting_corner, parking):
    my_rows = [deepcopy(parking.original_pattern[3]), deepcopy(parking.original_pattern[4])]
    result = parking.park_colour(
        StitchedCell("c", "200", [], "", StartedFrom.STARTED_NEW, 1), my_rows)
    assert result
    for cell in my_rows[0]:
        assert not cell.parked
    parked_idx = 2 if starting_corner == TOP_LEFT else 4
    for index, cell in enumerate(my_rows[1]):
        if index == parked_idx:
            assert cell.parked
        else:
            assert not cell.parked


""" Find rows to park """


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_find_rows_to_park_one_from_first_row(starting_corner, parking):
    actual_rows = parking.find_rows_to_park()
    expected_rows = (["babac"] if starting_corner == TOP_LEFT else ["bbaaa"])

    for actual_row, expected_row in zip(actual_rows, expected_rows):
        for actual, expected in zip(actual_row, expected_row):
            assert actual.display_symbol == expected


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_find_rows_to_park_multiple_rows(starting_corner, parking):
    parking.num_skippable_rows = 2
    actual_rows = parking.find_rows_to_park()
    expected_rows_symbols = (
        ["babac", "cccba"] if starting_corner == TOP_LEFT else ["bbaaa", "cccba"])

    for actual_row, expected_row in zip(actual_rows, expected_rows_symbols):
        for actual, expected in zip(actual_row, expected_row):
            assert actual.display_symbol == expected


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_find_rows_to_park_rows_left_matches_skippable_cols(starting_corner, parking):
    parking.stitched_pattern = (
        [parking.original_pattern[0], parking.original_pattern[1],
         parking.original_pattern[2], parking.original_pattern[3]]
        if starting_corner == TOP_LEFT
        else [parking.original_pattern[4], parking.original_pattern[3],
              parking.original_pattern[2], parking.original_pattern[1]])

    actual_rows = parking.find_rows_to_park()
    expected_rows = ["aaccc"] if starting_corner == TOP_LEFT else ["abbac"]

    for actual_row, expected_row in zip(actual_rows, expected_rows):
        for actual, expected in zip(actual_row, expected_row):
            assert actual.display_symbol == expected


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, BOTTOM_LEFT))
def test_find_rows_to_park_no_rows_left(starting_corner, parking):
    parking.stitched_pattern = (
        [parking.original_pattern[0], parking.original_pattern[1],
         parking.original_pattern[2], parking.original_pattern[3], parking.original_pattern[4]]
        if starting_corner == TOP_LEFT
        else [parking.original_pattern[4], parking.original_pattern[3],
              parking.original_pattern[2], parking.original_pattern[1],
              parking.original_pattern[0]])
    actual_rows = parking.find_rows_to_park()
    assert len(actual_rows) == 0


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT))
def test_find_rows_to_park_less_rows_than_skippable(starting_corner, parking):
    parking.num_skippable_rows = 2
    parking.stitched_pattern = (
        [parking.original_pattern[0], parking.original_pattern[1],
         parking.original_pattern[2], parking.original_pattern[3]]
        if starting_corner == TOP_LEFT
        else [parking.original_pattern[4], parking.original_pattern[3],
              parking.original_pattern[2], parking.original_pattern[1]])
    actual_rows = parking.find_rows_to_park()
    expected_rows = ["aaccc"] if starting_corner == TOP_LEFT else ["abbac"]

    for actual_row, expected_row in zip(actual_rows, expected_rows):
        for actual, expected in zip(actual_row, expected_row):
            assert actual.display_symbol == expected


""" Stitch next row """


def make_result_checker_helper(result):
    return [[(g.display_symbol, g.nth_stitched)
             for g in group] for group in result]


@pytest.mark.parametrize("starting_corner", [TOP_RIGHT, TOP_LEFT, BOTTOM_RIGHT, BOTTOM_LEFT])
def test_stitch_next_row_one_row(starting_corner, parking):
    parking.original_pattern = deepcopy(parking.original_pattern)
    result = parking.stitch_next_row()
    checker = make_result_checker_helper(result)

    assert parking.original_pattern == PATTERN
    if starting_corner == TOP_RIGHT:
        assert len(checker) == 3
        assert len(checker[0]) == 1
        assert checker[0] == [("c", 1)]
        assert len(checker[1]) == 2
        assert checker[1] == [("a", 2), ("a", 3)]
        assert len(checker[2]) == 2
        assert checker[2] == [("b", 4), ("b", 5)]

        assert not parking.original_pattern[1][0].parked
        assert not parking.original_pattern[1][1].parked
        assert parking.original_pattern[1][2].parked
        assert parking.original_pattern[1][3].parked
        assert parking.original_pattern[1][4].parked


    elif starting_corner == TOP_LEFT:
        assert len(checker) == 3
        assert len(checker[0]) == 2
        assert checker[0] == [("a", 1), ("a", 2)]
        assert len(checker[1]) == 2
        assert checker[1] == [("b", 3), ("b", 4)]
        assert len(checker[2]) == 1
        assert checker[2] == [("c", 5)]

        assert parking.original_pattern[1][0].parked
        assert parking.original_pattern[1][1].parked
        assert not parking.original_pattern[1][2].parked
        assert not parking.original_pattern[1][3].parked
        assert parking.original_pattern[1][4].parked

    elif starting_corner == BOTTOM_RIGHT:
        assert len(checker) == 2
        assert len(checker[0]) == 3
        assert checker[0] == [("c", 1), ("c", 2), ("c", 3)]
        assert len(checker[1]) == 2
        assert checker[1] == [("a", 4), ("a", 5)]

        assert not parking.original_pattern[3][0].parked
        assert not parking.original_pattern[3][1].parked
        assert not parking.original_pattern[3][2].parked
        assert not parking.original_pattern[3][3].parked
        assert parking.original_pattern[3][4].parked

    elif starting_corner == BOTTOM_LEFT:
        assert len(checker) == 2
        assert len(checker[0]) == 2
        assert checker[0] == [("a", 1), ("a", 2)]
        assert len(checker[1]) == 3
        assert checker[1] == [("c", 3), ("c", 4), ("c", 5)]

        assert not parking.original_pattern[3][0].parked
        assert not parking.original_pattern[3][1].parked
        assert parking.original_pattern[3][2].parked
        assert not parking.original_pattern[3][3].parked
        assert not parking.original_pattern[3][4].parked


"""Stitch entire pattern """


def helper_assert_stitched_cell(cell, sym, started, nth):
    assert cell.display_symbol == sym
    assert cell.started_from == started
    assert cell.nth_stitched == nth


def test_stitch_entire_pattern_top_left():
    parking = FullParkingStitcher(PATTERN, TOP_LEFT, config={"skippable-columns": 1})
    stitched_rows = parking.stitch_entire_pattern()
    row0 = stitched_rows[0]
    helper_assert_stitched_cell(row0[0][0], "a", StartedFrom.STARTED_NEW, 1)
    helper_assert_stitched_cell(row0[0][1], "a", StartedFrom.CONTINUED_FROM_ROW, 2)
    helper_assert_stitched_cell(row0[1][0], "b", StartedFrom.STARTED_NEW, 3)
    helper_assert_stitched_cell(row0[1][1], "b", StartedFrom.CONTINUED_FROM_ROW, 4)
    helper_assert_stitched_cell(row0[2][0], "c", StartedFrom.STARTED_NEW, 5)

    row1 = stitched_rows[1]
    helper_assert_stitched_cell(row1[0][0], "b", StartedFrom.FROM_PARKED_THREAD, 1)
    helper_assert_stitched_cell(row1[0][1], "b", StartedFrom.CONTINUED_FROM_ROW, 2)
    helper_assert_stitched_cell(row1[1][0], "a", StartedFrom.FROM_PARKED_THREAD, 3)
    helper_assert_stitched_cell(row1[1][1], "a", StartedFrom.CONTINUED_FROM_ROW, 4)
    helper_assert_stitched_cell(row1[2][0], "c", StartedFrom.FROM_PARKED_THREAD, 5)

    row2 = stitched_rows[2]
    helper_assert_stitched_cell(row2[0][0], "c", StartedFrom.FROM_PARKED_THREAD, 1)
    helper_assert_stitched_cell(row2[0][1], "c", StartedFrom.CONTINUED_FROM_ROW, 2)
    helper_assert_stitched_cell(row2[0][2], "c", StartedFrom.CONTINUED_FROM_ROW, 3)
    helper_assert_stitched_cell(row2[1][0], "b", StartedFrom.FROM_PARKED_THREAD, 4)
