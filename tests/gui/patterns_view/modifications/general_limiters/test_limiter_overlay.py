from unittest.mock import ANY, MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QComboBox, QLabel, QStackedWidget, QVBoxLayout, QWidget
from calleee import InstanceOf

from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_overlay"


def setup_patched_mocks(cur_applied_mock, dropdown_mock, stack_mock):
    stack_mock.return_value = QStackedWidget()
    dropdown_mock.return_value = QComboBox()
    cur_applied_mock.return_value = QVBoxLayout()
    return MagicMock(), MagicMock(), MagicMock()


@pytest.mark.parametrize("direction", [LimiterType.ROW, LimiterType.COLUMN])
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


@pytest.mark.parametrize("direction", [LimiterType.ROW, LimiterType.COLUMN])
@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied")
@patch(f"{FILE_LOC}.LimiterOverlay.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
def test_get_all_modifiers(
        set_layout_mock, add_widget_mock,
        applied_mock, dropdown_mock,
        stack_mock, direction):
    current_cc_mock, model_mock, current_mod_mock = MagicMock(), MagicMock(), MagicMock()
    overlay = LimiterOverlay(current_cc_mock, direction, current_mod_mock, model_mock)

    # Also move this to INIT!
    set_layout_mock.assert_called_once_with(applied_mock())
    add_widget_mock.assert_has_calls(
        [
            call(InstanceOf(QLabel)),
            call(InstanceOf(QWidget)),  # currently_applied_layout_widget
            call(dropdown_mock()),
            call(stack_mock())
        ])

    applied_mock.assert_has_calls(
        [call(model_mock, direction, current_mod_mock, overlay),
         call.get_all_modifiers()])


@pytest.mark.parametrize(
    ("direction", "other_direction"),
    [(LimiterType.ROW, LimiterType.COLUMN),
     (LimiterType.COLUMN, LimiterType.ROW)]
)
@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied")
def test_create_new_pattern_tab(
        cur_applied_mock,
        dropdown_mock,
        stack_mock,
        direction,
        other_direction):
    current_cc_layout_mock, model_mock, current_mod_mock = setup_patched_mocks(
        cur_applied_mock, dropdown_mock, stack_mock)
    parent_mock = MagicMock()

    overlay = LimiterOverlay(
        current_cc_layout_mock, direction, current_mod_mock, model_mock, parent_mock)

    new_model_mock = MagicMock()
    mod_mock = MagicMock()
    overlay.create_new_pattern_tab(new_model_mock, mod_mock)

    assert parent_mock.mock_calls == [
        call.get_modifiers_for_direction(other_direction),
        call.create_new_pattern_tab(new_model_mock, {direction: mod_mock, other_direction: ANY})]
