from unittest.mock import MagicMock, call, patch

import pytest
from gui.pattern_display_model import PatternDisplayModel

from floss_thread import Thread
from pattern_cells.pattern_cell import PatternCell

FILE_LOC = "old_gui.pattern_display_model"

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


@pytest.fixture()
def model():
    return PatternDisplayModel(TESTING_DATA_3_2)


# Model tests!
@patch(f"{FILE_LOC}.load_from_pattern_file")
def test_load_pattern_from_file(load_from_pattern_file_mock):
    load_from_pattern_file_mock.return_value = TESTING_DATA_3_3
    result = PatternDisplayModel.load_from_pattern_file("TESTING")

    assert load_from_pattern_file_mock.called_once_with("TESTING", "TESTING")
    assert type(result) == PatternDisplayModel
    assert result._data == TESTING_DATA_3_3


def test_load_pattern_from_file_fnf():
    with pytest.raises(FileNotFoundError):
        PatternDisplayModel.load_from_pattern_file("I don't exist")


def test_set_colour_mode(model):
    assert not model.show_colours
    model.set_colour_mode(True)
    assert model.show_colours
    model.set_colour_mode(False)
    assert not model.show_colours


@pytest.mark.parametrize("show_gridlines", [True, False])
def test_change_pattern_visible_gridlines(show_gridlines, model):
    display_mock = MagicMock()
    model.add_display(display_mock)
    model.change_pattern_visible_gridlines(show_gridlines)
    assert display_mock.mock_calls == [call.setShowGrid(show_gridlines)]
