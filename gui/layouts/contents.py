from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.layouts.current_page import CurrentPage
from gui.layouts.navigation_drawer import NavigationDrawer


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
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(open("styles/global_styles.qss").read())
        # self.setStyleSheet(open("styles/layout/contents.qss").read())
