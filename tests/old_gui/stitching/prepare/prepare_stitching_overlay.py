from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from gui.stitching.prepare.prepare_stitching_view_overlay import PrepareStitchingViewOverlay


class PrepareStitchingOverlay(QVBoxLayout):
    """ The overlay containing the display for the stitching technique.

    +-------------------------------------------------------------------+
    |                            TITLE                                  |
    |   pattern view          tech config(adds to pattern view)         |
    +-------------------------------------------------------------------+
    """
    title: QLabel
    view: PrepareStitchingViewOverlay
    parent: 'ViewHierarchy'

    def __init__(
            self,
            title: str,
            model: 'PrepareStitchingDisplayModel',
            parent: 'ViewHierarchy' = None):
        super().__init__()
        self.parent = parent

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.title)

        self.view = PrepareStitchingViewOverlay(model, self)
        view_layout_widget = QWidget()
        view_layout_widget.setLayout(self.view)
        self.addWidget(view_layout_widget)
