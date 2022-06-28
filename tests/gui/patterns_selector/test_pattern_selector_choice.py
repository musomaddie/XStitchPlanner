from unittest.mock import MagicMock, call, patch

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from gui.patterns_selector.pattern_selector_choice import PatternSelectorChoiceLayout


class ChildMock(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_pattern = True


class ParentMock(QWidget):
    def __init__(self):
        super().__init__()
        self.called = False

    def pattern_chosen(self, pattern_name):
        self.called = True


FILE_LOC = "gui.patterns_selector.pattern_selector_choice."


@patch(f"{FILE_LOC}PatternSelectorDropDownWidget")
@patch(f"{FILE_LOC}PatternSelectorChoiceLayout.addWidget")
@patch(f"{FILE_LOC}QPushButton")
def test_pattern_selector_choice_layout_init(
        push_button_mock, add_widget_mock, dropdown_mock):
    choice_layout = PatternSelectorChoiceLayout()

    push_button_mock.assert_called_once_with("Select this pattern")
    add_widget_mock.assert_has_calls(
        [call(dropdown_mock.return_value), call(push_button_mock.return_value)])

    assert choice_layout.combo_box == dropdown_mock.return_value
    assert choice_layout.submit_button == push_button_mock.return_value


@patch(f"{FILE_LOC}PatternSelectorDropDownWidget")
@patch(f"{FILE_LOC}PatternSelectorChoiceLayout.addWidget")
@patch(f"{FILE_LOC}QPushButton")
def test_choose_pattern(push_button_mock, add_widget_mock, dropdown_mock):
    parent_mock = MagicMock()
    choice_layout = PatternSelectorChoiceLayout(parent_mock)

    choice_layout.choose_pattern()
    parent_mock.assert_has_calls(dropdown_mock.selected_pattern.return_value)


@patch(f"{FILE_LOC}PatternSelectorDropDownWidget")
def test_choose_pattern_called_on_button_pressed(dropdown_mock, qtbot):
    dropdown_mock.return_value = ChildMock()
    parent_mock = ParentMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout(parent_mock))

    qtbot.addWidget(test_widget)

    assert not parent_mock.called

    qtbot.mouseClick(test_widget.layout().submit_button, Qt.MouseButton.LeftButton)

    assert parent_mock.called
