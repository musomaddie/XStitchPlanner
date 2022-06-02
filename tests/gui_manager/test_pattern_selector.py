from PyQt6.QtWidgets import QLabel, QWidget

import resources.gui_strings as s
from gui.patterns_ui.pattern_selector import PatternSelectorLayout


def test_pattern_selector_layout_init(qtbot):
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the label
    actual_label = test_widget.layout().itemAt(0).widget()
    assert type(actual_label) == QLabel
    assert actual_label.text() == s.pattern_selector_title()

    # TODO: tests for the remaining part?
