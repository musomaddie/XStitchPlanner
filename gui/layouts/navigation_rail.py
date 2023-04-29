from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from gui.layouts.styled_widget import StyledWidget
from gui.styles.styler import MINIMUM_TOUCH_TARGET_SIZE, generate_style_sheet


class _NavigationRailLayout(QHBoxLayout):
    """ Layout for the navigation drawer. This should not be accessed outside this class. """

    def __init__(self):
        super().__init__()

        button = QPushButton("")
        button.setIcon(QIcon("gui/styles/icons/home.svg"))
        button.setIconSize(QSize(24, 24))
        button.setMinimumSize(MINIMUM_TOUCH_TARGET_SIZE)
        self.addWidget(button)


class NavigationRail(StyledWidget):
    """ Drawer to help control navigation (goes on the left). Can open for further details. Always accessible. """

    def __init__(self):
        super().__init__("nav-rail")

        self.setLayout(_NavigationRailLayout())
        self.setStyleSheet(generate_style_sheet("nav_rail"))
        self.setMinimumSize(80, self.minimumSize().height())
        self.setMaximumSize(80, self.maximumSize().height())
