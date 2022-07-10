from unittest.mock import ANY, MagicMock, call, patch

from gui.stitching.stitching_view_overlay import StitchingViewOverlay

FILE_LOC = "gui.stitching.stitching_view_overlay"


@patch(f"{FILE_LOC}.PatternPrepareStitchingView")
@patch(f"{FILE_LOC}.StitchingViewOverlay.addWidget")
@patch(f"{FILE_LOC}.PreStitchingOptionsOverlay")
@patch(f"{FILE_LOC}.QWidget")
def test_init(widget_mock, options_mock, add_widget_mock, view_mock):
    model_mock = MagicMock()
    view_overlay = StitchingViewOverlay(model_mock)

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
