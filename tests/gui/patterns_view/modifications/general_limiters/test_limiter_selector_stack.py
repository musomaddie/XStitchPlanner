from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode
from gui.patterns_view.modifications.general_limiters.limiter_selector_stack import \
    LimiterSelectorStack

FILE_LOC = "gui.patterns_view.modifications.general_limiters.limiter_selector_stack"


@pytest.mark.parametrize("direction", [LimiterDirection.ROW, LimiterDirection.COLUMN])
@patch(f"{FILE_LOC}.LimiterValueSelector")
def test_init(selector_mock, direction):
    current_cc_layout_mock = MagicMock()
    selector_mock.return_value = QVBoxLayout()
    selector_stack = LimiterSelectorStack(current_cc_layout_mock, direction)

    expected_calls = [call(current_cc_layout_mock, direction, LimiterMode.NO_SELECTOR),
                      call(current_cc_layout_mock, direction, LimiterMode.BETWEEN),
                      call(current_cc_layout_mock, direction, LimiterMode.FROM),
                      call(current_cc_layout_mock, direction, LimiterMode.TO)]

    assert selector_mock.mock_calls == expected_calls

    assert len(selector_stack.selection_dictionary) == 4
    for value in selector_stack.selection_dictionary.values():
        assert type(value) == QWidget

    assert selector_stack.layout().count() == 4
