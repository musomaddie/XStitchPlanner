from PyQt6.QtWidgets import QGridLayout

from gui.stitching.options.corner_selector_button import CornerSelectorButton
from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT


class StartingCornerLayout(QGridLayout):
    """ Contains all the buttons for the different starting corners

    Methods:
        __init__(parent)
        select_corner(selected_button): marks the given corner as the one selected
        deselect_others(selected_button): marks all the other buttons as not selected
    """
    buttons: list[CornerSelectorButton]
    parent: 'StartingCornerOverlay'

    def __init__(self, parent: 'StartingCornerOverlay' = None):
        super().__init__()
        self.parent = parent
        self.buttons = [CornerSelectorButton(TOP_LEFT, self),
                        CornerSelectorButton(TOP_RIGHT, self),
                        CornerSelectorButton(BOTTOM_LEFT, self),
                        CornerSelectorButton(BOTTOM_RIGHT, self)]
        self.addWidget(self.buttons[0], 0, 0)
        self.addWidget(self.buttons[1], 0, 1)
        self.addWidget(self.buttons[2], 1, 0)
        self.addWidget(self.buttons[3], 1, 1)

    def select_corner(self, selected_button: CornerSelectorButton) -> None:
        """ Marks the given corner as the one selected """
        self.parent.select_corner(selected_button)
        self.deselect_others(selected_button)

    def deselect_others(self, selected_button: CornerSelectorButton) -> None:
        """ Marks all buttons as deselected expect the passed button"""
        for button in self.buttons:
            if button != selected_button:
                button.deselect()
