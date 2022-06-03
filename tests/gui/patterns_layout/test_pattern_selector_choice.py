from unittest.mock import patch

from PyQt6.QtWidgets import QPushButton, QWidget

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector_choice import \
    PatternSelectorChoiceLayout


@patch(
    "gui.patterns_layout.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_pattern_selector_choice_layout_init(psdl_mock, qtbot):
    psdl_mock.return_value = QWidget()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the button
    button = test_widget.layout().itemAt(1).widget()
    assert type(button) == QPushButton
    assert button.text() == s.pattern_selector_select()

    assert psdl_mock.call_count == 1
