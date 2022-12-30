from PyQt6.QtWidgets import QPushButton

from stitchers.old_stitcher import OLD_Stitcher


class NextButton(QPushButton):
    """ Parent class for the next buttons that move through the stitcher

    Methods:
        __init__(parent)
    """
    text: str
    parent: 'CurrentStitchingNextButtonsLayout'

    def __init__(self, item_type: str, stitcher: OLD_Stitcher, parent: 'CurrentStitchingNextButtonsLayout' = None):
        """
        Creates a new NextButton instance

        Args:
            stitcher: the stitcher that is used to move throughout this pattern.
            item_type: determines the behaviour of the button as well as the text label.
            parent: the layout containing this button [default: None]
        """
        super().__init__()
        self.setText(f"Next {item_type.title()}")
        self.stitcher = stitcher
        self.parent = parent

    def next_colour_clicked(self):
        """
        Handles the behaviour of the next colour being clicked.

        Returns:
        """
        self.stitcher.stitch_next_colour()
