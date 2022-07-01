from unittest.mock import call, patch

from gui.patterns_view.modifications.load_overlay import LoadOverlay

FILE_LOC = "gui.patterns_view.modifications.load_overlay"


@patch(f"{FILE_LOC}.VariantsLoadDropDown")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
@patch(f"{FILE_LOC}.QPushButton")
def test_init(button_mock, add_widget_mock, dropdown_mock):
    # def test_init(add_widget_mock, button_mock):
    overlay = LoadOverlay("testing")

    dropdown_mock.assert_called_once_with("testing")
    button_mock.assert_called_once_with("Load This Variant")
    add_widget_mock.assert_has_calls(
        [call(dropdown_mock.return_value), call(button_mock.return_value)])
