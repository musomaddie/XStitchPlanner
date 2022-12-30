import pytest

from pattern_cells.started_from import StartedFrom
from stitchers.full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import TOP_LEFT
from tests.test_utils import create_cell_for_stitcher


@pytest.fixture
def pattern():
    return [
        [create_cell_for_stitcher(x) for x in ["a", "b", "b", "a"]],
        [create_cell_for_stitcher(x) for x in ["b", "a", "b", "a"]],
        [create_cell_for_stitcher(x) for x in ["b", "b", "b", "a"]],
        [create_cell_for_stitcher(x) for x in ["a", "a", "a", "b"]]
    ]


def test_full_stitching_top_left(pattern):
    stitcher = FullParkingStitcher(pattern, TOP_LEFT)
    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[0]] == [True, False, False, True]
    assert [cell.started_from for cell in stitcher.stitched_pattern[0]] == [
        StartedFrom.STARTED_NEW, StartedFrom.NOT_STARTED, StartedFrom.NOT_STARTED, StartedFrom.CONTINUED_FROM_ROW]
    assert stitcher.stitched_pattern[1][1].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[0]] == [True, True, True, True]
    assert [cell.started_from for cell in stitcher.stitched_pattern[0]] == [
        StartedFrom.STARTED_NEW, StartedFrom.STARTED_NEW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.CONTINUED_FROM_ROW]
    assert stitcher.stitched_pattern[1][0].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[1]] == [True, False, True, False]
    assert [cell.started_from for cell in stitcher.stitched_pattern[1]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.NOT_STARTED,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.NOT_STARTED]
    assert stitcher.stitched_pattern[2][0].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[1]] == [True, True, True, True]
    assert [cell.started_from for cell in stitcher.stitched_pattern[1]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.FROM_PARKED_THREAD,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.CONTINUED_FROM_ROW]
    assert stitcher.stitched_pattern[2][3].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[2]] == [True, True, True, False]
    assert [cell.started_from for cell in stitcher.stitched_pattern[2]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.CONTINUED_FROM_ROW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.NOT_STARTED]
    assert stitcher.stitched_pattern[3][3].parked

    stitcher.stitch_next_colour()
    assert [cell.stitched for cell in stitcher.stitched_pattern[2]] == [True, True, True, True]
    assert [cell.started_from for cell in stitcher.stitched_pattern[2]] == [
        StartedFrom.FROM_PARKED_THREAD, StartedFrom.CONTINUED_FROM_ROW,
        StartedFrom.CONTINUED_FROM_ROW, StartedFrom.FROM_PARKED_THREAD
    ]
