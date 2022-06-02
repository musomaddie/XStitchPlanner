from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout

import resources.gui_strings as s
from gui.patterns_ui.pattern_selector_dropdown import (
    PatternSelectorDropDownLayout)


class PatternSelectorLayout(QVBoxLayout):

    def __init__(self):
        super().__init__()

        # Heading label
        label = QLabel(s.pattern_selector_title())
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(label)

        # Populate a combo box
        self.addWidget(PatternSelectorDropDownLayout())
