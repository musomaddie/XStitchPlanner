from unittest.mock import patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_direction import \
    LimiterDirection
from gui.patterns_view.stitching_opt_menu_overview import \
    StitchingOptMenuOverview

FILE_LOC = "gui.patterns_view.stitching_opt_menu_overview."


@patch(f"{FILE_LOC}LimiterOverlay")
def test_init(overlay_mock):
    overlay_mock.return_value = QVBoxLayout()
    test_widget = QWidget()
    opt_menu = StitchingOptMenuOverview()
    test_widget.setLayout(opt_menu)

    overlay_mock.assert_called_once_with(LimiterDirection.COLUMN)
