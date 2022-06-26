from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.stitching_opt_menu_overview import StitchingOptMenuOverview
from pattern_modifiers.limiters.limiter_direction import LimiterDirection

FILE_LOC = "gui.patterns_view.stitching_opt_menu_overview"


def setup_mocks(overlay_mock):
    overlay_mock.return_value = QVBoxLayout()
    return MagicMock(), MagicMock(), {LimiterDirection.COLUMN: [MagicMock()],
                                      LimiterDirection.ROW: [MagicMock()]}


@patch(f"{FILE_LOC}.LimiterOverlay")
def test_init(overlay_mock):
    current_cc_layout_mock, mod_mock, model_mock = setup_mocks(overlay_mock)
    test_widget = QWidget()
    opt_menu = StitchingOptMenuOverview(current_cc_layout_mock, model_mock, mod_mock, None)
    test_widget.setLayout(opt_menu)

    overlay_mock.assert_has_calls(
        [
            call(
                current_cc_layout_mock,
                LimiterDirection.COLUMN,
                mod_mock[LimiterDirection.COLUMN],
                model_mock, opt_menu),
            call(
                current_cc_layout_mock,
                LimiterDirection.ROW,
                mod_mock[LimiterDirection.ROW],
                model_mock, opt_menu)
        ])

    assert test_widget.layout().count() == 2


@patch(f"{FILE_LOC}.LimiterOverlay")
def test_create_new_pattern_tab(overlay_mock):
    cc_mock, mod_mock, model_mock = setup_mocks(overlay_mock)
    parent_mock = MagicMock()
    opt_menu = StitchingOptMenuOverview(cc_mock, model_mock, mod_mock, parent_mock)

    new_model_mock, new_mod_mock = MagicMock(), MagicMock()
    opt_menu.create_new_pattern_tab(new_model_mock, new_mod_mock)
    assert parent_mock.mock_calls == [call.create_new_pattern_tab(new_model_mock, new_mod_mock)]
