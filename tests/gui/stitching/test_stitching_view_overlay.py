from unittest.mock import MagicMock, call, patch

from gui.stitching.stitching_view_overlay import StitchingViewOverlay

FILE_LOC = "gui.stitching.stitching_view_overlay"


@patch(f"{FILE_LOC}.PrepareStitchingViewOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingViewOverlay.addWidget")
def test_init(add_widget_mock, widget_mock, prepare_overlay_mock):
    model_mock = MagicMock()
    overlay = StitchingViewOverlay(model_mock)

    prepare_overlay_mock.assert_called_once_with(model_mock, overlay)
    widget_mock.assert_has_calls([call(), call().setLayout(prepare_overlay_mock.return_value)])
    add_widget_mock.assert_called_once_with(widget_mock.return_value)
