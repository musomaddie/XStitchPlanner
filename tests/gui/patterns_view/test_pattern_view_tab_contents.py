from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.patterns_view.pattern_view_tab_contents import PatternViewTabContents

FILE_LOC = "gui.patterns_view.pattern_view_tab_contents"


def setup_mocks(toolbar_mock, display_mock):
    toolbar_mock.return_value = QWidget()
    display_mock.return_value = QHBoxLayout()
    return MagicMock(), MagicMock(), MagicMock()


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
@patch(f"{FILE_LOC}.PatternViewToolBar")
def test_init(toolbar_mock, display_mock):
    parent_mock, mod_mock, model_mock = setup_mocks(toolbar_mock, display_mock)
    contents = PatternViewTabContents("TESTING", model_mock, mod_mock)
    assert contents.layout().count() == 2

    assert display_mock.mock_calls == [call("TESTING", model_mock, mod_mock, contents)]
    assert toolbar_mock.mock_calls == [call(model_mock, display_mock.return_value)]


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
@patch(f"{FILE_LOC}.PatternViewToolBar")
def test_create_new_pattern_tab(toolbar_mock, display_mock):
    parent_mock, mod_mock, model_mock = setup_mocks(toolbar_mock, display_mock)
    contents = PatternViewTabContents("TESTING", model_mock, mod_mock, parent_mock)

    new_model_mock = MagicMock()
    new_mod_mock = MagicMock()
    contents.create_new_pattern_tab("TESTING", new_model_mock, new_mod_mock)

    assert parent_mock.mock_calls == [call.create_new_tab("TESTING", new_model_mock, new_mod_mock)]
