from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from gui.patterns_layout.pattern_selector_choice import \
    PatternSelectorChoiceLayout


class PatternSelectorLayout(QVBoxLayout):
    """ Contains the entire pattern selector layout

    +----------------------------------------------------------------+
    |                                                                |
    |                            TITLE                               |
    |                                                                |
    +----------------------------------------------------------------+
    |                                            |                   |
    |         DROP DOWN BOX                      |      CHOOSE       |
    |                                            |                   |
    +----------------------------------------------------------------+
    """

    def __init__(self):
        super().__init__()

        # Heading label
        label = QLabel(s.pattern_selector_title())
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(label)

        # Populate a combo box
        self.addLayout(PatternSelectorChoiceLayout())
