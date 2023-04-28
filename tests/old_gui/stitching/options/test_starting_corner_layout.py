from unittest.mock import call, patch

from gui.stitching.options.starting_corner_layout import StartingCornerLayout

from stitchers.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT

FILE_LOC = "old_gui.stitching.options.starting_corner_layout"


@patch(f"{FILE_LOC}.CornerSelectorButton")
@patch(f"{FILE_LOC}.StartingCornerLayout.addWidget")
def test_init(add_widget_mock, button_mock):
    layout = StartingCornerLayout()
    button_mock.assert_has_calls(
        [call(TOP_LEFT, layout), call(TOP_RIGHT, layout),
         call(BOTTOM_LEFT, layout), call(BOTTOM_RIGHT, layout)])

    add_widget_mock.assert_has_calls(
        [call(button_mock.return_value, 0, 0), call(button_mock.return_value, 0, 1),
         call(button_mock.return_value, 1, 0), call(button_mock.return_value, 1, 1)])

# TODO: add tests for deselect_others
