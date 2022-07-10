from PyQt6.QtWidgets import QGridLayout

from gui.stitching.options.corner_selector_button import CornerSelectorButton
from stitching_technique.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT


class StartingCornerLayout(QGridLayout):
    """ Contains all the buttons for the different starting corners """
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

    def deselect_others(self, selected_button: CornerSelectorButton):
        """ Marks all buttons as deselected expect the passed button"""
        for button in self.buttons:
            if button != selected_button:
                button.deselect()
