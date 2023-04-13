from unittest.mock import MagicMock, call, patch

from calleee import InstanceOf

from gui.patterns_view.editor_details.current_cell_layout import CurrentCellLayout
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "gui.patterns_view.editor_details.current_cell_layout"


class Idx:
    def __init__(self, r, c):
        self._r = r
        self._c = c

    def row(self):
        return self._r

    def column(self):
        return self._c


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.CurrentCellLayout.addWidget")
def test_init(add_widget_mock, qlabel_mock):
    current_cell_l = CurrentCellLayout()
    qlabel_mock.assert_has_calls(
        [call("Currently selected cell: "),
         call("(row:) 1"),
         call("(col:) 1")])
    add_widget_mock.assert_has_calls(
        [call(qlabel_mock.return_value) for _ in range(3)])

    assert current_cell_l.row_value == 0
    assert current_cell_l.col_value == 0


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.CurrentCellLayout.addWidget")
@patch(f"{FILE_LOC}.QLabel.setText")
def test_update_values(set_text_mock, add_widget_mock, qlabel_mock):
    values_mock = MagicMock()
    current_cell_lay = CurrentCellLayout()
    current_cell_lay.update_values(values_mock)

    values_mock.assert_has_calls([call.row(), call.column()])
    qlabel_mock.assert_has_calls(
        [
            call("Currently selected cell: "),
            call("(row:) 1"),
            call("(col:) 1"),
            call().setText(InstanceOf(str)),
            call().setText(InstanceOf(str))
        ])


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.CurrentCellLayout.addWidget")
def test_get_current_value(add_widget_mock, qlabel_mock):
    current_cell_layout = CurrentCellLayout()
    current_cell_layout.row_value = 1
    current_cell_layout.col_value = 2

    assert current_cell_layout.get_current_value(LimiterType.ROW) == 1
    assert current_cell_layout.get_current_value(LimiterType.COLUMN) == 2
