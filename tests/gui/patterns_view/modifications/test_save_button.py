from unittest.mock import patch

from gui.patterns_view.modifications.save_button import SaveButton

FILE_LOC = "gui.patterns_view.modifications.save_button"


@patch(f"{FILE_LOC}.SaveButton.setText")
def test_init(set_text_mock):
    save_button = SaveButton()
    set_text_mock.assert_called_once_with("Save these modifications")
