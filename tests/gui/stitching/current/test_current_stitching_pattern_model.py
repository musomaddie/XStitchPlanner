import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from gui.stitching.current.current_stitching_pattern_model import CurrentStitchingPatternModel
from pattern_cells.pattern_cell import PatternCell
from pattern_cells.stitching_cell import StitchingCell
from stitchers.OLD_full_parking_stitcher import FullParkingStitcher
from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT


class Idx:
    def __init__(self, row_i, col_i):
        self._row = row_i
        self._col = col_i

    def row(self):
        return self._row

    def column(self):
        return self._col


TESTING_DATA_3_2 = [
    [StitchingCell(PatternCell("a", "310", (0, 0), "000000")),
     StitchingCell(PatternCell("a", "310", (0, 1), "000000")),
     StitchingCell(PatternCell("b", "666", (0, 2), "FF0000"))],
    [StitchingCell(PatternCell("c", "550", (1, 0), "FF00FF")),
     StitchingCell(PatternCell("b", "666", (1, 1), "FF0000")),
     StitchingCell(PatternCell("d", "336", (1, 2), "00FF00"))]]


@pytest.fixture
def model(starting_corner):
    stitcher = FullParkingStitcher(TESTING_DATA_3_2, starting_corner)
    return CurrentStitchingPatternModel(stitcher)


@pytest.mark.parametrize(
    ("r", "c", "starting_corner"),
    [(0, 0, TOP_LEFT),
     (0, 2, TOP_RIGHT),
     (1, 0, BOTTOM_LEFT),
     (1, 2, BOTTOM_RIGHT)])
def test_data(r, c, starting_corner, model):
    color_result = model.data(Idx(r, c), Qt.ItemDataRole.BackgroundRole)
    assert color_result.rgb() == QColor(
        f"#{TESTING_DATA_3_2[r][c].hex_colour}").rgb()
