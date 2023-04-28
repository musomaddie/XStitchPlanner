from unittest.mock import MagicMock, call, patch

from gui.patterns_view.editor_details.pattern_display_view import PatternDisplayView

FILE_LOC = "old_gui.patterns_view.editor_details.pattern_display_view"


@patch(f"{FILE_LOC}.PatternView.setModel")
@patch(f"{FILE_LOC}.PatternView.clicked")
def test_init(clicked_mock, set_model_mock, qtbot):
    parent_mock, cc_mock = [MagicMock() for _ in range(2)]
    display_view = PatternDisplayView(MagicMock(), cc_mock, parent_mock)

    clicked_mock.assert_has_calls([call.connect(cc_mock.update_values)])
    assert display_view.parent == parent_mock
