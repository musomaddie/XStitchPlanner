from unittest.mock import MagicMock, call, patch

from gui.stitching.options.starting_corner_overlay import StartingCornerOverlay

FILE_LOC = "old_gui.stitching.options.starting_corner_overlay"


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.StartingCornerOverlay.addWidget")
@patch(f"{FILE_LOC}.StartingCornerLayout")
@patch(f"{FILE_LOC}.QWidget")
def test_init(widget_mock, corner_layout_mock, add_widget_mock, label_mock):
    overlay = StartingCornerOverlay()

    label_mock.assert_called_once_with("Select the corner of the pattern where you start stitching")
    add_widget_mock.assert_has_calls(
        [call(label_mock.return_value), call(widget_mock.return_value)])
    corner_layout_mock.assert_called_once_with(overlay)
    widget_mock.assert_has_calls([call(), call().setLayout(corner_layout_mock.return_value)])

    assert overlay.parent is None
    assert overlay.selected_corner is None
    assert overlay.header == label_mock.return_value
    assert overlay.grid == corner_layout_mock.return_value


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.StartingCornerOverlay.addWidget")
@patch(f"{FILE_LOC}.StartingCornerLayout")
@patch(f"{FILE_LOC}.QWidget")
def test_select_corner(widget_mock, corner_layout_mock, add_widget_mock, label_mock):
    overlay = StartingCornerOverlay()
    button = MagicMock()

    overlay.select_corner(button)
    assert overlay.selected_corner == button.corner
