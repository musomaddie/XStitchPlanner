from PyQt6.QtWidgets import QGridLayout


class PatternDisplayOverlay(QGridLayout):
    """ Wraps all the different elements required for viewing the pattern.

   +-------------------------------------------------------------------+
   |                            TOOL BAR                               |
   +-------------------------------------------------------------------+
   |                                                    |   STITCHING  |
   |        PATTERN GRID                                |   OPTIONS    |
   |                                                    |   MENU       |
   +-------------------------------------------------------------------+

   Parameters:
       parent           PatternViewOverviewLayout
       toolbar          PatternToolbarOverlay
       pattern_grid     PatternGrid
       so_menu          StitchingOptMenuOverlay
   """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.toolbar = None
        self.pattern_grid = None
        self.so_menu = None
