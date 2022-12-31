from unittest.mock import MagicMock, call, patch

from PyQt6.QtCore import Qt

from gui.stitching.stitching_overlay import StitchingOverlay

FILE_LOC = "gui.stitching.stitching_overlay"


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.StitchingOverlay.addWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay")
def test_init(view_overlay_mock, add_widget_mock, label_mock):
    model_mock = MagicMock()
    overlay = StitchingOverlay("Testing", model_mock)

    label_mock.assert_has_calls(
        [call("Testing"), call().setAlignment(Qt.AlignmentFlag.AlignCenter)])
    add_widget_mock.assert_has_calls(
        [call(label_mock.return_value), call(view_overlay_mock.return_value)])
    view_overlay_mock.assert_called_once_with(model_mock, overlay)

    assert overlay.title == label_mock.return_value
    assert overlay.view == view_overlay_mock.return_value
