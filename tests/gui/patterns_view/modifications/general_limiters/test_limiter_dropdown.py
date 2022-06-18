from unittest.mock import MagicMock

import pytest

from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_drop_down import LimiterDropDown
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode


@pytest.mark.parametrize("direction", [LimiterDirection.COLUMN, LimiterDirection.ROW])
def test_init_dropdown(direction, qtbot):
    dropdown = LimiterDropDown(direction, MagicMock())
    qtbot.addWidget(dropdown)

    assert dropdown.currentIndex() == 0
    assert dropdown.options == [
        LimiterMode.NO_SELECTOR,
        LimiterMode.BETWEEN,
        LimiterMode.FROM,
        LimiterMode.TO]

    assert dropdown.count() == 4
    if direction == LimiterDirection.ROW:
        assert dropdown.itemText(0) == "No Rows"
        assert dropdown.itemText(1) == "Between Rows"
        assert dropdown.itemText(2) == "From Row"
        assert dropdown.itemText(3) == "To Row"
    else:
        assert dropdown.itemText(0) == "No Columns"
        assert dropdown.itemText(1) == "Between Columns"
        assert dropdown.itemText(2) == "From Column"
        assert dropdown.itemText(3) == "To Column"
