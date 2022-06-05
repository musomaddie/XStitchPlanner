from unittest import mock

import pytest

from gui.patterns_view.pattern_display_grid import PatternDisplayGridModel

TESTING_DATA_3_2 = [['a', 'a', 'b'], ['b', 'b', 'a']]
TESTING_DATA_3_3 = [['a', 'a', 'b'], ['b', 'b', 'c'], ['c', 'c', 'a']]
TESTING_DATA_3_3_STR = "aab\nbbc\ncca\n"


@pytest.fixture()
def model():
    return PatternDisplayGridModel(TESTING_DATA_3_2)


# Model tests!
def test_load_pattern_from_file():
    open_mock = mock.mock_open(read_data=TESTING_DATA_3_3_STR)
    with mock.patch("gui.patterns_view.pattern_display_grid.open", open_mock):
        result = PatternDisplayGridModel.load_from_pattern_file("TESTING")
    assert type(result) == PatternDisplayGridModel
    assert len(result.data) == 3
    for actual, expected in zip(result.data, TESTING_DATA_3_3):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert a == e


def test_load_pattern_from_file_fnf():
    with pytest.raises(FileNotFoundError):
        PatternDisplayGridModel.load_from_pattern_file("I don't exist")


def test_init(model):
    assert model.data == TESTING_DATA_3_2


def test_rowCount(model):
    assert model.rowCount(None) == 2


def test_columnCount(model):
    assert model.columnCount(None) == 3
