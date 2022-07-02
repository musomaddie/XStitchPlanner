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
@patch(f"{FILE_LOC}.PatternViewTabContents.addWidget")
@patch(f"{FILE_LOC}.QWidget")
def test_init(widget_mock, add_widget_mock, toolbar_mock, overlay_mock):
    model_mock, mod_mock = MagicMock(), MagicMock()
    name = "Testing"
    contents = PatternViewTabContents(name, model_mock, mod_mock)

    overlay_mock.assert_called_once_with(name, model_mock, mod_mock, contents)
    toolbar_mock.assert_called_once_with(model_mock, overlay_mock.return_value)
    add_widget_mock.assert_has_calls(
        [call(toolbar_mock.return_value), call(widget_mock.return_value)])
    widget_mock.assert_has_calls([call(), call().setLayout(overlay_mock.return_value)])

    assert contents.display_overlay == overlay_mock.return_value
    assert contents.toolbar == toolbar_mock.return_value


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
@patch(f"{FILE_LOC}.PatternViewToolBar")
@patch(f"{FILE_LOC}.PatternViewTabContents.addWidget")
@patch(f"{FILE_LOC}.QWidget")
def test_create_new_pattern_tab_with_modifications(
        widget_mock, add_widget_mock, toolbar_mock, overlay_mock):
    model_mock, mod_mock, parent_mock = MagicMock(), MagicMock(), MagicMock()
    contents = PatternViewTabContents("Testing", model_mock, mod_mock, parent_mock)
    new_model, modification = MagicMock(), MagicMock()

    contents.create_new_pattern_tab(new_model, modification)
    parent_mock.assert_has_calls([call.create_new_tab_with_modifications(new_model, modification)])


@patch(f"{FILE_LOC}.PatternDisplayOverlay")
@patch(f"{FILE_LOC}.PatternViewToolBar")
@patch(f"{FILE_LOC}.PatternViewTabContents.addWidget")
@patch(f"{FILE_LOC}.QWidget")
def test_create_new_pattern_variant_tab(
        widget_mock, add_widget_mock, toolbar_mock, overlay_mock):
    model_mock, mod_mock, parent_mock = MagicMock(), MagicMock(), MagicMock()
    contents = PatternViewTabContents("Testing", model_mock, mod_mock, parent_mock)
    new_model_data, modification = MagicMock(), MagicMock()

    contents.create_new_pattern_variant_tab(new_model_data, modification)
    parent_mock.assert_has_calls(
        [call.create_new_pattern_variant_tab(new_model_data, modification)])
