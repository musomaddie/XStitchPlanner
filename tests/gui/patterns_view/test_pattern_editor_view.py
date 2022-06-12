from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QTableView, QVBoxLayout, QWidget

from gui.patterns_view.editor_details.pattern_title_bar import PatternTitleBar
from gui.patterns_view.pattern_editor_view import PatternEditorView

FILE_LOC = "gui.patterns_view.pattern_editor_view."


@patch(f"{FILE_LOC}PatternDisplayView")
@patch(f"{FILE_LOC}PatternTitleBar")
@patch("gui.patterns_view.editor_details.pattern_title_bar.CurrentCellLayout")
def test_init(cc_mock, title_bar_mock, mock_display, qtbot):
    mock_display.return_value = QTableView()
    model_mock = MagicMock()
    cc_mock.return_value = QVBoxLayout()
    title_bar_mock.return_value = PatternTitleBar("TESTING", model_mock)
    mock_model = MagicMock()
    mock_cell = MagicMock()

    test_widget = QWidget()
    editor_view = PatternEditorView("Testing", mock_model, mock_cell)
    test_widget.setLayout(editor_view)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2
    assert editor_view.model == mock_model
    assert title_bar_mock.mock_calls == [
        call("Testing", mock_model, editor_view)]
    assert mock_display.mock_calls == [
        call(mock_model, cc_mock.return_value, editor_view)]
