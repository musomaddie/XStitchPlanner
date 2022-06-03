from unittest.mock import patch

from PyQt6.QtWidgets import QVBoxLayout

import resources.gui_strings as s
from gui.main_window import MainWindow


@patch("gui.main_window.PatternSelectorLayout")
def test_init(child_mock, qtbot):
    child_mock.return_value = QVBoxLayout()
    test_window = MainWindow(True)

    qtbot.addWidget(test_window)

    print(test_window)
    assert test_window.windowTitle() == s.program_title()
    assert child_mock.call_count == 1
