from unittest.mock import patch

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

import resources.gui_strings as s
from gui.patterns_selector.pattern_selector import PatternSelectorLayout

FILE_LOC = "gui.patterns_selector.pattern_selector"


class ParentMock:
    def __init__(self):
        self.called = False

    def pattern_chosen(self, pattern_name):
        self.called = True


@patch(f"{FILE_LOC}.PatternSelectorChoiceLayout")
def test_init(child_mock):
    child_mock.return_value = QHBoxLayout()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout())

    assert test_widget.layout().count() == 2

    # Testing the label
    actual_label = test_widget.layout().title
    assert type(actual_label) == QLabel
    assert actual_label.text() == s.pattern_selector_title()

    assert child_mock.call_count == 1


@patch(f"{FILE_LOC}.PatternSelectorChoiceLayout")
def test_pattern_chosen(child_mock):
    child_mock.return_value = QHBoxLayout()
    parent_mock = ParentMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorLayout(parent_mock))

    assert not parent_mock.called

    test_widget.layout().pattern_chosen(None)
    assert parent_mock.called
