from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar


class PatternViewToolBar(QToolBar):
    # TODO: potentially move where this is located
    """ Contains all the buttons in the view pattern tool bar.

   +-------------------------------------------------------------------+
   |        |       |                                                  |
   | COLOUR | B / W |                                                  |
   |        |       |                                                  |
   +-------------------------------------------------------------------+

    Parameters:
        parent      ViewHierarchy           the parent that this attaches to
        pattern_model  PatternDisplayGridModel the model managing the visible
                                                pattern
        colour_on   CellColourSwitcher      an action that adds a colour
                                                background
        colour_off  CellColourSwitcher      an action that removes a colour
                                                background
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pattern_model = None
        self.setIconSize(QSize(16, 16))

        # TODO: if I also have a menu bar it's going to be hard to access
        #  these icons so fix it in this case
        self.colour_on = QAction(
            QIcon("resources/gui_icons/color-swatch.png"),
            "Enable Colour Background", parent)
        self.colour_off = QAction(
            QIcon("resources/gui_icons/gradient.png"),
            "Disable Colour Background", parent)
        self.addAction(self.colour_on)
        self.addAction(self.colour_off)

    def pattern_chosen(self, pattern_model):
        self.pattern_model = pattern_model
        self.colour_on.triggered.connect(
            lambda: pattern_model.set_colour_mode(True))
        self.colour_off.triggered.connect(
            lambda: pattern_model.set_colour_mode(False))
