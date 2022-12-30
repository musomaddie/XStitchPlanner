import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.started_from import StartedFrom
from pattern_cells.stitching_cell import StitchingCell
from stitchers.full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import TOP_LEFT


def create_stitching_cell(value: str):
    return StitchingCell(PatternCell(value, value, [], ""))


@pytest.fixture
def pattern():
    return [
        [create_stitching_cell(x) for x in ["a", "b", "b", "a"]],
        [create_stitching_cell(x) for x in ["b", "a", "b", "a"]],
        [create_stitching_cell(x) for x in ["b", "b", "b", "a"]],
        [create_stitching_cell(x) for x in ["a", "a", "a", "b"]]
    ]


def test_full_stitching_top_left(pattern):
    stitcher = FullParkingStitcher(pattern, TOP_LEFT)
    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[0]] == [True, False, False, True]
    assert [cell.started_from for cell in pattern[0]] == [
        StartedFrom.STARTED_NEW, StartedFrom.NOT_STARTED, StartedFrom.NOT_STARTED, StartedFrom.CONTINUED_FROM_ROW]
    assert pattern[1][1].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[0]] == [True, True, True, True]
    assert [cell.started_from for cell in pattern[0]] == [
        StartedFrom.STARTED_NEW, StartedFrom.STARTED_NEW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.CONTINUED_FROM_ROW]
    assert pattern[1][0].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[1]] == [True, False, True, False]
    assert [cell.started_from for cell in pattern[1]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.NOT_STARTED,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.NOT_STARTED]
    assert pattern[2][0].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[1]] == [True, True, True, True]
    assert [cell.started_from for cell in pattern[1]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.FROM_PARKED_THREAD,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.CONTINUED_FROM_ROW]
    assert pattern[2][3].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[2]] == [True, True, True, False]
    assert [cell.started_from for cell in pattern[2]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.CONTINUED_FROM_ROW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.NOT_STARTED]
    assert pattern[3][3].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in pattern[2]] == [True, True, True, True]
    assert [cell.started_from for cell in pattern[2]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.CONTINUED_FROM_ROW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.FROM_PARKED_THREAD
    ]
