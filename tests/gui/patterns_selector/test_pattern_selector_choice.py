from unittest.mock import patch

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget

import resources.gui_strings as s
from gui.patterns_selector.pattern_selector_choice import \
    PatternSelectorChoiceLayout


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


@patch(
    "gui.patterns_selector.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_pattern_selector_choice_layout_init(psdl_mock, qtbot):
    psdl_mock.return_value = ChildMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the button
    button = test_widget.layout().submit_button
    assert type(button) == QPushButton
    assert button.text() == s.pattern_selector_select()

    assert psdl_mock.call_count == 1


@patch(
    "gui.patterns_selector.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_choose_pattern(psdl_mock, qtbot):
    psdl_mock.return_value = ChildMock()
    parent_mock = ParentMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout(parent_mock))
    qtbot.addWidget(test_widget)

    assert not parent_mock.called

    test_widget.layout().choose_pattern()

    assert parent_mock.called


@patch(
    "gui.patterns_selector.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_choose_pattern_called_on_button_pressed(psdl_mock, qtbot):
    psdl_mock.return_value = ChildMock()
    parent_mock = ParentMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout(parent_mock))

    qtbot.addWidget(test_widget)

    assert not parent_mock.called

    qtbot.mouseClick(test_widget.layout().submit_button,
                     Qt.MouseButton.LeftButton)

    assert parent_mock.called
