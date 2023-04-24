from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class StyledWidget(QWidget):
    """ A wrapper class for all widgets that I will be applying styling too.

    This handles setting any attribute vaules so that my style changed actually show up.
    """

    def __init__(self, object_name: str):
        """

        Args:
            object_name:  the name used to identify this widget for the style sheet.
        """
        super().__init__()
        self.setObjectName(object_name)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
