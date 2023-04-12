import csv
import sys

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QPushButton, QTableView,
    QVBoxLayout, QWidget)

from floss_thread import Thread
from pattern_cells.pattern_cell import PatternCell

""" TODO / Random note: when reworking architecture make all layouts return widgets instead for an easier time. """

PATTERN_NAME = "patterns/disney-testing-copy"


class DisplayModel(QAbstractTableModel):

    def __init__(self, data: list[list[PatternCell]]):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> int:
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(f"#{self._data[index.row()][index.column()].hex_colour}")
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignHCenter + Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()].display_symbol


class TableView(QTableView):
    def __init__(self, model, current_cell):
        super().__init__()
        self.model = model
        self.setModel(self.model)
        self.clicked.connect(current_cell.update_value)

        # View configs.
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setMinimumSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(20)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setMinimumSectionSize(20)
        self.verticalHeader().setDefaultSectionSize(20)

        current_font = self.font()
        current_font.setPointSize(8)
        self.horizontalHeader().setFont(current_font)
        self.verticalHeader().setFont(current_font)


class CurrentCellLayout(QVBoxLayout):
    """ TODO: neaten this please!! """

    def __init__(self):
        super().__init__()
        self.addWidget(QLabel("Current cell"))
        self.row_value = 0
        self.column_value = 0

        self.display = QLabel(f"({self.row_value + 1}, {self.column_value + 1})")
        self.addWidget(self.display)

    def _update_display(self):
        self.display.setText(f"({self.row_value + 1}, {self.column_value + 1})")

    def get_current_value(self):
        return self.row_value, self.column_value

    def update_value(self, index: QModelIndex):
        self.row_value = index.row()
        self.column_value = index.column()
        self._update_display()


class OptionsView(QVBoxLayout):
    def __init__(self, current_cell):
        super().__init__()
        # Setting up information for rect limiter.
        # Include information about the current cell here too.
        self.current_cell = current_cell
        cc_widget = QWidget()
        cc_widget.setLayout(current_cell)
        self.addWidget(cc_widget)
        self.addWidget(QLabel("Remove Areas by Rectangle"))
        self.addWidget(QPushButton("I am a button!"))
        self.edge_values = [0, 0, 0, 0]
        self.corner_labels = [QLabel("(0, 0)") for _ in range(4)]

        # Add the label widgets!!
        rect_values_grid_layout = QGridLayout()
        rect_values_grid_layout.addWidget(self.corner_labels[0], 0, 0)
        rect_values_grid_layout.addWidget(self.corner_labels[1], 0, 1)
        rect_values_grid_layout.addWidget(self.corner_labels[2], 1, 0)
        rect_values_grid_layout.addWidget(self.corner_labels[3], 1, 1)
        self.addWidget(QLabel("Current selected values: "))
        values_grid_widget = QWidget()
        values_grid_widget.setLayout(rect_values_grid_layout)
        self.addWidget(values_grid_widget)
        self.updater_grid = QGridLayout()
        self.add_buttons()
        grid_widget = QWidget()
        grid_widget.setLayout(self.updater_grid)
        self.addWidget(grid_widget)

        # Add value controller.

    def add_buttons(self):
        def create_button(layout, index):
            label = QLabel("")
            button = QPushButton("Update")
            button.clicked.connect(lambda: self.update_button(index, label))
            layout.addWidget(label)
            layout.addWidget(button)
            w = QWidget()
            w.setLayout(layout)
            return w

        top = create_button(QHBoxLayout(), 0)
        left = create_button(QVBoxLayout(), 1)
        right = create_button(QVBoxLayout(), 2)
        bottom = create_button(QHBoxLayout(), 3)
        self.updater_grid.addWidget(top, 0, 2)
        self.updater_grid.addWidget(left, 2, 0)
        self.updater_grid.addWidget(right, 2, 4)
        self.updater_grid.addWidget(bottom, 4, 2)

        # LEFT
        update_right = QVBoxLayout()

    def update_button(self, edge_idx, label):
        # Get the value and update things
        current_row, current_column = self.current_cell.get_current_value()
        new_value = current_row if edge_idx == 0 or edge_idx == 2 else current_column
        # Replace the line edit, and the corresponding label text.
        label.setText(str(new_value + 1))
        self.edge_values[edge_idx] = new_value
        current_row, current_column = self.corner_labels[edge_idx].text().split(", ")
        if edge_idx == 0 or edge_idx == 2:
            current_row = f"({new_value + 1}"
        else:
            current_column = f"{new_value + 1})"
        self.corner_labels[edge_idx].setText(f"{current_row}, {current_column}")

        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    def corner_str(self, corner_idx):
        return f"({self.corner_values[corner_idx][0] + 1}, {self.corner_values[corner_idx][1] + 1})"


class TableAndMenuView(QHBoxLayout):
    """ Contains the pattern and a right options menu. """

    def __init__(self):
        # Read key
        super().__init__()
        current_cell = CurrentCellLayout()
        self.key = {k.symbol: k for k in read_key()}
        self.pattern = read_pattern_rows(self.key)
        self.model = DisplayModel(self.pattern)
        self.view = TableView(self.model, current_cell)
        self.options_layout = OptionsView(current_cell)

        self.addWidget(self.view)
        options_widget = QWidget()
        options_widget.setMaximumSize(QSize(300, options_widget.maximumSize().height()))
        options_widget.setLayout(self.options_layout)
        self.addWidget(options_widget)


def read_key():
    with open(f"{PATTERN_NAME}.key", encoding="utf-8") as key_file:
        reader = csv.reader(key_file, delimiter="\t")
        return [Thread(row[0], row[1], row[2], row[3], row[4]) for row in reader]


def read_pattern_rows(key):
    all_rows = []
    with open(f"{PATTERN_NAME}.pat", encoding="utf-8") as f:
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
    return all_rows


class MainWindow(QMainWindow):
    """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""

    def __init__(self):
        super().__init__()
        self.view = TableAndMenuView()
        self.view_widget = QWidget()
        self.view_widget.setLayout(self.view)
        self.setCentralWidget(self.view_widget)

        # TODO: add ability to remove areas by diagaonal, and from edges with rect later.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
