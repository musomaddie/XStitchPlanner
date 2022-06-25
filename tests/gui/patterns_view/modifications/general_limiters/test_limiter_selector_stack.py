from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_selector_stack import \
    LimiterSelectorStack
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_selector_stack"


def setup_mocks(selector_mock):
    selector_mock.return_value = QVBoxLayout()
    return MagicMock(), MagicMock()


@pytest.mark.parametrize("direction", list(LimiterDirection))
@patch(f"{FILE_LOC}.LimiterValueSelector")
def test_init(selector_mock, direction):
    current_cc_layout_mock, applier_mock = setup_mocks(selector_mock)
    selector_stack = LimiterSelectorStack(applier_mock, current_cc_layout_mock, direction)

    expected_calls = [
        call(current_cc_layout_mock, applier_mock, direction, LimiterMode.NO_SELECTOR),
        call(current_cc_layout_mock, applier_mock, direction, LimiterMode.BETWEEN),
        call(current_cc_layout_mock, applier_mock, direction, LimiterMode.FROM),
        call(current_cc_layout_mock, applier_mock, direction, LimiterMode.TO)]

    assert selector_mock.mock_calls == expected_calls

    assert len(selector_stack.selection_dictionary) == 4
    for value in selector_stack.selection_dictionary.values():
        assert type(value) == QWidget

    assert selector_stack.layout().count() == 4


@patch(f"{FILE_LOC}.LimiterValueSelector")
def test_change_selector(selector_mock):
    current_cc_layout_mock, applier_mock = setup_mocks(selector_mock)
    selector_stack = LimiterSelectorStack(
        applier_mock, current_cc_layout_mock, LimiterDirection.ROW)

    selector_stack.change_selected(LimiterMode.BETWEEN)
    assert selector_stack.currentIndex() == 1

    selector_stack.change_selected(LimiterMode.NO_SELECTOR)
    assert selector_stack.currentIndex() == 0

    selector_stack.change_selected(LimiterMode.FROM)
    assert selector_stack.currentIndex() == 2

    selector_stack.change_selected(LimiterMode.TO)
    assert selector_stack.currentIndex() == 3
