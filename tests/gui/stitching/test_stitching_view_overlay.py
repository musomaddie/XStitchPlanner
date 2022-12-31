from unittest.mock import MagicMock, call, patch

import pytest

from gui.stitching.stitching_view_overlay import StitchingViewOverlay
from pattern_cells.pattern_cell import PatternCell
from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT

FILE_LOC = "gui.stitching.stitching_view_overlay"


@patch(f"{FILE_LOC}.PrepareStitchingViewOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay.start_stitching")
def test_init(start_stitching_mock, add_widget_mock, widget_mock, prepare_overlay_mock):
    model_mock = MagicMock()
    overlay = StitchingViewOverlay(model_mock)

    prepare_overlay_mock.assert_called_once_with(model_mock, overlay)
    widget_mock.assert_has_calls([call(), call().setLayout(prepare_overlay_mock.return_value)])
    add_widget_mock.assert_called_once_with(widget_mock.return_value)
    start_stitching_mock.assert_called_once_with(model_mock._data, TOP_LEFT)

    assert overlay.prepare_layout == prepare_overlay_mock.return_value
    assert overlay.stitching_layout is None


@patch(f"{FILE_LOC}.PrepareStitchingViewOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay.setCurrentWidget")
@patch(f"{FILE_LOC}.CurrentStitchingViewOverlay")
@patch(f"{FILE_LOC}.FullParkingStitcher")
@pytest.mark.parametrize("corner", [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
def test_start_stitching(
        stitcher_mock,
        current_view_overlay_mock,
        current_widget_mock,
        add_widget_mock,
        widget_mock,
        prepare_overlay_mock,
        corner):
    model_mock = MagicMock()
    overlay = StitchingViewOverlay(model_mock)

    c1 = PatternCell("a", "310", [], "")
    c2 = PatternCell("b", "550", [], "")

    original_pattern_data = [[c1, c2], [c2, c1]]
    overlay.start_stitching(original_pattern_data, corner)

    # TODO: switch the following two asserts to assert_called_once_with after the saved start in
    #  the init is removed
    stitcher_mock.assert_has_calls(
        [call(model_mock._data, TOP_LEFT), call(original_pattern_data, corner)])
    # call(
    #     [[stitching_cell_mock.return_value, stitching_cell_mock.return_value],
    #      [stitching_cell_mock.return_value, stitching_cell_mock.return_value]], corner)
    # ])

    current_view_overlay_mock.assert_has_calls(
        [call(stitcher_mock.return_value, overlay), call(stitcher_mock.return_value, overlay)])
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(widget_mock.return_value)])
    current_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(widget_mock.return_value)])
