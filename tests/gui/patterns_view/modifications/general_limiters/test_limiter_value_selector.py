from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)
from allpairspy import AllPairs

from gui.patterns_view.modifications.general_limiters.limiter_value_selector import (
    LimiterValueSelector, ValueWidget)
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode

FILE_LOC = "gui.patterns_view.modifications.general_limiters" \
           ".limiter_value_selector"


# Helpers
def assert_prompt(prompt: QWidget, expected_str: str):
    assert type(prompt) == QLabel
    assert prompt.text() == expected_str


def assert_button(widget: QWidget, exp_button_str: str):
    assert type(widget.layout()) == QHBoxLayout
    assert widget.layout().count() == 2
    assert type(widget.children()[1]) == QLineEdit
    assert type(widget.children()[2]) == QPushButton
    assert widget.children()[2].text() == exp_button_str


def setup_mocks(creator_mock):
    m = MagicMock()
    m.get_current_value.return_value = 100
    creator_mock.return_value = QWidget()
    return MagicMock(), m


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
def test_value_widget(direction):
    applier_mocks, current_cell_layout_mock = setup_mocks(MagicMock())
    # No selector
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.NO_SELECTOR)
    assert len(wid.children()) == 0

    cur_str = ("Use current column" if direction == LimiterDirection.COLUMN
               else "Use current row")

    # Between
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.BETWEEN)
    assert wid.layout().count() == 4
    assert type(wid.children()[0]) == QVBoxLayout
    assert_prompt(wid.children()[1], "Between:")
    assert_button(wid.children()[2], cur_str)
    assert_prompt(wid.children()[3], "&")
    assert_button(wid.children()[4], cur_str)

    # From
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.FROM)
    assert wid.layout().count() == 2
    assert_prompt(wid.children()[1], "From:")
    assert_button(wid.children()[2], cur_str)

    # To
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.TO)
    assert wid.layout().count() == 2
    assert_prompt(wid.children()[1], "To:")
    assert_button(wid.children()[2], cur_str)


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
@patch(f"{FILE_LOC}.ValueWidget")
def test_init_general(value_mock, direction):
    applier_mock, current_cell_mock = setup_mocks(value_mock)
    selector = LimiterValueSelector(
        current_cell_mock, applier_mock, direction, LimiterMode.NO_SELECTOR)
    test_widget = QWidget()
    test_widget.setLayout(selector)

    value_mock.assert_called_once_with(current_cell_mock, direction, LimiterMode.NO_SELECTOR)
    assert selector.layout().count() == 3
    assert type(test_widget.children()[1]) == QLabel
    assert type(test_widget.children()[2]) == QWidget
    assert type(test_widget.children()[3]) == QPushButton
    assert test_widget.children()[3].text() == "Apply!"


@pytest.mark.parametrize(
    ("direction", "mode"),
    [values for values in AllPairs(
        [
            [LimiterDirection.COLUMN, LimiterDirection.ROW],
            [LimiterMode.NO_SELECTOR, LimiterMode.BETWEEN, LimiterMode.TO, LimiterMode.FROM]
        ])
     ]
)
@patch(f"{FILE_LOC}.ValueWidget")
def test_init_explanation_text(value_mock, direction, mode):
    applier_mock, current_cc_layout_mock = setup_mocks(value_mock)
    selector = LimiterValueSelector(current_cc_layout_mock, applier_mock, direction, mode)
    test_widget = QWidget()
    test_widget.setLayout(selector)

    actual_text = test_widget.children()[1].text()

    if mode == LimiterMode.NO_SELECTOR:
        if direction == LimiterDirection.COLUMN:
            assert actual_text == "Removes any currently applied column limits"
        else:
            assert actual_text == "Removes any currently applied row limits"
    elif mode == LimiterMode.BETWEEN:
        if direction == LimiterDirection.COLUMN:
            assert actual_text == "Only shows the pattern between " \
                                  "(inclusive) the provided column values"
        else:
            assert actual_text == "Only shows the pattern between " \
                                  "(inclusive) the provided row values"
    elif mode == LimiterMode.FROM:
        if direction == LimiterDirection.COLUMN:
            assert actual_text == "Only shows the pattern right " \
                                  "(inclusive) of the provided column value"
        else:
            assert actual_text == "Only shows the pattern below " \
                                  "(inclusive) the provided row value"
    else:
        if direction == LimiterDirection.COLUMN:
            assert actual_text == "Only shows the pattern left (inclusive) " \
                                  "of the provided column value"
        else:
            assert actual_text == "Only shows the pattern above (inclusive) " \
                                  "the provided row value"


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
def test_use_current_value_button(direction, qtbot):
    def mock_get_cur_value_method(direction):
        if direction == LimiterDirection.COLUMN:
            return 100
        else:
            return 200

    current_cell_layout_mock = MagicMock()
    current_cell_layout_mock.get_current_value.side_effect = mock_get_cur_value_method
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.FROM)
    qtbot.addWidget(wid)

    qtbot.mouseClick(wid.children()[2].children()[2], Qt.MouseButton.LeftButton)
    expected_value = 101 if direction == LimiterDirection.COLUMN else 201
    assert str(expected_value) in wid.children()[2].children()[1].text()
