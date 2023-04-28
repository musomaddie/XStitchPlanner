from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from floss_thread import Thread
from gui.pattern_model import PatternModel
from pattern_cells.pattern_cell import PatternCell

TESTING_DATA_3_2 = [
    [PatternCell("a", "310", (0, 0), "000000"),
     PatternCell("a", "310", (0, 1), "000000"),
     PatternCell("b", "666", (0, 2), "FF0000")],
    [PatternCell("b", "666", (1, 0), "FF0000"),
     PatternCell("b", "666", (1, 1), "FF0000"),
     PatternCell("a", "310", (1, 2), "000000")]]
TESTING_DATA_3_3 = [['a', 'a', 'b'], ['b', 'b', 'c'], ['c', 'c', 'a']]
TESTING_DATA_3_3_STR = "aab\nbbc\ncca\n"
TESTING_DATA_3_THREAD_DICT = [Thread("310", "a", "a", "Black", "000000"),
                              Thread("550", "b", "b", "Purple", "800080"),
                              Thread("666", "c", "c", "Red", "ff0000")]


class Idx:
    def __init__(self, row_i, col_i):
        self._row = row_i
        self._col = col_i

    def row(self):
        return self._row

    def column(self):
        return self._col


@pytest.fixture
def model():
    return PatternModel(TESTING_DATA_3_2)


def test_init(model):
    assert model._data == TESTING_DATA_3_2
    assert model.display is None
    assert not model.show_colours


def test_rowCount(model):
    assert model.rowCount(None) == 2


def test_columnCount(model):
    assert model.columnCount(None) == 3


def test_add_display(model):
    display_mock = MagicMock()
    model.add_display(display_mock)
    assert model.display == display_mock


@pytest.mark.parametrize(("r", "col"), [(0, 0), (1, 0)])
def test_data(r, col, model):
    model.show_colours = True
    color_result = model.data(Idx(r, col), Qt.ItemDataRole.BackgroundRole)
    assert color_result.rgb() == QColor(
        f"#{TESTING_DATA_3_2[r][col].hex_colour}").rgb()

    string_result = model.data(Idx(r, col), Qt.ItemDataRole.DisplayRole)
    assert string_result == TESTING_DATA_3_2[r][col].display_symbol


def test_data_no_colour(model):
    color_result = model.data(Idx(0, 0), Qt.ItemDataRole.BackgroundRole)
    assert color_result is None
