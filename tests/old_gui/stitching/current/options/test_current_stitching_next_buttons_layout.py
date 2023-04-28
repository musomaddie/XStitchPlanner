from unittest.mock import MagicMock, call, patch

from gui.stitching.current.options.current_stitching_next_buttons_layout import \
    CurrentStitchingNextButtonsLayout

FILE_LOC = "old_gui.stitching.current.options.current_stitching_next_buttons_layout"


@patch(f"{FILE_LOC}.NextButton")
@patch(f"{FILE_LOC}.CurrentStitchingNextButtonsLayout.addWidget")
def test_init(add_widget_mock, next_button_mock):
    # TODO: fix this test
    return
    stitcher_mock = MagicMock()
    layout = CurrentStitchingNextButtonsLayout(stitcher_mock)
    next_button_mock.assert_has_calls([call("colour", stitcher_mock, layout), call("row", stitcher_mock, layout)])
    add_widget_mock.assert_has_calls(
        [call(next_button_mock.return_value), call(next_button_mock.return_value)])

    assert layout.parent is None
    assert len(layout.buttons) == 2
    for button in layout.buttons:
        assert button == next_button_mock.return_value
