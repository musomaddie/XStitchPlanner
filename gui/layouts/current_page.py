from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStackedWidget

from gui.layouts.choose_pattern import ChoosePattern


class CurrentPage(QStackedWidget):
    """
    Holds the content of the current page. Sits in between contents and something else - dunno what yet.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName("page")
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        choose_page = ChoosePattern()
        self.addWidget(choose_page)
        self.setCurrentWidget(choose_page)
