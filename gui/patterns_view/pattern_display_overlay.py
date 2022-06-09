from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.patterns_view.pattern_display_grid import PatternDisplayGridView
from gui.patterns_view.stitching_opt_menu_overview import (
    StitchingOptMenuOverview)


class PatternDisplayOverlay(QHBoxLayout):
    """ Wraps all the different elements required for viewing the pattern.

   +-------------------------------------------------------------------+
   |                                                    |   STITCHING  |
   |        PATTERN GRID                                |   OPTIONS    |
   |                                                    |   MENU       |
   +-------------------------------------------------------------------+

   Parameters:
       parent (PatternViewOverviewLayout)
       pattern_model (PatternDisplayModel)
       pattern_grid (PatternDisplayGridView)
       so_menu (StitchingOptMenuOverlay)

    Methods:
        __init__(pattern_name)  PatternDisplayOverlay
   """

    def __init__(
            self,
            pattern_name: str,
            pattern_model: 'PatternDisplayModel',
            parent: 'PatternViewOverviewLayout' = None):
        super().__init__()

        self.pattern_model = pattern_model
        self.parent = parent
        self.pattern_grid = PatternDisplayGridView(pattern_name,
                                                   self.pattern_model, self)
        self.so_menu = StitchingOptMenuOverview(self)
        opt_menu_layout_widget = QWidget()
        opt_menu_layout_widget.setLayout(self.so_menu)
        self.addWidget(self.pattern_grid)
        self.addWidget(opt_menu_layout_widget)
