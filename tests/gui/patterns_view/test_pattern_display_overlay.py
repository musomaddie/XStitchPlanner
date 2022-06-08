from unittest.mock import patch, MagicMock

from PyQt6.QtWidgets import QWidget, QTableView

from gui.patterns_view.pattern_display_grid import PatternDisplayGridModel
from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


@patch("gui.patterns_view.pattern_display_overlay.PatternDisplayGridView")
def test_init(table_view_mock, qtbot):
    table_view_mock.return_value = QTableView()
    table_model_mock = MagicMock(
        return_value=PatternDisplayGridModel([["a", "b"], ["b", "a"]]))
    test_widget = QWidget()
    test_widget.setLayout(PatternDisplayOverlay("Testing", table_model_mock))
    qtbot.addWidget(test_widget)

    table_view_mock.assert_called_once_with("Testing",
                                            test_widget.layout().pattern_model,
                                            test_widget.layout())
    assert test_widget.layout().count() == 1
