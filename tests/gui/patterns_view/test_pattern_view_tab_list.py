from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QHBoxLayout, QTabWidget

from gui.patterns_view.pattern_view_tab_list import PatternViewTabList

FILE_LOC = "gui.patterns_view.pattern_view_tab_list"


@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.Modification")
def test_init(mod_mock, tab_mock):
    tab_mock.return_value = QHBoxLayout()
    model_mock = MagicMock()

    view_tab = PatternViewTabList("Testing", model_mock)
    tab_mock.assert_called_once_with("Testing", model_mock, mod_mock.return_value, view_tab)

    assert view_tab.tabPosition() == QTabWidget.TabPosition.North
    assert view_tab.currentIndex() == 0
    assert view_tab.tabText(0) == "Testing (Original)"


@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.Modification")
@patch(f"{FILE_LOC}.PatternDisplayModel")
def test_create_new_tab(display_model_mock, mod_mock, tab_mock):
    tab_mock.return_value = QHBoxLayout()
    model_data_mock = MagicMock()
    new_mod_mock = MagicMock()
    model_mock = MagicMock()

    view_tab_list = PatternViewTabList("Testing", model_mock)
    view_tab_list.create_new_tab("TESTING", model_data_mock, new_mod_mock)

    display_model_mock.assert_called_once_with(model_data_mock)
    assert tab_mock.mock_calls == [
        call("Testing", model_mock, mod_mock.return_value, view_tab_list),
        call("TESTING", display_model_mock.return_value, new_mod_mock, view_tab_list)]

    assert len(view_tab_list.tab_list) == 1
    assert view_tab_list.currentIndex() == 1
    assert view_tab_list.tabText(1) == "TESTING (1)"
