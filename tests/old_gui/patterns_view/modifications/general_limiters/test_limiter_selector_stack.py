from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QVBoxLayout
from gui.patterns_view.modifications.general_limiters.limiter_selector_stack import \
    LimiterSelectorStack

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "old_gui.patterns_view.modifications.general_limiters.limiter_selector_stack"


@pytest.mark.parametrize("direction", list(LimiterType))
@patch(f"{FILE_LOC}.LimiterValueSelector")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.LimiterSelectorStack.addWidget")
def test_init(add_widget_mock, widget_mock, selector_mock, direction):
    current_cc_layout_mock, applier_mock = MagicMock(), MagicMock()

    selector_stack = LimiterSelectorStack(applier_mock, current_cc_layout_mock, direction)

    selector_mock.assert_has_calls(
        [call(current_cc_layout_mock, applier_mock, direction, mode) for mode in list(LimiterMode)])
    widget_mock.assert_has_calls(
        [call(), call().setLayout(selector_mock.return_value),
         call(), call().setLayout(selector_mock.return_value),
         call(), call().setLayout(selector_mock.return_value),
         call(), call().setLayout(selector_mock.return_value)])

    add_widget_mock.assert_has_calls([call(widget_mock.return_value) for _ in range(3)])

    assert selector_stack.current_cell_layout == current_cc_layout_mock
    assert selector_stack.limiter_direction == direction
    assert len(selector_stack.selection_dictionary) == 4
    for mode in list(LimiterMode):
        assert mode in selector_stack.selection_dictionary
    for value in selector_stack.selection_dictionary.values():
        assert value == widget_mock.return_value


@patch(f"{FILE_LOC}.LimiterValueSelector")
def test_change_selector(selector_mock):
    selector_mock.return_value = QVBoxLayout()
    current_cc_layout_mock, applier_mock = MagicMock(), MagicMock()

    selector_stack = LimiterSelectorStack(
        applier_mock, current_cc_layout_mock, LimiterType.ROW)

    selector_stack.change_selected(LimiterMode.BETWEEN)
    assert selector_stack.currentIndex() == 1

    selector_stack.change_selected(LimiterMode.NO_SELECTOR)
    assert selector_stack.currentIndex() == 0

    selector_stack.change_selected(LimiterMode.FROM)
    assert selector_stack.currentIndex() == 2

    selector_stack.change_selected(LimiterMode.TO)
    assert selector_stack.currentIndex() == 3
