from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.stitching.options.starting_corner_layout import StartingCornerLayout


class StartingCornerOverlay(QVBoxLayout):
    """ Contains a header and grid view to choose the starting corner"""
    header: QLabel
    grid: StartingCornerLayout
    parent: 'PreStitchingOptionsOverlay'

    def __init__(self, parent: 'PreStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent

        # TODO: resize so that the heading is closer to the buttons?
        self.header = QLabel(s.starting_corner_select())
        self.addWidget(self.header)

        self.grid = StartingCornerLayout(self)
        grid_layout_widget = QWidget()
        grid_layout_widget.setLayout(self.grid)
        self.addWidget(grid_layout_widget)
