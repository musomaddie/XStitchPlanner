from PyQt6.QtWidgets import QHBoxLayout, QPushButton

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector_dropdown import \
    PatternSelectorDropDownWidget


class PatternSelectorChoiceLayout(QHBoxLayout):
    """ Creates a pattern selector which contains a submit button and a
    dropdown list of choices.

    +----------------------------------------------------------------+
    |                                            |                   |
    |         DROP DOWN BOX                      |      CHOOSE       |
    |                                            |                   |
    +----------------------------------------------------------------+

    Parameters:
        parent      PatternSelectorLayout           the parent layout
        combo_box   PatternSelectorDropDownWidget   controls pattern choice
        submit_button    QPushButton                a button to press to move to
                                                    the next step.

    Methods:
        __init__(parent)        PatternSelectorChoiceLayout
        on_pattern_choice()     Moves to the next layout with the chosen pattern
                                extracted from the combo_box
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        # Combo box
        self.combo_box = PatternSelectorDropDownWidget()
        self.addWidget(self.combo_box)

        # Submit button
        # Not required to be a class variable but makes testing so much easier
        self.submit_button = QPushButton(s.pattern_selector_select())
        self.addWidget(self.submit_button)
        self.submit_button.pressed.connect(self.choose_pattern)

    def choose_pattern(self):
        # Should actually make and call a new layout (no return value)
        selected_pattern = self.combo_box.selected_pattern
        return self.parent.pattern_chosen(selected_pattern)
