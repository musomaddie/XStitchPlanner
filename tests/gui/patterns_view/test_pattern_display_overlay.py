from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay

FILE_LOC = "gui.patterns_view.pattern_display_overlay"


@patch(f"{FILE_LOC}.PatternEditorView")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview")
def test_init(stitching_opt_mock, editor_view_mock, qtbot):
    editor_view_mock.return_value = QGridLayout()
    stitching_opt_mock.return_value = QVBoxLayout()
    table_model_mock = MagicMock(
        return_value=PatternDisplayModel([["a", "b"], ["b", "a"]]))
    test_widget = QWidget()
    test_widget.setLayout(PatternDisplayOverlay("Testing", table_model_mock))
    qtbot.addWidget(test_widget)

    editor_view_mock.assert_called_once_with("Testing",
                                             test_widget.layout().model,
                                             test_widget.layout())
    # stitching_opt_mock.assert_called_once_with(test_widget.layout())

    assert test_widget.layout().count() == 1
    # assert test_widget.layout().count() == 2
