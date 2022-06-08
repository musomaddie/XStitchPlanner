from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget

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
        parent              ViewHierarchy              parent layout [default None]
        pattern_title       QLabel                  title of pattern
        pattern_display     PatternDisplayOverlay   contains the detailed
                                                        pattern display

    Methods:
        __init__(pattern_title, parent)         PatternViewOverlayLayout
    """

    def __init__(self, pattern_title, pattern_model, parent=None):
        """ Creates a new PatternViewOverviewLayout

        Parameters:
             pattern_title      str         the title of this pattern
             parent             ViewHierarchy  the parent of this view [default
                                                None]

        """
        super().__init__()

        self.parent = parent
        self.pattern_model = pattern_model
        self.pattern_title = QLabel(pattern_title)
        self.addWidget(self.pattern_title)

        self.overlay = PatternDisplayOverlay(pattern_title, pattern_model, self)
        layout_widget = QWidget()
        layout_widget.setLayout(self.overlay)
        self.addWidget(layout_widget)
