from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.stitching.options.starting_corner_overlay import StartingCornerOverlay
from gui.stitching.prepare.stitching_technique_combo_box import StitchingTechniqueComboBox


class PreStitchingOptionsOverlay(QVBoxLayout):
    """ Contains the options overlay for pre stitching. Details update dynamically based on
    selections
    +---------------+
    |starting corner|
    +---------------+
    |  stitching    |
    |  tech         |
    +---------------+
    |  STITCH!!     |
    +---------------+
    """
    starting_corner: StartingCornerOverlay
    stitching_technique: StitchingTechniqueComboBox
    start_button: QPushButton
    parent: 'StitchingViewOverlay'

    def __init__(self, parent: 'StitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent

        self.starting_corner = StartingCornerOverlay(self)
        starting_corner_layout_widget = QWidget()
        starting_corner_layout_widget.setLayout(self.starting_corner)
        self.addWidget(starting_corner_layout_widget)

        self.stitching_technique = StitchingTechniqueComboBox(self)
        self.addWidget(self.stitching_technique)

        self.start_button = QPushButton(s.start_stitching_button_desc())
        self.addWidget(self.start_button)
