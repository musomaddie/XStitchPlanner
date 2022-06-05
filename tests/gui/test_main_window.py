from unittest.mock import patch

from PyQt6.QtWidgets import QVBoxLayout

import resources.gui_strings as s
from gui.main_window import MainWindow


@patch("gui.main_window.PatternSelectorLayout")
def test_init(layout_child_mock, qtbot):
    layout_child_mock.return_value = QVBoxLayout()
    test_widget = MainWindow(True)
    qtbot.addWidget(test_widget)

    assert test_widget.windowTitle() == s.program_title()
    assert test_widget.layout().count() == 2

    layout_child_mock.assert_called_once_with(test_widget)
    assert test_widget.currentIndex() == 0


@patch("gui.main_window.PatternSelectorLayout")
@patch("gui.main_window.PatternViewOverviewLayout")
def test_pattern_chosen(view_child_mock, layout_child_mock, qtbot):
    layout_child_mock.return_value = QVBoxLayout()
    view_child_mock.return_value = QVBoxLayout()
    test_widget = MainWindow(True)
    qtbot.addWidget(test_widget)
    test_widget.pattern_chosen("Testing")

    view_child_mock.assert_called_once_with("Testing", test_widget)
    assert test_widget.currentIndex() == 1
