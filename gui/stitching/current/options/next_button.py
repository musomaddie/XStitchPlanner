from PyQt6.QtWidgets import QPushButton


class NextButton(QPushButton):
    # TODO: NOW I think this needs to be an abstract class
    """ Parent class for the next buttons that move through the stitcher

    Methods:
        __init__(parent)
    """
    text: str
    parent: 'CurrentStitchingNextButtonsLayout'

    def __init__(self, text: str, parent: 'CurrentStitchingNextButtonsLayout' = None):
        super().__init__()
        self.setText(text)
        self.parent = parent
