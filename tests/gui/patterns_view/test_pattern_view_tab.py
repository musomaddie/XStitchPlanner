from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QHBoxLayout, QTabWidget

from gui.patterns_view.pattern_view_tab import PatternViewTab

FILE_LOC = "gui.patterns_view.pattern_view_tab"


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
def test_init(mock_display):
    mock_display.return_value = QHBoxLayout()
    model_mock = MagicMock()

    view_tab = PatternViewTab("Testing", model_mock)
    mock_display.assert_called_once_with("Testing", model_mock, view_tab)
    assert view_tab.tabPosition() == QTabWidget.TabPosition.North
