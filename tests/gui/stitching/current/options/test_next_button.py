from unittest.mock import patch

from gui.stitching.current.options.next_button import NextButton

FILE_LOC = "gui.stitching.current.options.next_button"


@patch(f"{FILE_LOC}.NextButton.setText")
def test_init(set_text_mock):
    button = NextButton("Testing Button")
    assert set_text_mock.has_calls("Testing Button")

    assert button.parent is None
