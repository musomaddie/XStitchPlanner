from PyQt6.QtWidgets import QLabel, QVBoxLayout

from gui.layouts.styled_widget import StyledWidget


class _ChoosePatternLayout(QVBoxLayout):
    """ Layout for choosing the pattern! """

    def __init__(self):
        super().__init__()
        self.addWidget(QLabel("choose pattern"))


class ChoosePattern(StyledWidget):
    """ Handles the layout / stuff for selecting a pattern. """

    def __init__(self):
        super().__init__("choose-pattern")

        self.setLayout(_ChoosePatternLayout())
