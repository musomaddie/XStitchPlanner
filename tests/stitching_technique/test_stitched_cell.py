import pytest

from pattern_cells.stitched_cell import StartedFrom, StitchedCell
from pattern_cells.stitching_cell import StitchingCell


@pytest.fixture
def cell():
    return StitchingCell("a", "310")


def test_create_from_stitching_cell(cell):
    result = StitchedCell.create_from_stitching_cell(cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.STARTED_NEW


def test_create_from_stitching_cell_parked(cell):
    cell.parked = True
    result = StitchedCell.create_from_stitching_cell(cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.FROM_PARKED_THREAD


def test_create_when_found_in_row(cell):
    result = StitchedCell.create_when_found_in_row(cell, 0)
    assert result.display_symbol == "a"
    assert result.started_from == StartedFrom.CONTINUED_FROM_ROW
