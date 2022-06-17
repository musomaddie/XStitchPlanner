from unittest.mock import call, patch

import pytest
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_direction import \
    LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import \
    LimiterMode
from gui.patterns_view.modifications.general_limiters.limiter_selector_stack \
    import \
    LimiterSelectorStack

FILE_LOC = "gui.patterns_view.modifications.general_limiters" \
           ".limiter_selector_stack"


@pytest.mark.parametrize(
    "direction", [LimiterDirection.ROW, LimiterDirection.COLUMN]
)
@patch(f"{FILE_LOC}.LimiterValueSelector")
def test_init(selector_mock, direction, qtbot):
    selector_mock.return_value = QVBoxLayout()
    selector_stack = LimiterSelectorStack(direction)
    qtbot.addWidget(selector_stack)

    expected_calls = [call(direction, LimiterMode.NO_SELECTOR),
                      call(direction, LimiterMode.BETWEEN),
                      call(direction, LimiterMode.FROM),
                      call(direction, LimiterMode.TO)]

    assert selector_mock.mock_calls == expected_calls

    assert len(selector_stack.selection_dictionary) == 4
    for value in selector_stack.selection_dictionary.values():
        assert type(value) == QWidget

    assert selector_stack.layout().count() == 4
