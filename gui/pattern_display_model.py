import typing

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from pattern_cell import PatternCell
from utils import read_key


class PatternDisplayModel(QAbstractTableModel):
    """ Handles the pattern data for display

    Methods:
        __init__(data)
        data(index, role): displays the data
        rowCount(index): number of rows
        columnCount(index): number of columns
        set_colour_mode(bool): updates the show_colours method
        add_display(display): adds what is being used to display this, so it can be modified as
            necessary
        change_pattern_visible_gridlines(show_gridlines): changes if the gridlines are shown
            when displaying the pattern loaded by this model.

    Static Methods:
        load_from_pattern_file(pattern_name)    PatternDisplayModel
                loads a pattern display grid model from the .pat file with the
                given pattern name

    """
    data: list[list[PatternCell]]
    display: 'PatternDisplayView'
    show_colours: bool

    def __init__(self, data: list[list[PatternCell]]):
        super().__init__()
        self._data = data
        self.show_colours = False
        self.display = None

    def add_display(self, display: 'PatternDisplayView') -> None:
        self.display = display

    def change_pattern_visible_gridlines(self, show_gridlines: bool) -> None:
        # TODO: make this togglable in the settings bar too!
        self.display.setShowGrid(show_gridlines)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.BackgroundRole and self.show_colours:
            return QColor(f"#{self._data[index.row()][index.column()].hex_colour}")
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()].display_symbol

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

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

        # TODO: handle patterns with saved configurations without duplicating the pattern name (?)

        key = {k.symbol: k for k in read_key(f"patterns/{pattern_name}.key")}

        all_rows = []
        with open(f"patterns/{pattern_name}.pat") as f:
            for row_count, row in enumerate(f.readlines()):
                this_row = []
                for col_count, letter in enumerate(row.rstrip()):
                    this_row.append(
                        PatternCell(
                            letter,
                            key[letter].dmc_value,
                            (row_count, col_count),
                            key[letter].hex_colour))
                all_rows.append(this_row)
            return PatternDisplayModel(all_rows)
