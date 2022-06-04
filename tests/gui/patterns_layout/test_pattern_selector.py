from unittest.mock import patch

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector import PatternSelectorLayout


class ParentMock:
    def __init__(self):
        self.called = False

    def pattern_chosen(self, pattern_name):
        self.called = True


@patch("gui.patterns_layout.pattern_selector.PatternSelectorChoiceLayout")
def test_init(child_mock, qtbot):
    child_mock.return_value = QHBoxLayout()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the label
    actual_label = test_widget.layout().title
    assert type(actual_label) == QLabel
    assert actual_label.text() == s.pattern_selector_title()

    assert child_mock.call_count == 1


@patch("gui.patterns_layout.pattern_selector.PatternSelectorChoiceLayout")
def test_pattern_chosen(child_mock, qtbot):
    child_mock.return_value = QHBoxLayout()
    parent_mock = ParentMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout(parent_mock))
    qtbot.addWidget(test_widget)

    assert not parent_mock.called

    test_widget.layout().pattern_chosen(None)
    assert parent_mock.called
