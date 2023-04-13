from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.stitching.options.starting_corner_overlay import StartingCornerOverlay
from gui.stitching.prepare.stitching_technique_combo_box import StitchingTechniqueComboBox
from stitchers.starting_corner import TOP_LEFT


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
    parent: 'PrepareStitchingViewOverlay'

    def __init__(self, parent: 'PrepareStitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent

        self.starting_corner = StartingCornerOverlay(self)
        starting_corner_layout_widget = QWidget()
        starting_corner_layout_widget.setLayout(self.starting_corner)
        self.addWidget(starting_corner_layout_widget)

        self.stitching_technique = StitchingTechniqueComboBox(self)
        self.addWidget(self.stitching_technique)

        self.start_button = QPushButton(s.start_stitching_button_desc())
        self.start_button.pressed.connect(self.start_stitching)
        self.addWidget(self.start_button)

    def start_stitching(self):
        """ Starts stitching this pattern and changes the layout to reflect this. """
        corner = self.starting_corner.selected_corner  # TODO: move this default to the correct
        # layout
        if not corner:
            corner = TOP_LEFT
        self.parent.start_stitching(corner)
