from PyQt6.QtWidgets import QHBoxLayout

from gui.stitching.current.current_stitching_pattern_model import CurrentStitchingPatternModel
from gui.stitching.current.options.next_button import NextButton
from pattern_cells.stitcher import Stitcher


class CurrentStitchingNextButtonsLayout(QHBoxLayout):
    """Contains all the buttons for moving through the pattern while stitching

    Methods:
        __init__(parent)
    """
    # TODO: allow moving backwards??
    buttons: list[NextButton]

    def __init__(self,
                 stitcher: Stitcher,
                 model: CurrentStitchingPatternModel,
                 parent: 'CurrentStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent
        self.buttons = [NextButton("colour", stitcher, model, self), NextButton("row", stitcher, model, self)]
        for button in self.buttons:
            self.addWidget(button)
