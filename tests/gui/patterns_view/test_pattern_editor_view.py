from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QHBoxLayout, QTableView, QWidget

from gui.patterns_view.pattern_editor_view import PatternEditorView

FILE_LOC = "gui.patterns_view.pattern_editor_view."


@patch(f"{FILE_LOC}PatternDisplayView")
@patch(f"{FILE_LOC}PatternTitleBar")
def test_init(title_bar_mock, mock_display, qtbot):
    mock_display.return_value = QTableView()
    title_bar_mock.return_value = QHBoxLayout()
    mock_model = MagicMock()

    test_widget = QWidget()
    editor_view = PatternEditorView("Testing", mock_model)
    test_widget.setLayout(editor_view)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2
    assert editor_view.model == mock_model
    assert title_bar_mock.mock_calls == [
        call("Testing", mock_model, editor_view)]
    assert mock_display.mock_calls == [call("Testing", mock_model, editor_view)]
