from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QWidget
from calleee import InstanceOf

from gui.view_hierarchy import ViewHierarchy

FILE_LOC = "gui.view_hierarchy"

# TODO: commented out temporarily due to the added pattern_chosen call. When restructuring move
#  part of test_pattern_chosen to test_init
"""
@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
def test_init(set_layout_mock, add_widget_mock, selector_layout_mock):
    selector_layout_mock.return_value = QVBoxLayout()
    view_hierarchy = ViewHierarchy()

    selector_layout_mock.assert_called_once_with(view_hierarchy)

test_widget = ViewHierarchy()

assert test_widget.layout().count() == 2
selector_layout_mock.assert_called_once_with(test_widget)
# assert test_widget.currentIndex() == 0
# Changed to reflect the temp hard coded call
assert test_widget.currentIndex() == 1
"""


@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.PatternDisplayModel.load_from_pattern_file")
@patch(f"{FILE_LOC}.PatternViewTabList")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.setCurrentWidget")
def test_pattern_chosen(
        set_current_widget_mock,
        set_layout_mock,
        add_widget_mock,
        tablist_mock,
        model_mock,
        selector_mock):

    view_hierarchy = ViewHierarchy()

    selector_mock.assert_called_once_with(view_hierarchy)
    model_mock.assert_has_calls([call.load_from_pattern_file("hp")])
    tablist_mock.assert_called_once_with("hp", model_mock.return_value, view_hierarchy)
    add_widget_mock.assert_has_calls([call(InstanceOf(QWidget)), call(tablist_mock.return_value)])
    set_layout_mock.assert_called_once_with(selector_mock.return_value)
    set_current_widget_mock.assert_called_once_with(tablist_mock.return_value)


@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.PatternDisplayModel.load_from_pattern_file")
@patch(f"{FILE_LOC}.PatternViewTabList")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.QWidget.setLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.setCurrentWidget")
def test_load_stitch_view(
        set_current_widget_mock,
        set_layout_mock,
        add_widget_mock,
        tablist_mock,
        model_mock,
        selector_mock):
    model_mock = MagicMock()
    view_hierarchy = ViewHierarchy()
    view_hierarchy.load_stitch_view("Testing", model_mock)
