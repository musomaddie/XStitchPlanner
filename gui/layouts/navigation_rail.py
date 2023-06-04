from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from gui.layouts.styled_widget import StyledWidget
from gui.styles.styler import MINIMUM_TOUCH_TARGET_SIZE


class _NavigationRailLayout(QHBoxLayout):
    """ Layout for the navigation drawer. This should not be accessed outside this class. """

    def __init__(self):
        super().__init__()

        # TODO: show if we are currently at this button or not.
        button = QPushButton("")
        button.setAutoFillBackground(True)
        button.setIcon(QIcon("gui/styles/icons/home.svg"))
        # TODO: look into setting the below using the style sheet instead.
        button.setIconSize(QSize(24, 24))
        button.setMinimumSize(MINIMUM_TOUCH_TARGET_SIZE)
        self.addWidget(button)


class NavigationRail(StyledWidget):
    """ Drawer to help control navigation (goes on the left). Can open for further details. Always accessible. """

    def __init__(self):
        super().__init__("nav-rail")

        self.setLayout(_NavigationRailLayout())
        # self.setStyleSheet(generate_style_sheet("nav_rail"))
