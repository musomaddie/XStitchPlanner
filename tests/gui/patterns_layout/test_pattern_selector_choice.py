from unittest.mock import patch

from PyQt6.QtWidgets import QPushButton, QWidget

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector_choice import \
    PatternSelectorChoiceLayout


class psddWidgetMock(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_pattern = "SELECTED"


@patch(
    "gui.patterns_layout.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_pattern_selector_choice_layout_init(psdl_mock, qtbot):
    psdl_mock.return_value = QWidget()
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
    "gui.patterns_layout.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_choose_pattern(psdl_mock, qtbot):
    psdl_mock.return_value = psddWidgetMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().choose_pattern() == "SELECTED"


@patch(
    "gui.patterns_layout.pattern_selector_choice.PatternSelectorDropDownWidget")
def test_choose_pattern_called_on_button_pressed(psdl_mock, qtbot):
    psdl_mock.return_value = psddWidgetMock()
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout())
    qtbot.addWidget(test_widget)

    # Patching the call to choose_pattern so I can confirm whether it's been
    # called.
    # with patch.object(test_widget.layout(), "choose_pattern") as \
    #         choose_pattern_mock:
    #     qtbot.mouseClick(test_widget.layout().submit_button,
    #                      Qt.MouseButton.LeftButton)
    #
    #     print(choose_pattern_mock)
    #     assert choose_pattern_mock.called
