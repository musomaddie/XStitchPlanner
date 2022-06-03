from PyQt6.QtWidgets import QHBoxLayout, QPushButton

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector_dropdown import \
    PatternSelectorDropDownLayout


class PatternSelectorChoiceLayout(QHBoxLayout):
    """ Creates a pattern selector which contains a submit button and a
    dropdown list of choices.

    +----------------------------------------------------------------+
    |                                            |                   |
    |         DROP DOWN BOX                      |      CHOOSE       |
    |                                            |                   |
    +----------------------------------------------------------------+
    """

    def __init__(self):
        super().__init__()

        # Combo box
        self.addWidget(PatternSelectorDropDownLayout())

        # Submit button
        self.addWidget(QPushButton(s.pattern_selector_select()))
