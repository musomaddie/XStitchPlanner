from PyQt6.QtWidgets import QPushButton

from gui.stitching.current.current_stitching_pattern_model import CurrentStitchingPatternModel
from pattern_cells.stitcher import Stitcher


class NextButton(QPushButton):
    """ Parent class for the next buttons that move through the stitcher

    Methods:
        __init__(parent)
    """
    text: str
    stitcher: Stitcher
    parent: 'CurrentStitchingNextButtonsLayout'

    def __init__(self,
                 item_type: str,
                 stitcher: Stitcher,
                 model: CurrentStitchingPatternModel,
                 parent: 'CurrentStitchingNextButtonsLayout' = None):
        """
        Creates a new NextButton instance

        Args:
            stitcher: the stitcher that is used to move throughout this pattern.
            item_type: determines the behaviour of the button as well as the text label.
            model: the model that is responsible for containing this data (NOTE: I can technically get the stitcher from this.
            parent: the layout containing this button [default: None]
        """
        super().__init__()
        self.setText(f"Next {item_type.title()}")
        self.stitcher = stitcher
        self.model = model
        self.parent = parent
        self.clicked.connect(self.next_colour_clicked)

    def next_colour_clicked(self):
        """
        Handles the behaviour of the next colour being clicked.
        """
        top_left_index, bottom_right_index = self.stitcher.stitch_next_colour()
        self.model.dataChanged.emit(self.model.index(top_left_index[0], top_left_index[1]),
                                    self.model.index(bottom_right_index[0], bottom_right_index[1]))
