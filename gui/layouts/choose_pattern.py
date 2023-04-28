from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel, QComboBox, QHBoxLayout

from gui.layouts.styled_widget import StyledWidget


class ChoosePatternDropdown(QComboBox):

    def __init__(self):
        super().__init__()
        self.setObjectName("pattern-dropdown")
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.addItem("Item 1")
        self.addItem("Item 2")
        # TODO - width (more dynamic)
        self.setMaximumSize(QSize(200, self.maximumSize().height()))


class _ChoosePatternLayout(QHBoxLayout):
    """ Layout for choosing the pattern!

    We need a ~dropdown box~ LIST (m3) with a list of pattern names, and a button to load the selected one.

    """

    def __init__(self):
        super().__init__()
        title_label = QLabel("Select a pattern to load:")
        dropdown = ChoosePatternDropdown()
        self.addWidget(title_label)
        self.addWidget(dropdown)


class ChoosePattern(StyledWidget):
    """ Handles the layout / stuff for selecting a pattern. """

    def __init__(self):
        super().__init__("choose-pattern")
        self.setLayout(_ChoosePatternLayout())
        self.setMaximumSize(QSize(500, self.maximumSize().height()))
