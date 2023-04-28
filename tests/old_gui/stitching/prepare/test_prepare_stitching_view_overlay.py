from unittest.mock import ANY, MagicMock, call, patch

import pytest
from gui.stitching.prepare.prepare_stitching_view_overlay import PrepareStitchingViewOverlay

from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT

FILE_LOC = "old_gui.stitching.prepare.prepare_stitching_view_overlay"


@patch(f"{FILE_LOC}.PatternPrepareStitchingView")
@patch(f"{FILE_LOC}.PrepareStitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.PreStitchingOptionsOverlay")
@patch(f"{FILE_LOC}.QWidget")
def test_init(widget_mock, options_mock, add_widget_mock, view_mock):
    model_mock = MagicMock()
    view_overlay = PrepareStitchingViewOverlay(model_mock)

    view_mock.assert_called_once_with(model_mock, view_overlay)
    add_widget_mock.assert_has_calls(
        [call(view_mock.return_value), call(widget_mock.return_value)])
    options_mock.assert_called_once_with(view_overlay)

    widget_mock.assert_has_calls(
        [call(),
         call().setLayout(options_mock.return_value),
         call().minimumSize(),
         call().minimumSize().height(),
         call().setMinimumSize(300, ANY)])

    assert view_overlay.pattern_view == view_mock.return_value


@patch(f"{FILE_LOC}.PatternPrepareStitchingView")
@patch(f"{FILE_LOC}.PrepareStitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.PreStitchingOptionsOverlay")
@patch(f"{FILE_LOC}.QWidget")
@pytest.mark.parametrize("corner", [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
def test_start_stitching(widget_mock, options_mock, add_widget_mock, view_mock, corner):
    model_mock, parent_mock = [MagicMock() for _ in range(2)]
    view_overlay = PrepareStitchingViewOverlay(model_mock, parent_mock)

    view_overlay.start_stitching(corner)
    parent_mock.assert_has_calls(
        [call.start_stitching(view_mock().model._data, corner)])
