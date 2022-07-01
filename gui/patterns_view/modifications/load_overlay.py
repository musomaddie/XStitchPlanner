from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QPushButton

import resources.gui_strings as s
from gui.patterns_view.modifications.variants_load_dropdown import VariantsLoadDropDown


class LoadOverlay(QHBoxLayout):
    """
    Handles the overall layout for loading a previously saved configuration. Initially everything is
    compressed into one button which when clicked expands out the layout. (I HOPE)
    +---------------+
    |   LOAD        |
    +---------------+

    Methods:
        __init__()
    """
    parent: 'StitchingOptMenuOverview'
    variants_dropdown: QComboBox
    load_impl_button: QPushButton

    # TODO: don't show if no pattern modifiers saved!

    def __init__(self, pattern_name: str, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.variants_dropdown = VariantsLoadDropDown(pattern_name)
        self.addWidget(self.variants_dropdown)
        self.load_impl_button = QPushButton(s.load_variant())
        self.addWidget(self.load_impl_button)
