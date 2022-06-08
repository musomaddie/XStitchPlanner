from PyQt6.QtWidgets import QGridLayout

from gui.patterns_view.pattern_display_grid import PatternDisplayGridView, \
    PatternDisplayGridModel


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

    def __init__(self, pattern_name: object, parent: object = None) -> object:
        super().__init__()

        self.pattern_model = PatternDisplayGridModel.load_from_pattern_file(
            pattern_name)
        self.parent = parent

        self.toolbar = None
        self.pattern_grid = PatternDisplayGridView(pattern_name,
                                                   self.pattern_model, self)
        self.so_menu = None

        self.addWidget(self.pattern_grid)
