from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QHBoxLayout, QTabWidget

from gui.patterns_view.pattern_view_tab_list import PatternViewTabList

FILE_LOC = "gui.patterns_view.pattern_view_tab_list"


@patch(f"{FILE_LOC}.PatternViewTabContents")
def test_init(tab_mock):
    tab_mock.return_value = QHBoxLayout()
    model_mock = MagicMock()

    view_tab = PatternViewTabList("Testing", model_mock)
    tab_mock.assert_called_once_with("Testing", model_mock, view_tab)
    assert view_tab.tabPosition() == QTabWidget.TabPosition.North
