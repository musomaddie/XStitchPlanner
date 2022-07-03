import pytest

from pattern_cells.stitched_cell import StartedFrom, StitchedCell
from pattern_cells.stitching_cell import StitchingCell


@pytest.fixture
def stitching_cell():
    return StitchingCell("a", "310")


def test_create_from_stitching_cell(stitching_cell):
    result = StitchedCell.create_from_stitching_cell(stitching_cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.STARTED_NEW


def test_create_from_stitching_cell_parked(stitching_cell):
    stitching_cell.parked = True
    result = StitchedCell.create_from_stitching_cell(stitching_cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.FROM_PARKED_THREAD


def test_create_when_found_in_row(stitching_cell):
    result = StitchedCell.create_when_found_in_row(stitching_cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.CONTINUED_FROM_ROW


def test_repr():
    cell = StitchedCell("a", StartedFrom.STARTED_NEW, 1)
    assert cell.__repr__() == "a [1] (sed)"
