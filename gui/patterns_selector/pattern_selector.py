from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import resources.gui_strings as s
from gui.patterns_selector.pattern_selector_choice import \
    PatternSelectorChoiceLayout


class PatternSelectorLayout(QVBoxLayout):
    """ Contains the entire pattern selector layout

    +----------------------------------------------------------------+
    |                                                                |
    |                            TITLE                               |
    |                                                                |
    +----------------------------------------------------------------+
    |                                            |                   |
    |         DROP DOWN BOX                      |      CHOOSE       |
    |                                            |                   |
    +----------------------------------------------------------------+

    Parameters:
        title       QLabel                          the title of the page
        selector    PatternSelectorChoiceLayout     handles choosing the pattern
        parent      ViewHierarchy                      the parent layout [default
                                                        None].

    Methods:
        __init__()          PatternSelectorLayout
        pattern_chosen(pattern_name)        echos call to its parent
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        # Heading label
        self.title = QLabel(s.pattern_selector_title())
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.title)

        # Populate a combo box and button.
        layout_holder = QWidget()
        self.selector = PatternSelectorChoiceLayout(self)
        layout_holder.setLayout(self.selector)
        self.addWidget(layout_holder)

    def pattern_chosen(self, pattern_name):
        return self.parent.pattern_chosen(pattern_name)
