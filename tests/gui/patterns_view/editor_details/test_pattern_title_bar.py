from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.editor_details.pattern_title_bar import PatternTitleBar

FILE_LOC = "gui.patterns_view.editor_details.pattern_title_bar."


@patch(f"{FILE_LOC}CurrentCellLayout")
def test_init(current_cell_mock):
    current_cell_mock.return_value = QVBoxLayout()
    mock_model = MagicMock()

    test_widget = QWidget()
    title_bar = PatternTitleBar("TESTING", mock_model)
    test_widget.setLayout(title_bar)

    assert test_widget.layout().count() == 2
    assert title_bar.model == mock_model

    assert current_cell_mock.mock_calls == [call(title_bar)]
