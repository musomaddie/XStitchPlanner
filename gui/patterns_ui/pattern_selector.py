from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout

from gui.patterns_ui.pattern_selector_dropdown import find_all_patterns


class PatternSelectorLayout(QVBoxLayout):

    def __init__(self):
        super().__init__()

        # Heading label
        label = QLabel("Hello World this is vbox")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(label)

        # Populate a combo box


