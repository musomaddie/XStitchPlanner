from unittest.mock import patch

from gui.patterns_view.modifications.load_overlay import LoadOverlay

FILE_LOC = "gui.patterns_view.modifications.load_overlay"


@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
def test_init(add_widget_mock, button_mock):
    overlay = LoadOverlay()

    button_mock.assert_called_once_with("Show Saved Variants")
    add_widget_mock.assert_called_once_with(button_mock.return_value)

    assert overlay.load_show_options == button_mock.return_value
