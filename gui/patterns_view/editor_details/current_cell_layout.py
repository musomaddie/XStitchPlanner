from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QHBoxLayout, QLabel

import resources.gui_strings as s


class CurrentCellLayout(QHBoxLayout):
    """ Contains the information for the current cell
    +-------------------------------------------------------------------+
    |         title            |      row        |      col             |
    +-------------------------------------------------------------------+

    Methods:
        update_displays()   updates the numbers being displayed
    """
    # TODO: handle selected range somehow nicely
    parent: 'PatternTitleBar'
    title: QLabel
    row_display: QLabel
    col_display: QLabel
    row_value: int
    col_value: int

    def __init__(self, parent: 'PatternTitleBar' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel(s.cell_display_title())
        self.row_value = 0
        self.col_value = 0

        # TODO: make this look pretty!
        self.row_display = QLabel(s.cell_display("row", self.row_value))
        self.col_display = QLabel(s.cell_display("col", self.col_value))

        self.addWidget(self.title)
        self.addWidget(self.row_display)
        self.addWidget(self.col_display)

    def _update_displays(self):
        self.row_display.setText(s.cell_display("row", self.row_value))
        self.col_display.setText(s.cell_display("col", self.col_value))

    def update_values(self, index: QModelIndex) -> None:
        self.row_value = index.row()
        self.col_value = index.column()
        self._update_displays()
