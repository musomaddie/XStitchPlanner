from unittest.mock import patch

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

import resources.gui_strings as s
from gui.patterns_ui.pattern_selector import PatternSelectorLayout


@patch("gui.patterns_ui.pattern_selector.PatternSelectorChoiceLayout")
def test_pattern_selector_layout_init(pscl_mock, qtbot):
    pscl_mock.return_value = QHBoxLayout()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the label
    actual_label = test_widget.layout().itemAt(0).widget()
    assert type(actual_label) == QLabel
    assert actual_label.text() == s.pattern_selector_title()

    assert pscl_mock.call_count == 1
