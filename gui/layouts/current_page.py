from gui.layouts.choose_pattern import ChoosePattern
from gui.layouts.styled_widget import StyledStackedWidget
from gui.styles.styler import Styler


class CurrentPage(StyledStackedWidget):
    """
    Holds the content of the current page. Sits in between contents and something else - dunno what yet.
    """

    def __init__(self):
        super().__init__("current-page")

        choose_page = ChoosePattern()
        self.addWidget(choose_page)
        self.setCurrentWidget(choose_page)
        self.setStyleSheet(Styler("current_page").get_style())
