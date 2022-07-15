import pytest

from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell


@pytest.fixture
def cell():
    return StitchingCell(PatternCell("a", "310", [], ""))


def test_init(cell):
    assert cell.display_symbol == "a"
    assert cell.dmc_value == "310"
    assert not cell.stitched
    assert not cell.parked
    assert not cell.to_start_with


@pytest.mark.parametrize(
    ("other_cell", "expected_result"),
    [(StitchingCell(PatternCell("a", "310", [], "")), True),
     (StitchingCell(PatternCell("a", "550", [], "")), True),
     (StitchingCell(PatternCell("b", "310", [], "")), False),
     (StitchingCell(PatternCell("b", "550", [], "")), False)]
)
def test_eq(cell, other_cell, expected_result):
    assert cell.__eq__(other_cell) == expected_result
    assert other_cell.__eq__(cell) == expected_result


def test_repr(cell):
    assert cell.__repr__() == "a (s)"
