from unittest.mock import MagicMock, patch

from gui.stitching.stitching_view_overlay import StitchingViewOverlay

FILE_LOC = "gui.stitching.stitching_view_overlay"


@patch(f"{FILE_LOC}.PatternPrepareStitchingView")
@patch(f"{FILE_LOC}.StitchingViewOverlay.addWidget")
def test_init(add_widget_mock, view_mock):
    model_mock = MagicMock()
    view_overlay = StitchingViewOverlay(model_mock)

    view_mock.assert_called_once_with(model_mock, view_overlay)
    add_widget_mock.assert_called_once_with(view_mock.return_value)

    assert view_overlay.pattern_view == view_mock.return_value
