from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QGridLayout, QVBoxLayout

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay

FILE_LOC = "gui.patterns_view.pattern_display_overlay"

get_cc_layout = MagicMock()


class TestWid(QGridLayout):
    def __init__(self):
        super().__init__()

    def get_current_cell_layout(self):
        return get_cc_layout


def setup_mocks(stitching_mock, editor_mock):
    editor_mock.return_value = TestWid()
    stitching_mock.return_value = QVBoxLayout()
    table_mock = MagicMock(return_value=PatternDisplayModel((["a", "b"], ["b", "a"])))
    return table_mock, MagicMock()


@patch(f"{FILE_LOC}.PatternEditorView")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview")
@patch(f"{FILE_LOC}.QSize")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternDisplayOverlay.addWidget")
def test_init(add_widget_mock, widget_mock, size_mock, stitching_opt_mock, editor_view_mock):
    pattern_name = "Testing"
    model_mock = MagicMock()
    current_mods = MagicMock()

    overlay = PatternDisplayOverlay(pattern_name, model_mock, current_mods)

    editor_view_mock.assert_called_once_with(pattern_name, model_mock, overlay)
    editor_view_mock.assert_has_calls(
        [call(pattern_name, model_mock, overlay), call().get_current_cell_layout()])
    stitching_opt_mock.assert_called_once_with(
        editor_view_mock().get_current_cell_layout.return_value, model_mock, current_mods, overlay)
    widget_mock.assert_has_calls(
        [call(), call().setLayout(editor_view_mock.return_value),
         call(), call().setLayout(stitching_opt_mock.return_value),
         call().maximumSize(), call().maximumSize().height(),
         call().setMaximumSize(size_mock.return_value)])
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(widget_mock.return_value)])

    assert overlay.pattern_title == pattern_name
    assert overlay.model == model_mock
    assert overlay.editor == editor_view_mock.return_value
    assert overlay.opt_menu == stitching_opt_mock.return_value


@patch(f"{FILE_LOC}.PatternEditorView")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview")
@patch(f"{FILE_LOC}.QSize")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternDisplayOverlay.addWidget")
def test_create_new_pattern_tab(
        add_widget_mock, widget_mock, size_mock, stitching_opt_mock, editor_mock):
    parent_mock = MagicMock()
    overlay = PatternDisplayOverlay("Testing", MagicMock(), MagicMock(), parent_mock)
    new_model_mock = MagicMock()
    modification_mock = MagicMock()
    overlay.create_new_pattern_tab(new_model_mock, modification_mock)

    parent_mock.assert_has_calls(
        [call.create_new_pattern_tab("Testing", new_model_mock, modification_mock)])
