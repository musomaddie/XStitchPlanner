from copy import copy

import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT

SC_A = StitchingCell(PatternCell("a", "310", [], ""))
SC_B = StitchingCell(PatternCell("b", "550", [], ""))
SC_C = StitchingCell(PatternCell("c", "666", [], ""))
PATTERN = [[copy(SC_A), copy(SC_B), copy(SC_B), copy(SC_A), copy(SC_C)],
           [copy(SC_B), copy(SC_A), copy(SC_B), copy(SC_A), copy(SC_C)],
           [copy(SC_C), copy(SC_C), copy(SC_C), copy(SC_B), copy(SC_A)],
           [copy(SC_B), copy(SC_B), copy(SC_A), copy(SC_A), copy(SC_A)],
           [copy(SC_A), copy(SC_A), copy(SC_C), copy(SC_C), copy(SC_C)]]


@pytest.fixture
def stitcher(starting_corner):
    return FullParkingStitcher(copy(PATTERN), starting_corner)


@pytest.mark.parametrize("starting_corner", (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT))
def test_init(stitcher, starting_corner):
    assert stitcher.height == 5
    assert stitcher.width == 5
    assert stitcher.stitched_pattern == []
    assert stitcher.starting_corner == starting_corner

    # Due to test set up the values propogate down
    if starting_corner == TOP_LEFT:
        assert stitcher.original_pattern[0][0].to_start_with
        assert not stitcher.original_pattern[0][4].to_start_with
        assert not stitcher.original_pattern[4][0].to_start_with
        assert not stitcher.original_pattern[4][4].to_start_with
    if starting_corner == TOP_RIGHT:
        assert stitcher.original_pattern[0][4].to_start_with
        assert not stitcher.original_pattern[4][0].to_start_with
        assert not stitcher.original_pattern[4][4].to_start_with
    if starting_corner == BOTTOM_LEFT:
        assert stitcher.original_pattern[4][0].to_start_with
        assert not stitcher.original_pattern[4][4].to_start_with
    if starting_corner == BOTTOM_RIGHT:
        assert stitcher.original_pattern[4][4].to_start_with
