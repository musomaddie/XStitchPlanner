from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableView, QHeaderView

from pattern_cell import PatternCell
from utils import read_key


class PatternDisplayGridModel(QAbstractTableModel):
    """ Handles the pattern data for display

    Parameters:
        data    list[list[str]]     the pattern data

    Methods:
        __init__(data)  PatternDisplayGridModel

    Static Methods:
        load_from_pattern_file(pattern_name)    PatternDisplayGridModel
                loads a pattern display grid model from the .pat file with the
                given pattern name

    """

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(
                f"#{self._data[index.row()][index.column()].hex_colour}")
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()].display_symbol

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    @staticmethod
    def load_from_pattern_file(pattern_name):
        """ Returns a PatternDisplayGridModel containing a data loaded from the
        .pat file of the given pattern.

        Args:
            pattern_name    str     the name of the pattern to load

        Returns:
            PatternDisplayGridModel     with the given pattern loaded as data

        Raises:
            FileNotFoundError   if the given pattern does not have a
                                    corresponding file name. This should never
                                    be reached as it MUST have a .pat file to be
                                    selected from the pattern selector
        """

        key = {k.symbol: k for k in read_key(f"patterns/{pattern_name}.key")}

        all_rows = []
        with open(f"patterns/{pattern_name}.pat") as f:
            for row_count, row in enumerate(f.readlines()):
                this_row = []
                for col_count, letter in enumerate(row.rstrip()):
                    this_row.append(PatternCell(letter,
                                                key[letter].dmc_value,
                                                (row_count, col_count),
                                                key[letter].hex_colour))
                all_rows.append(this_row)
            return PatternDisplayGridModel(all_rows)


class PatternDisplayGridView(QTableView):
    """ Responsible for actually displaying the pattern in a table form.

    Parameters:
        parent  PatternDisplayOverlay
        model   PatternDisplayGridModel     the model managing this table

    Methods:
        __init__(pattern_name)  PatternDisplayGridView
    """

    def __init__(self, pattern_name, parent=None):
        super().__init__()

        self.parent = parent
        self.model = PatternDisplayGridModel.load_from_pattern_file(
            pattern_name)

        self.setModel(self.model)

        # Using ResizeMode.Fixed to control the size of the cells as using a
        # more dynamic resize caused the program to take a long time loading
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setDefaultSectionSize(10)
        self.verticalHeader().setDefaultSectionSize(10)
