from PyQt6.QtWidgets import QWidget

from gui.patterns_view.editor_details.current_cell_layout import CurrentCellLayout
from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection


class Idx:
    def __init__(self, r, c):
        self._r = r
        self._c = c

    def row(self):
        return self._r

    def column(self):
        return self._c


def test_init():
    test_widget = QWidget()
    current_cell_lay = CurrentCellLayout()
    test_widget.setLayout(current_cell_lay)

    assert test_widget.layout().count() == 3
    assert current_cell_lay.row_value == 0
    assert current_cell_lay.col_value == 0
    assert current_cell_lay.row_display.text() == "(row:) 1"
    assert current_cell_lay.col_display.text() == "(col:) 1"


def test_update_values():
    test_widget = QWidget()
    current_cell_lay = CurrentCellLayout()
    test_widget.setLayout(current_cell_lay)

    current_cell_lay.update_values(Idx(1, 2))

    assert current_cell_lay.row_value == 1
    assert current_cell_lay.col_value == 2
    assert current_cell_lay.row_display.text() == "(row:) 2"
    assert current_cell_lay.col_display.text() == "(col:) 3"


def test_get_current_value():
    test_widget = QWidget()
    current_cell_layout = CurrentCellLayout()
    test_widget.setLayout(current_cell_layout)

    current_cell_layout.update_values(Idx(1, 2))

    assert current_cell_layout.get_current_value(LimiterDirection.ROW) == 1
    assert current_cell_layout.get_current_value(LimiterDirection.COLUMN) == 2
