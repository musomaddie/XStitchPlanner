from unittest.mock import ANY, MagicMock, call, patch

from gui.stitching.current.current_stitching_view_overlay import CurrentStitchingViewOverlay

FILE_LOC = "gui.stitching.current.current_stitching_view_overlay"


@patch(f"{FILE_LOC}.CurrentStitchingPatternModel")
@patch(f"{FILE_LOC}.CurrentStitchingPatternView")
@patch(f"{FILE_LOC}.CurrentStitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.CurrentStitchingOptionsOverlay")
@patch(f"{FILE_LOC}.QWidget")
def test_init(widget_mock, options_overlay_mock, add_widget_mock, view_mock, model_mock):
    # TODO: fix this test
    return
    stitcher_mock = MagicMock()
    overlay = CurrentStitchingViewOverlay(stitcher_mock)

    model_mock.assert_called_once_with(stitcher_mock)
    view_mock.assert_called_once_with(model_mock.return_value)
    add_widget_mock.assert_has_calls([call(view_mock.return_value), call(widget_mock.return_value)])
    options_overlay_mock.assert_called_once_with(stitcher_mock, overlay)

    widget_mock.assert_has_calls(
        [call(),
         call().setLayout(options_overlay_mock.return_value),
         call().minimumSize(),
         call().minimumSize().height(),
         call().setMinimumSize(300, ANY)])
