from PyQt6.QtWidgets import QGridLayout

from gui.patterns_view.pattern_display_grid import PatternDisplayGridView


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

    Methods:
        __init__(pattern_name)  PatternDisplayOverlay
   """

    def __init__(self, pattern_name, parent=None):
        super().__init__()
        self.parent = parent

        self.toolbar = None
        self.pattern_grid = PatternDisplayGridView(pattern_name, self)
        self.so_menu = None

        self.addWidget(self.pattern_grid)
