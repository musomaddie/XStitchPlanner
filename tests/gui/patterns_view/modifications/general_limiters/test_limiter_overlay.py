from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QComboBox, QLabel, QStackedWidget, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_overlay import LimiterOverlay

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_overlay"


@pytest.mark.parametrize("direction", [LimiterDirection.ROW, LimiterDirection.COLUMN])
@patch(f"{FILE_LOC}.LimiterSelectorStack")
@patch(f"{FILE_LOC}.LimiterDropDown")
def test_init(dropdown_mock, stack_mock, direction):
    stack_mock.return_value = QStackedWidget()
    dropdown_mock.return_value = QComboBox()
    test_widget = QWidget()
    overlay = LimiterOverlay(direction)
    test_widget.setLayout(overlay)

    stack_mock.assert_called_once_with(direction)
    dropdown_mock.assert_called_once_with(
        direction, overlay.value_selector_stack)

    # Asserting the layout is set up correctly
    assert test_widget.layout().count() == 3
    assert type(test_widget.children()[1]) == QLabel
    assert type(test_widget.children()[2]) == QComboBox
    assert type(test_widget.children()[3]) == QStackedWidget
