from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QComboBox, QLabel, QStackedWidget, QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from pattern_modifiers.limiters.limiter_direction import LimiterDirection

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_overlay"


def setup_patched_mocks(cur_applied_mock, dropdown_mock, stack_mock):
    stack_mock.return_value = QStackedWidget()
    dropdown_mock.return_value = QComboBox()
    cur_applied_mock.return_value = QVBoxLayout()
    return MagicMock(), MagicMock(), MagicMock()


@pytest.mark.parametrize("direction", [LimiterDirection.ROW, LimiterDirection.COLUMN])
@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied")
def test_init(cur_applied_mock, dropdown_mock, stack_mock, direction):
    current_cc_layout_mock, model_mock, current_mod_mock = setup_patched_mocks(
        cur_applied_mock, dropdown_mock, stack_mock)

    test_widget = QWidget()
    overlay = LimiterOverlay(current_cc_layout_mock, direction, current_mod_mock, model_mock)
    test_widget.setLayout(overlay)

    cur_applied_mock.assert_called_once_with(model_mock, direction, current_mod_mock, overlay)
    stack_mock.assert_called_once_with(
        cur_applied_mock.return_value, current_cc_layout_mock, direction)
    dropdown_mock.assert_called_once_with(direction, overlay.value_selector_stack)

    # Asserting the layout is set up correctly
    assert test_widget.layout().count() == 4
    assert type(test_widget.children()[1]) == QLabel
    assert type(test_widget.children()[2]) == QWidget
    assert type(test_widget.children()[3]) == QComboBox
    assert type(test_widget.children()[4]) == QStackedWidget


@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied")
def test_create_new_pattern_tab(cur_applied_mock, dropdown_mock, stack_mock):
    current_cc_layout_mock, model_mock, current_mod_mock = setup_patched_mocks(
        cur_applied_mock, dropdown_mock, stack_mock)
    parent_mock = MagicMock()

    overlay = LimiterOverlay(
        current_cc_layout_mock, LimiterDirection.COLUMN, current_mod_mock, model_mock, parent_mock)

    new_model_mock = MagicMock()
    mod_mock = MagicMock()
    overlay.create_new_pattern_tab(new_model_mock, mod_mock)

    assert parent_mock.mock_calls == [call.create_new_pattern_tab(new_model_mock, mod_mock)]
