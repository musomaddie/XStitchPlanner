from PyQt6.QtWidgets import QHBoxLayout, QLabel

from gui.layouts.styled_widget import StyledWidget


class _CurrentPageLayout(QHBoxLayout):
    """ ???? No idea if this is really the layout I want but I'll figure it out. """

    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Current page contents :)"))


class CurrentPage(StyledWidget):
    """
    Holds the content of the current page. Sits in between contents and something else - dunno what yet.
    """

    def __init__(self):
        super().__init__("page")

        self.setLayout(_CurrentPageLayout())
