from PyQt6.QtWidgets import QHBoxLayout, QPushButton

import resources.gui_strings as s
from gui.patterns_selector.pattern_selector_dropdown import PatternSelectorDropDownWidget


class PatternSelectorChoiceLayout(QHBoxLayout):
    """ Creates a pattern selector which contains a submit button and a dropdown list of choices.

    +----------------------------------------------------------------+
    |                                            |                   |
    |         DROP DOWN BOX                      |      CHOOSE       |
    |                                            |                   |
    +----------------------------------------------------------------+

    Parameters:
        parent: the parent layout [default None]
        combo_box: controls pattern choice
        submit_button: a button to press to move to the next step.

    Methods:
        __init__(parent)
        on_pattern_choice(): Moves to the next layout with the chosen pattern extracted from the
            combo_box
    """

    parent: 'PatternSelectorLayout'
    combo_box: PatternSelectorDropDownWidget
    submit_button: QPushButton

    def __init__(self, parent: 'PatternSelectorLayout' = None):
        super().__init__()
        self.parent = parent

        # Combo box
        self.combo_box = PatternSelectorDropDownWidget()
        self.addWidget(self.combo_box)

        # Submit button
        self.submit_button = QPushButton(s.pattern_selector_select())
        self.addWidget(self.submit_button)
        self.submit_button.pressed.connect(self.choose_pattern)

    def choose_pattern(self):
        selected_pattern = self.combo_box.selected_pattern
        self.parent.pattern_chosen(selected_pattern)
