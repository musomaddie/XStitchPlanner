from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.patterns_view.pattern_view_tab_contents import PatternViewTabContents

FILE_LOC = "gui.patterns_view.pattern_view_tab_contents"


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
@patch(f"{FILE_LOC}.PatternViewToolBar")
def test_init(toolbar_mock, display_mock):
    toolbar_mock.return_value = QWidget()
    display_mock.return_value = QHBoxLayout()
    model = MagicMock()
    contents = PatternViewTabContents("TESTING", model)
    assert contents.layout().count() == 2

    assert toolbar_mock.mock_calls == [call(model, display_mock.return_value)]
    assert display_mock.mock_calls == [call("TESTING", model, contents)]
