from unittest.mock import MagicMock, call, patch

import pytest
from calleee import InstanceOf
from gui.patterns_view.modifications.general_limiters.limiter_drop_down import LimiterDropDown

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "old_gui.patterns_view.modifications.general_limiters.limiter_drop_down"


@pytest.mark.parametrize("direction", [LimiterType.COLUMN, LimiterType.ROW])
@patch(f"{FILE_LOC}.LimiterDropDown.addItems")
def test_init_dropdown(add_items_mock, direction):
    value_selector_mock = MagicMock()
    dropdown = LimiterDropDown(direction, value_selector_mock)

    assert dropdown.options == [
        LimiterMode.NO_SELECTOR,
        LimiterMode.BETWEEN,
        LimiterMode.FROM,
        LimiterMode.TO]

    if direction == LimiterType.ROW:
        add_items_mock.assert_called_once_with(["No Rows", "Between Rows", "From Row", "To Row"])
    else:
        add_items_mock.assert_called_once_with(
            ["No Columns", "Between Columns", "From Column", "To Column"])


@patch(f"{FILE_LOC}.LimiterDropDown.addItems")
@patch(f"{FILE_LOC}.LimiterDropDown.currentIndex")
def test_update_currently_selected(current_index_mock, add_items_mock):
    value_selector_mock = MagicMock()
    dropdown = LimiterDropDown(LimiterType.COLUMN, value_selector_mock)
    dropdown.update_currently_selected()

    assert current_index_mock.called
    value_selector_mock.assert_has_calls([call.change_selected(InstanceOf(LimiterMode))])
