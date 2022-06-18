from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)

from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode
from gui.patterns_view.modifications.general_limiters.limiter_value_selector import (
    LimiterValueSelector, create_value_widget)

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


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
def test_create_value_widget(direction):
    # No selector
    wid = create_value_widget(direction, LimiterMode.NO_SELECTOR)
    assert len(wid.children()) == 0
    assert type(wid) == QWidget

    cur_str = ("Use current column" if direction == LimiterDirection.COLUMN
               else "Use current row")

    # Between
    wid = create_value_widget(direction, LimiterMode.BETWEEN)
    assert wid.layout().count() == 4
    assert type(wid.children()[0]) == QVBoxLayout
    assert_prompt(wid.children()[1], "Between:")
    assert_button(wid.children()[2], cur_str)
    assert_prompt(wid.children()[3], "&")
    assert_button(wid.children()[4], cur_str)

    # From
    wid = create_value_widget(direction, LimiterMode.FROM)
    assert wid.layout().count() == 2
    assert_prompt(wid.children()[1], "From:")
    assert_button(wid.children()[2], cur_str)

    # To
    wid = create_value_widget(direction, LimiterMode.TO)
    assert wid.layout().count() == 2
    assert_prompt(wid.children()[1], "To:")
    assert_button(wid.children()[2], cur_str)


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
@patch(f"{FILE_LOC}.create_value_widget")
def test_init_general(creator_mock, direction):
    creator_mock.return_value = QWidget()
    selector = LimiterValueSelector(direction, LimiterMode.NO_SELECTOR)
    test_widget = QWidget()
    test_widget.setLayout(selector)

    creator_mock.assert_called_once_with(direction, LimiterMode.NO_SELECTOR)
    assert selector.layout().count() == 3
    assert type(test_widget.children()[1]) == QLabel
    assert type(test_widget.children()[2]) == QWidget
    assert type(test_widget.children()[3]) == QPushButton
    assert test_widget.children()[3].text() == "Apply!"


@pytest.mark.parametrize(
    ("direction", "mode"),
    # TODO: surely there's a nicer way to do this
    [(LimiterDirection.COLUMN, LimiterMode.NO_SELECTOR),
     (LimiterDirection.ROW, LimiterMode.NO_SELECTOR),
     (LimiterDirection.COLUMN, LimiterMode.BETWEEN),
     (LimiterDirection.ROW, LimiterMode.BETWEEN),
     (LimiterDirection.COLUMN, LimiterMode.FROM),
     (LimiterDirection.ROW, LimiterMode.FROM),
     (LimiterDirection.COLUMN, LimiterMode.TO),
     (LimiterDirection.ROW, LimiterMode.TO)]
)
@patch(f"{FILE_LOC}.create_value_widget")
def test_init_explanation_text(creator_mock, direction, mode):
    creator_mock.return_value = QWidget()
    selector = LimiterValueSelector(direction, mode)
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
