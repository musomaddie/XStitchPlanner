from PyQt6.QtWidgets import QPushButton, QWidget

from gui.patterns_ui.pattern_selector_choice import PatternSelectorChoiceLayout
import resources.gui_strings as s


def test_pattern_selector_choice_layout_init(qtbot):
    test_widget = QWidget()
    test_widget.setLayout(PatternSelectorChoiceLayout())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    # Testing the button
    button = test_widget.layout().itemAt(1).widget()
    assert type(button) == QPushButton
    assert button.text() == s.pattern_selector_select()
