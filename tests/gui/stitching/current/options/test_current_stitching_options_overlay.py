from unittest.mock import patch

from gui.stitching.current.options.current_stitching_options_overlay import \
    CurrentStitchingOptionsOverlay

FILE_LOC = "gui.stitching.current.current_stitching_options_overlay"


@patch(f"{FILE_LOC}.CurrentStitchingOptionsOverlay.addWidget")
@patch(f"{FILE_LOC}.QLabel")
def test_init(label_mock, add_widget_mock):
    overlay = CurrentStitchingOptionsOverlay()

    label_mock.assert_called_once_with("Options menu")
    add_widget_mock.assert_called_once_with(label_mock.return_value)
