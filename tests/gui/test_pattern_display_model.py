from unittest import mock
from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from floss_thread import Thread
from gui.pattern_display_model import PatternDisplayModel
from pattern_cell import PatternCell

FILE_LOC = "gui.pattern_display_model"

TESTING_DATA_3_2 = [
    [PatternCell("a", "310", [0, 0], "000000"),
     PatternCell("a", "310", [0, 1], "000000"),
     PatternCell("b", "666", [0, 2], "FF0000")],
    [PatternCell("b", "666", [1, 0], "FF0000"),
     PatternCell("b", "666", [1, 1], "FF0000"),
     PatternCell("a", "310", [1, 2], "000000")]]
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


@pytest.fixture()
def model():
    return PatternDisplayModel(TESTING_DATA_3_2)


# Model tests!
def test_load_pattern_from_file():
    read_key_mock = MagicMock(return_value=TESTING_DATA_3_THREAD_DICT)
    open_mock = mock.mock_open(read_data=TESTING_DATA_3_3_STR)
    with mock.patch(f"{FILE_LOC}.open", open_mock):
        with mock.patch(f"{FILE_LOC}.read_key", read_key_mock):
            result = PatternDisplayModel.load_from_pattern_file("TESTING")
    assert type(result) == PatternDisplayModel
    assert len(result._data) == 3
    for actual, expected in zip(result._data, TESTING_DATA_3_3):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert a.display_symbol == e


def test_load_pattern_from_file_fnf():
    with pytest.raises(FileNotFoundError):
        PatternDisplayModel.load_from_pattern_file("I don't exist")


def test_init(model):
    assert model._data == TESTING_DATA_3_2


def test_rowCount(model):
    assert model.rowCount(None) == 2


def test_columnCount(model):
    assert model.columnCount(None) == 3


def test_set_colour_mode(model):
    assert not model.show_colours
    model.set_colour_mode(True)
    assert model.show_colours
    model.set_colour_mode(False)
    assert not model.show_colours


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
