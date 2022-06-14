from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QComboBox, QStackedLayout, QWidget

from gui.patterns_view.modifications.limit_columns import (
    ColumnLimiterMode, LimitColumnsDropDown, LimitColumnsLayout,
    LimitColumnsValueSelector)

FILE_LOC = "gui.patterns_view.modifications.limit_columns."


# VALUE_SELECTOR
def test_init_value_selector(qtbot):
    test_widget = QWidget()
    value_selector = LimitColumnsValueSelector()
    test_widget.setLayout(value_selector)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 4
    assert value_selector.currentIndex() == 0


@pytest.mark.parametrize(
    ("new_mode", "num_child"),
    [(ColumnLimiterMode.NO_SELECTOR, 0),
     (ColumnLimiterMode.BETWEEN_COLUMNS, 1),
     (ColumnLimiterMode.FROM_COLUMN, 2),
     (ColumnLimiterMode.TO_COLUMN, 3)]
)
def test_change_selected(new_mode, num_child, qtbot):
    test_widget = QWidget()
    value_selector = LimitColumnsValueSelector()
    test_widget.setLayout(value_selector)
    qtbot.addWidget(test_widget)

    value_selector.change_selected(new_mode)
    assert value_selector.currentIndex() == num_child


# LAYOUT
@patch(f"{FILE_LOC}LimitColumnsValueSelector")
@patch(f"{FILE_LOC}LimitColumnsDropDown")
def test_init_layout(dropdown_mock, selector_mock, qtbot):
    dropdown_mock.return_value = QComboBox()
    selector_mock.return_value = QStackedLayout()
    test_widget = QWidget()
    limit_columns = LimitColumnsLayout()
    test_widget.setLayout(limit_columns)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 3
    assert dropdown_mock.called
    assert selector_mock.called


# DROPDOWN
def test_init_dropdown(qtbot):
    opt_dropdown = LimitColumnsDropDown(MagicMock())
    qtbot.addWidget(opt_dropdown)

    assert opt_dropdown.currentIndex() == 0
    assert opt_dropdown.options == [
        ColumnLimiterMode.NO_SELECTOR,
        ColumnLimiterMode.BETWEEN_COLUMNS,
        ColumnLimiterMode.FROM_COLUMN,
        ColumnLimiterMode.TO_COLUMN]


@pytest.mark.parametrize(
    ("index", "expected_argument"),
    [(0, ColumnLimiterMode.NO_SELECTOR),
     (1, ColumnLimiterMode.BETWEEN_COLUMNS),
     (2, ColumnLimiterMode.FROM_COLUMN),
     (3, ColumnLimiterMode.TO_COLUMN)]
)
def test_update_currently_selected(index, expected_argument):
    value_selector = MagicMock()
    opt_dropdown = LimitColumnsDropDown(value_selector)

    opt_dropdown.setCurrentIndex(index)
    opt_dropdown.update_currently_selected()
    assert value_selector.mock_calls == [
        call.change_selected(expected_argument)]
