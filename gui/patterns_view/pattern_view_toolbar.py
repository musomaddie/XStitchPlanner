from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar

from gui.pattern_display_model import PatternDisplayModel
from gui.view_hierarchy import ViewHierarchy


class PatternViewToolBar(QToolBar):
    """ Contains all the buttons in the view pattern tool bar.

   +-------------------------------------------------------------------+
   |        |       |                                                  |
   | COLOUR | B / W |                                                  |
   |        |       |                                                  |
   +-------------------------------------------------------------------+

    Parameters:
        parent (ViewHierarchy): the parent that this attaches to
        pattern_model (PatternDisplayModel): the model managing the visible
            pattern
        colour_on (CellColourSwitcher): an action that adds a colour background
        colour_off (CellColourSwitcher): an action that removes a colour
            background
    """

    def __init__(self, parent: ViewHierarchy = None):
        super().__init__(parent)
        self.parent = parent
        self.pattern_model = None
        self.setIconSize(QSize(16, 16))

        # TODO: if I also have a menu bar it's going to be hard to access
        #  these icons so reposition this logic if required.
        # TODO: gray out and make un-clickable these icons appropriately (i.e.
        #  if no pattern selected OR already in that view mode).
        self.colour_on = QAction(
            QIcon("resources/gui_icons/color-swatch.png"),
            "Enable Colour Background", parent)
        self.colour_off = QAction(
            QIcon("resources/gui_icons/gradient.png"),
            "Disable Colour Background", parent)
        self.addAction(self.colour_on)
        self.addAction(self.colour_off)

    def pattern_chosen(self, pattern_model: PatternDisplayModel) -> None:
        self.pattern_model = pattern_model
        self.colour_on.triggered.connect(
            lambda: pattern_model.set_colour_mode(True))
        self.colour_off.triggered.connect(
            lambda: pattern_model.set_colour_mode(False))
