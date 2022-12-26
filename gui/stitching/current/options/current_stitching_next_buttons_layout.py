from PyQt6.QtWidgets import QHBoxLayout

from gui.stitching.current.options.next_button import NextButton


class CurrentStitchingNextButtonsLayout(QHBoxLayout):
    """Contains all the buttons for moving through the pattern while stitching

    Methods:
        __init__(parent)
    """
    # TODO: allow moving backwards??
    buttons: list[NextButton]

    def __init__(self, parent: 'CurrentStitchingOptionsOverlay' = None):
        super().__init__()
        self.parent = parent
        self.buttons = [NextButton("Next Colour", self), NextButton("Next Row", self)]
        for button in self.buttons:
            self.addWidget(button)
