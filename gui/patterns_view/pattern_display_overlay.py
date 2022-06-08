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
       pattern_model    PatternDisplayGridModel
       toolbar          PatternToolbarOverlay
       pattern_grid     PatternDisplayGridView
       so_menu          StitchingOptMenuOverlay

    Methods:
        __init__(pattern_name)  PatternDisplayOverlay
   """

    def __init__(self, pattern_name, pattern_model, parent=None):
        super().__init__()

        self.pattern_model = pattern_model
        self.parent = parent

        self.toolbar = None
        self.pattern_grid = PatternDisplayGridView(pattern_name,
                                                   self.pattern_model, self)
        self.so_menu = None

        self.addWidget(self.pattern_grid)
