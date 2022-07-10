from unittest.mock import call, patch

from gui.stitching.prepare.pre_stitching_options_overlay import PreStitchingOptionsOverlay

FILE_LOC = "gui.stitching.prepare.pre_stitching_options_overlay"


@patch(f"{FILE_LOC}.StartingCornerOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PreStitchingOptionsOverlay.addWidget")
@patch(f"{FILE_LOC}.StitchingTechniqueComboBox")
@patch(f"{FILE_LOC}.QPushButton")
def test_init(button_mock, tech_box_mock, add_widget_mock, widget_mock, corner_mock):
    overlay = PreStitchingOptionsOverlay()

    corner_mock.assert_called_once_with(overlay)
    widget_mock.assert_has_calls([call(), call().setLayout(corner_mock.return_value)])
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value),
         call(tech_box_mock.return_value),
         call(button_mock.return_value)])
    tech_box_mock.assert_called_once_with(overlay)
    button_mock.assert_called_once_with("Start Stitching!")

    assert overlay.starting_corner == corner_mock.return_value
    assert overlay.stitching_technique == tech_box_mock.return_value
    assert overlay.start_button == button_mock.return_value
