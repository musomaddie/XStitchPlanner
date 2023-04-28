from unittest.mock import MagicMock, call, patch

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from calleee import InstanceOf
from gui.patterns_selector.pattern_selector import PatternSelectorLayout

FILE_LOC = "old_gui.patterns_selector.pattern_selector"


class ParentMock:
    def __init__(self):
        self.called = False

    def pattern_chosen(self, pattern_name):
        self.called = True


@patch(f"{FILE_LOC}.PatternSelectorChoiceLayout")
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.PatternSelectorLayout.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
def test_init(set_layout_mock, add_widget_mock, qlabel_mock, child_mock):
    selector_layout = PatternSelectorLayout()

    assert selector_layout.title == qlabel_mock.return_value
    assert selector_layout.selector == child_mock.return_value

    child_mock.assert_called_once_with(selector_layout)
    qlabel_mock.assert_has_calls(
        [call("Select the pattern to view"), call().setAlignment(Qt.AlignmentFlag.AlignCenter)])
    add_widget_mock.assert_has_calls(
        [call(qlabel_mock.return_value), call(InstanceOf(QWidget))])
    set_layout_mock.assert_called_once_with(child_mock.return_value)


@patch(f"{FILE_LOC}.PatternSelectorChoiceLayout")
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.PatternSelectorLayout.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
def test_pattern_chosen(set_layout_mock, add_widget_mock, qlabel_mock, child_mock):
    parent_mock = MagicMock()
    selector_layout = PatternSelectorLayout(parent_mock)
    assert not parent_mock.called

    pattern_name = "TESTING"
    selector_layout.pattern_chosen(pattern_name)
    parent_mock.assert_has_calls([call.pattern_chosen(pattern_name)])
