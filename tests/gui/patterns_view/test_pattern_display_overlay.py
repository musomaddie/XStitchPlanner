from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay

FILE_LOC = "gui.patterns_view.pattern_display_overlay"


# TODO: figure out which test is forcing the display of the python file (
#  window switch)

@patch(f"{FILE_LOC}.PatternEditorView")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview")
def test_init(stitching_opt_mock, editor_view_mock):
    get_cc_layout = MagicMock()

    class TestWid(QGridLayout):
        def __init__(self):
            super().__init__()

        def get_current_cell_layout(self):
            return get_cc_layout

    editor_view_mock.return_value = TestWid()
    stitching_opt_mock.return_value = QVBoxLayout()
    table_model_mock = MagicMock(
        return_value=PatternDisplayModel([["a", "b"], ["b", "a"]]))
    test_widget = QWidget()
    overlay = PatternDisplayOverlay("Testing", table_model_mock)
    test_widget.setLayout(overlay)

    assert test_widget.layout().count() == 2
    editor_view_mock.assert_called_once_with("Testing",
                                             test_widget.layout().model,
                                             test_widget.layout())
    stitching_opt_mock.assert_called_once_with(get_cc_layout, test_widget.layout())
    opt_menu_layout_widg = test_widget.childAt(0, 1)
    assert opt_menu_layout_widg.maximumSize().width() == 300
