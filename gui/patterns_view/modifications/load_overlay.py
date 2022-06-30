from PyQt6.QtWidgets import QPushButton, QVBoxLayout

import resources.gui_strings as s


class LoadOverlay(QVBoxLayout):
    """
    Handles the overall layout for loading a previously saved configuration. Initially everything is
    compressed into one button which when clicked expands out the layout. (I HOPE)
    +---------------+
    |   LOAD        |
    +---------------+
    """
    parent: 'StitchingOptMenuOverview'
    load_show_options: QPushButton

    def __init__(self, parent: 'StitchingOptMenuOverview' = None):
        super().__init__()
        self.parent = parent

        self.load_show_options = QPushButton(s.load_variants_show_desc())
        self.addWidget(self.load_show_options)
