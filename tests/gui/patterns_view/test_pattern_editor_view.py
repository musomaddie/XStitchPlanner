from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QTableView, QWidget

from gui.patterns_view.pattern_editor_view import PatternEditorView

FILE_LOC = "gui.patterns_view.pattern_editor_view."


@patch(f"{FILE_LOC}PatternDisplayView")
def test_init(mock_display, qtbot):
    mock_display.return_value = QTableView()
    mock_model = MagicMock()

    test_widget = QWidget()
    editor_view = PatternEditorView("Testing", mock_model)
    test_widget.setLayout(editor_view)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2
    assert editor_view.model == mock_model
    assert mock_display.called
