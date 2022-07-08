from unittest.mock import MagicMock, patch

from gui.stitching.pattern_prepare_stitching_view import PatternPrepareStitchingView

FILE_LOC = "gui.stitching.pattern_prepare_stitching_view"


@patch(f"{FILE_LOC}.PatternView.setModel")
def test_init(set_model_mock, qtbot):
    model_mock = MagicMock()
    view = PatternPrepareStitchingView(model_mock)
    assert view.model == model_mock
