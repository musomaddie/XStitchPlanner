from unittest.mock import MagicMock, call, patch

from gui.patterns_view.pattern_editor_view import PatternEditorView

FILE_LOC = "old_gui.patterns_view.pattern_editor_view"


@patch(f"{FILE_LOC}.PatternTitleBar")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternEditorView.addWidget")
@patch(f"{FILE_LOC}.PatternDisplayView")
def test_init(display_view_mock, add_widget_mock, widget_mock, title_bar_mock):
    title = "Testing"
    model_mock = MagicMock()
    editor_view = PatternEditorView(title, model_mock)

    title_bar_mock.assert_called_once_with(title, model_mock, editor_view)
    widget_mock.assert_has_calls([call(), call().setLayout(title_bar_mock.return_value)])
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(display_view_mock.return_value)])
    display_view_mock.assert_called_once_with(
        model_mock, title_bar_mock().current_cell, editor_view)

    assert editor_view.model == model_mock
    assert editor_view.title_bar == title_bar_mock.return_value
    assert editor_view.table_view == display_view_mock.return_value
