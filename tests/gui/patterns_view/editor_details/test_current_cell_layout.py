from PyQt6.QtWidgets import QWidget

from gui.patterns_view.editor_details.current_cell_layout import \
    CurrentCellLayout


class Idx:
    def __init__(self, r, c):
        self._r = r
        self._c = c

    def row(self):
        return self._r

    def column(self):
        return self._c


def test_init(qtbot):
    test_widget = QWidget()
    current_cell_lay = CurrentCellLayout()
    test_widget.setLayout(current_cell_lay)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 3
    assert current_cell_lay.row_value == 0
    assert current_cell_lay.col_value == 0
    assert current_cell_lay.row_display.text() == "(row:) 0"
    assert current_cell_lay.col_display.text() == "(col:) 0"


def test_update_values(qtbot):
    test_widget = QWidget()
    current_cell_lay = CurrentCellLayout()
    test_widget.setLayout(current_cell_lay)
    qtbot.addWidget(test_widget)

    current_cell_lay.update_values(Idx(1, 2))

    assert current_cell_lay.row_value == 1
    assert current_cell_lay.col_value == 2
    assert current_cell_lay.row_display.text() == "(row:) 1"
    assert current_cell_lay.col_display.text() == "(col:) 2"
