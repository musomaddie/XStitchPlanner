from PyQt6.QtWidgets import QLabel, QVBoxLayout


class CurrentStitchingOptionsOverlay(QVBoxLayout):
    """ Contains the overlay for the options' menu for the current stitching
    +---------------+
    |               |
    |               |
    |               |
    |               |
    |               |
    +---------------+

    Methods:
        __init__()
    """
    parent: 'CurrentStitchingViewOverlay'

    def __init__(self, parent: 'CurrentStitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent

        self.addWidget(QLabel("Options menu"))
