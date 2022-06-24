from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar

from gui.pattern_display_model import PatternDisplayModel


class PatternViewToolBar(QToolBar):
    """ Contains all the buttons in the view pattern tool bar.

   +-------------------------------------------------------------------+
   |        |       |                                                  |
   | COLOUR | B / W |                                                  |
   |        |       |                                                  |
   +-------------------------------------------------------------------+
    """
    display_overlay: 'PatternDisplayOverlay'
    model: PatternDisplayModel
    colour_on: QAction
    colour_off: QAction

    def __init__(self, model: 'PatternDisplayModel', display_overlay: 'PatternDisplayOverlay'):
        super().__init__()
        self.display_overlay = display_overlay
        self.model = model
        self.setIconSize(QSize(16, 16))

        # TODO: if I also have a menu bar it's going to be hard to access
        #  these icons so reposition this logic if required.
        # TODO: gray out and make un-clickable these icons appropriately (i.e.
        #  if no pattern selected OR already in that view mode).
        self.colour_on = QAction(
            QIcon("resources/gui_icons/color-swatch.png"), "Enable Colour Background")
        self.colour_off = QAction(
            QIcon("resources/gui_icons/gradient.png"), "Disable Colour Background")
        self.addAction(self.colour_on)
        self.addAction(self.colour_off)

        self.colour_on.triggered.connect(lambda: self.change_colour_mode(True))
        self.colour_off.triggered.connect(lambda: self.change_colour_mode(False))

    def change_colour_mode(self, show_colour: bool) -> None:
        """ Used to toggle the change in actions"""
        self.model.set_colour_mode(show_colour)
        self.model.change_pattern_visible_gridlines(not show_colour)
