from unittest.mock import patch

from PyQt6.QtWidgets import QWidget, QTableView

from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


@patch("gui.patterns_view.pattern_display_overlay.PatternDisplayGridView")
def test_init(child_mock, qtbot):
    child_mock.return_value = QTableView()
    test_widget = QWidget()
    test_widget.setLayout(PatternDisplayOverlay("Testing"))
    qtbot.addWidget(test_widget)

    child_mock.assert_called_once_with("Testing", test_widget.layout())
    assert test_widget.layout().count() == 1
