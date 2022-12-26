from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from gui.stitching.current.options.current_stitching_next_buttons_layout import \
    CurrentStitchingNextButtonsLayout


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
    next_buttons: CurrentStitchingNextButtonsLayout

    def __init__(self, parent: 'CurrentStitchingViewOverlay' = None):
        super().__init__()
        self.parent = parent

        self.addWidget(QLabel("Options menu"))
        self.next_buttons = CurrentStitchingNextButtonsLayout(self)
        next_buttons_layout_widget = QWidget()
        next_buttons_layout_widget.setLayout(self.next_buttons)
        self.addWidget(next_buttons_layout_widget)
