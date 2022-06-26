from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

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
def test_init(stitching_opt_mock, editor_view_mock):
    table_model_mock, mod_mock = setup_mocks(stitching_opt_mock, editor_view_mock)
    test_widget = QWidget()
    overlay = PatternDisplayOverlay("Testing", table_model_mock, mod_mock)
    test_widget.setLayout(overlay)

    assert test_widget.layout().count() == 2
    editor_view_mock.assert_called_once_with("Testing", table_model_mock, overlay)
    stitching_opt_mock.assert_called_once_with(
        get_cc_layout, table_model_mock, mod_mock, overlay)
    opt_menu_layout_widg = test_widget.childAt(0, 1)
    assert opt_menu_layout_widg.maximumSize().width() == 300

# TODO: add test for create_new_pattern_tab
