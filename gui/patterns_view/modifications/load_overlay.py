from PyQt6.QtWidgets import QHBoxLayout, QPushButton

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
    variants_dropdown: VariantsLoadDropDown
    load_impl_button: QPushButton

    # TODO: don't show if no pattern modifiers saved!
    # TODO: refresh once something has been saved!

    def __init__(self, pattern_name: str, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.variants_dropdown = VariantsLoadDropDown(pattern_name)
        self.addWidget(self.variants_dropdown)
        self.load_impl_button = QPushButton(s.load_variant())
        self.addWidget(self.load_impl_button)
        self.load_impl_button.pressed.connect(self.load_variant)

    def load_variant(self) -> None:
        """ Loads the selected variant into a new tab. """
        self.parent.create_new_pattern_variant_tab(
            self.variants_dropdown.get_pattern_model_from_selected_variant())
