from unittest.mock import call, patch

from gui.stitching.current.options.current_stitching_options_overlay import \
    CurrentStitchingOptionsOverlay

FILE_LOC = "gui.stitching.current.options.current_stitching_options_overlay"


@patch(f"{FILE_LOC}.CurrentStitchingOptionsOverlay.addWidget")
@patch(f"{FILE_LOC}.CurrentStitchingNextButtonsLayout")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.QLabel")
def test_init(label_mock, widget_mock, next_buttons_mock, add_widget_mock):
    overlay = CurrentStitchingOptionsOverlay(None)

    label_mock.assert_called_once_with("Options menu")
    add_widget_mock.assert_has_calls(
        [call(label_mock.return_value), call(widget_mock.return_value)])
    next_buttons_mock.assert_called_once_with(overlay)
    widget_mock.assert_has_calls(
        [call(), call().setLayout(next_buttons_mock.return_value)])
