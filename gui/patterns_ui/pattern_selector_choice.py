from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from gui.patterns_ui.pattern_selector_dropdown import \
    PatternSelectorDropDownLayout

import resources.gui_strings as s


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
