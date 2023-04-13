from gui.pattern_model import PatternModel

from pattern_cells.pattern_cell import PatternCell


class PrepareStitchingDisplayModel(PatternModel):
    """ Handles the pattern data for display immediately prior to starting stitching """

    def __init__(self, data: list[list[PatternCell]]):
        super().__init__(data)

        self.show_colours = True
        # TODO: add a toggle for the visible gridlines here!
