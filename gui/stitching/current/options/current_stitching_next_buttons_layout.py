from PyQt6.QtWidgets import QHBoxLayout

from gui.stitching.current.options.next_button import NextButton
from stitchers.old_stitcher import OLD_Stitcher


class CurrentStitchingNextButtonsLayout(QHBoxLayout):
    """Contains all the buttons for moving through the pattern while stitching

    Methods:
        __init__(parent)
    """
    # TODO: allow moving backwards??
    buttons: list[NextButton]

    def __init__(self, stitcher: OLD_Stitcher, parent: 'CurrentStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent
        self.buttons = [NextButton("colour", stitcher, self), NextButton("row", stitcher, self)]
        for button in self.buttons:
            self.addWidget(button)
