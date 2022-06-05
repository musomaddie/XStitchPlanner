from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QTableView


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
        self.data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self.data[0])

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

        with open(f"resources/{pattern_name}.pat") as f:
            return PatternDisplayGridModel(
                [[letter for letter in row.rstrip()]
                 for row in f.readlines()]
            )


class PatternDisplayGridView(QTableView):
    pass
