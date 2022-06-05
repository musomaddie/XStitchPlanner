from PyQt6.QtWidgets import QVBoxLayout, QLabel

from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


class PatternViewOverviewLayout(QVBoxLayout):
    """ Contains everything for the pattern view

    +-------------------------------------------------------------------+
    |                         PATTERN TITLE                             |
    +-------------------------------------------------------------------+
    |                                                                   |
    |                          PATTERN  DISPLAY                         |
    |                                                                   |
    +-------------------------------------------------------------------+

    Parameters:
        parent              MainWindow              parent layout [default None]
        pattern_title       QLabel                  title of pattern
        pattern_display     PatternDisplayOverlay   contains the detailed
                                                        pattern display

    Methods:
        __init__(pattern_title, parent)         PatternViewOverlayLayout
    """

    def __init__(self, pattern_title, parent=None):
        """ Creates a new PatternViewOverviewLayout

        Parameters:
             pattern_title      str         the title of this pattern
             parent             MainWindow  the parent of this view [default
                                                None]

        """
        super().__init__()
        self.pattern_title = QLabel(pattern_title)
        self.parent = parent

        self.addWidget(self.pattern_title)
        self.addLayout(PatternDisplayOverlay(self))
