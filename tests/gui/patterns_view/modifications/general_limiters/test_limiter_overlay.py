from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtWidgets import QComboBox, QLabel, QStackedWidget, QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay
from pattern_modifiers.limiters.limiter_direction import LimiterDirection

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_overlay"


@pytest.mark.parametrize("direction", [LimiterDirection.ROW, LimiterDirection.COLUMN])
@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied")
def test_init(cur_applied_mock, dropdown_mock, stack_mock, direction):
    current_cc_layout_mock = MagicMock()
    stack_mock.return_value = QStackedWidget()
    dropdown_mock.return_value = QComboBox()
    cur_applied_mock.return_value = QVBoxLayout()
    test_widget = QWidget()
    overlay = LimiterOverlay(current_cc_layout_mock, direction)
    test_widget.setLayout(overlay)

    stack_mock.assert_called_once_with(current_cc_layout_mock, direction)
    dropdown_mock.assert_called_once_with(direction, overlay.value_selector_stack)

    # Asserting the layout is set up correctly
    assert test_widget.layout().count() == 4
    assert type(test_widget.children()[1]) == QLabel
    assert type(test_widget.children()[2]) == QWidget
    assert type(test_widget.children()[3]) == QComboBox
    assert type(test_widget.children()[4]) == QStackedWidget
