from PyQt6.QtWidgets import QPushButton

from stitching_technique.starting_corner import StartingCorner


class CornerSelectorButton(QPushButton):
    """ Class for buttons that handle corner selection

    Methods:
        __init__(corner, parent)
        __eq__(other) -> bool
        select(): marks this button (corner) as selected
        deselect(): marks this button (corner) as non selected
    """
    corner: StartingCorner
    parent: 'StartingCornerLayout'

    def __init__(self, corner: StartingCorner, parent: 'StartingCornerLayout' = None):
        super().__init__()
        self.corner = corner
        self.parent = parent

        self.setText(corner.description.title())
        self.setStyleSheet("background-color: gray")

        self.clicked.connect(self.select)

    def __eq__(self, other: 'CornerSelectorButton'):
        return self.corner == other.corner

    def select(self):
        """ Handles the logic for selecting this corner"""
        self.setStyleSheet("background-color: blue")
        self.parent.select_corner(self)

    def deselect(self):
        """ Marks this button as no longer selected """
        self.setStyleSheet("background-color: gray")
