from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class CurrentPageLayout(QHBoxLayout):
    """ ???? No idea if this is really the layout I want but I'll figure it out. """

    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Current page contents :)"))


class CurrentPage(QWidget):
    """
    Holds the content of the current page. Sits in between contents and something else - dunno what yet.
    """

    def __init__(self):
        super().__init__()

        self.setLayout(CurrentPageLayout())
