from unittest.mock import patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.patterns_view.stitching_opt_menu_overview import \
    StitchingOptMenuOverview

FILE_LOC = "gui.patterns_view.stitching_opt_menu_overview."


@patch(f"{FILE_LOC}LimitColumnsLayout")
def test_init(limit_columns_mock, qtbot):
    limit_columns_mock.return_value = QVBoxLayout()
    test_widget = QWidget()
    opt_menu = StitchingOptMenuOverview()
    test_widget.setLayout(opt_menu)
    qtbot.addWidget(test_widget)

    assert opt_menu.parent is None
    assert limit_columns_mock.called
