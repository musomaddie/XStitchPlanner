from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QWidget
from calleee import InstanceOf
from gui.patterns_view.editor_details.pattern_title_bar import PatternTitleBar

FILE_LOC = "old_gui.patterns_view.editor_details.pattern_title_bar"


@patch(f"{FILE_LOC}.CurrentCellLayout")
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.QWidget.setLayout")
@patch(f"{FILE_LOC}.PatternTitleBar.addWidget")
def test_init(add_widget_mock, set_layout_mock, qlabel_mock, current_cell_mock):
    pattern_name = "Testing"
    mock_model = MagicMock()
    title_bar = PatternTitleBar(pattern_name, mock_model)

    qlabel_mock.assert_called_once_with(pattern_name)
    set_layout_mock.assert_called_once_with(current_cell_mock.return_value)
    add_widget_mock.assert_has_calls([call(qlabel_mock.return_value), call(InstanceOf(QWidget))])

    assert title_bar.title == qlabel_mock.return_value
    assert title_bar.current_cell == current_cell_mock.return_value
    assert title_bar.model == mock_model


@patch(f"{FILE_LOC}.CurrentCellLayout")
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.QWidget.setLayout")
@patch(f"{FILE_LOC}.PatternTitleBar.addWidget")
def test_get_current_cell_layout(add_widget_mock, set_layout_mock, qlabel_mock, current_cell_mock):
    title_bar = PatternTitleBar("Testing", MagicMock())
    assert title_bar.get_current_cell_layout() == current_cell_mock.return_value
