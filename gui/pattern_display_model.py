from gui.pattern_model import PatternModel
from pattern_cells.pattern_cell import PatternCell
from utils import load_from_pattern_file


class PatternDisplayModel(PatternModel):
    """ Handles the pattern data for display

    Methods:
        set_colour_mode(bool): updates the show_colours method
        change_pattern_visible_gridlines(show_gridlines): changes if the gridlines are shown
            when displaying the pattern loaded by this model.

    Static Methods:
        load_from_pattern_file(pattern_name)    PatternDisplayModel
                loads a pattern display grid model from the .pat file with the
                given pattern name

    """

    def __init__(self, data: list[list[PatternCell]]):
        super().__init__(data)

    def change_pattern_visible_gridlines(self, show_gridlines: bool) -> None:
        # TODO: make this togglable in the settings bar too!
        self.display.setShowGrid(show_gridlines)

    def set_colour_mode(self, mode: bool):
        """Changes whether the data is shown in colour"""
        self.show_colours = mode
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(), self.columnCount()))

    @staticmethod
    def load_from_pattern_file(pattern_name: str) -> 'PatternDisplayModel':
        """ Returns a PatternDisplayModel containing a data loaded from the
        .pat file of the given pattern.

        Args:
            pattern_name: the name of the pattern to load

        Returns:
            PatternDisplayModel: with the given pattern loaded as data

        Raises:
            FileNotFoundError: if the given pattern does not have a corresponding file name. This
                should never be reached as it MUST have a .pat file to be selected from the pattern
                selector
        """
        patterns_rows = load_from_pattern_file(pattern_name, pattern_name)
        return PatternDisplayModel(patterns_rows)
