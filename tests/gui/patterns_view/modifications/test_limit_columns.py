from unittest.mock import patch

from PyQt6.QtWidgets import QComboBox, QStackedLayout, QWidget

from gui.patterns_view.modifications.limit_columns import (
    ColumnLimiterMode, LimitColumnsDropDown, LimitColumnsLayout,
    LimitColumnsValueSelector)

FILE_LOC = "gui.patterns_view.modifications.limit_columns."


def test_init_value_selector(qtbot):
    test_widget = QWidget()
    value_selector = LimitColumnsValueSelector()
    test_widget.setLayout(value_selector)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 4


@patch(f"{FILE_LOC}LimitColumnsValueSelector")
@patch(f"{FILE_LOC}LimitColumnsDropDown")
def test_init(dropdown_mock, selector_mock, qtbot):
    dropdown_mock.return_value = QComboBox()
    selector_mock.return_value = QStackedLayout()
    test_widget = QWidget()
    limit_columns = LimitColumnsLayout()
    test_widget.setLayout(limit_columns)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 3
    assert dropdown_mock.called
    assert selector_mock.called


def test_init_dropdown(qtbot):
    opt_dropdown = LimitColumnsDropDown()
    qtbot.addWidget(opt_dropdown)

    assert opt_dropdown.selected_mode == ColumnLimiterMode.NO_SELECTOR
    assert opt_dropdown.options == [
        ColumnLimiterMode.NO_SELECTOR,
        ColumnLimiterMode.BETWEEN_COLUMNS,
        ColumnLimiterMode.FROM_COLUMN,
        ColumnLimiterMode.TO_COLUMN]
