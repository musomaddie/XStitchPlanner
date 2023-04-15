from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class NavigationDrawerLayout(QHBoxLayout):
    """ Layout for the navigation drawer. This should not be accessed outside this class. """

    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("nav drawer "))


class NavigationDrawer(QWidget):
    """ Drawer to help control navigation (goes on the left). Can open for further details. Always accessible. """

    def __init__(self):
        super().__init__()

        self.setLayout(NavigationDrawerLayout())
        #
        # self.setMinimumSize(300, self.minimumSize().height())
        # self.setMaximumSize(300, self.maximumSize().height())
