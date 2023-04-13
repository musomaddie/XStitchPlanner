from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from gui.patterns_selector.pattern_selector_choice import PatternSelectorChoiceLayout

import resources.gui_strings as s


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
        title: the title of the page
        selector: handles choosing the pattern to display
        parent: the parent layout [default None].

    Methods:
        __init__()
        pattern_chosen(pattern_name): echoes call to the parent
    """
    title: QLabel
    selector: PatternSelectorChoiceLayout
    parent: 'ViewHierarchy'

    def __init__(self, parent: 'ViewHierarchy' = None):
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

    def pattern_chosen(self, pattern_name: str):
        self.parent.pattern_chosen(pattern_name)
