from PyQt6.QtWidgets import QHBoxLayout

from gui.layouts.current_page import CurrentPage
from gui.layouts.navigation_drawer import NavigationDrawer
from gui.layouts.styled_widget import StyledWidget


class _ContentsLayout(QHBoxLayout):
    """ Layout for all the contents. """

    def __init__(self):
        super().__init__()
        self.addWidget(NavigationDrawer())
        self.addWidget(CurrentPage())


class Contents(StyledWidget):
    """ Parent class of all layout contents. Does all the hard work (hopefully). """

    def __init__(self):
        super().__init__("contents")
        self.setLayout(_ContentsLayout())
