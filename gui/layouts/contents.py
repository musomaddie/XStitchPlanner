from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.layouts.current_page import CurrentPage
from gui.layouts.navigation_drawer import NavigationDrawer


def read_stylesheet():
    with open("styles.qss") as f:
        return f.read()


class ContentsLayout(QHBoxLayout):
    """ Layout for all the contents. """

    def __init__(self):
        super().__init__()
        self.addWidget(NavigationDrawer())
        self.addWidget(CurrentPage())


class Contents(QWidget):
    """ Parent class of all layout contents. Does all the hard work (hopefully). """

    def __init__(self):
        super().__init__()

        self.setLayout(ContentsLayout())
        self.setObjectName("contents")
        self.setStyleSheet(read_stylesheet())
