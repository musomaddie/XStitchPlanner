from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.stitching.options.corner_selector_button import CornerSelectorButton
from gui.stitching.options.starting_corner_layout import StartingCornerLayout
from stitchers.starting_corner import StartingCorner


class StartingCornerOverlay(QVBoxLayout):
    """ Contains a header and grid view to choose the starting corner

    Methods:
        __init__(parent)
        select_corner(selected_button): marks the given corner as the one selected
    """
    header: QLabel
    grid: StartingCornerLayout
    selected_corner: StartingCorner
    parent: 'PreStitchingOptionsOverlay'

    def __init__(self, parent: 'PreStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent
        self.selected_corner = None

        # TODO: resize so that the heading is closer to the buttons?
        self.header = QLabel(s.starting_corner_select())
        self.addWidget(self.header)

        self.grid = StartingCornerLayout(self)
        grid_layout_widget = QWidget()
        grid_layout_widget.setLayout(self.grid)
        self.addWidget(grid_layout_widget)

    def select_corner(self, selected_button: CornerSelectorButton) -> None:
        """ Marks the given corner as the place to start """
        self.selected_corner = selected_button.corner
