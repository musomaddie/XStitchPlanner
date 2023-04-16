from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from gui.layouts.styled_widget import StyledWidget


class _NavigationDrawerLayout(QHBoxLayout):
    """ Layout for the navigation drawer. This should not be accessed outside this class. """

    def __init__(self):
        super().__init__()

        button = QPushButton("")
        button.setIcon(QIcon("styles/icons/home.svg"))
        button.setIconSize(QSize(24, 24))
        self.addWidget(button)


class NavigationDrawer(StyledWidget):
    """ Drawer to help control navigation (goes on the left). Can open for further details. Always accessible. """

    def __init__(self):
        super().__init__("navigation-drawer")

        self.setLayout(_NavigationDrawerLayout())
        self.setMinimumSize(80, self.minimumSize().height())
        self.setMaximumSize(80, self.maximumSize().height())
