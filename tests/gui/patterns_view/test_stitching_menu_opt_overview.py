from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.stitching_opt_menu_overview import StitchingOptMenuOverview
from pattern_modifiers.limiters.limiter_direction import LimiterDirection

FILE_LOC = "gui.patterns_view.stitching_opt_menu_overview."


@patch(f"{FILE_LOC}LimiterOverlay")
def test_init(overlay_mock):
    overlay_mock.return_value = QVBoxLayout()
    current_cc_layout_mock = MagicMock()
    test_widget = QWidget()
    opt_menu = StitchingOptMenuOverview(current_cc_layout_mock)
    test_widget.setLayout(opt_menu)

    overlay_mock.assert_called_once_with(current_cc_layout_mock, LimiterDirection.COLUMN)
