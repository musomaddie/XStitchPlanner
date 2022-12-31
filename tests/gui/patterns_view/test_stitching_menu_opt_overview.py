from unittest.mock import MagicMock, call, patch

from gui.patterns_view.stitching_opt_menu_overview import StitchingOptMenuOverview
from pattern_modifiers.limiters.limiter_direction import LimiterDirection

FILE_LOC = "gui.patterns_view.stitching_opt_menu_overview"


@patch(f"{FILE_LOC}.LimiterOverlay")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.addWidget")
@patch(f"{FILE_LOC}.SaveButton")
@patch(f"{FILE_LOC}.LoadOverlay")
def test_init(
        load_overlay_mock,
        save_button_mock,
        add_widget_mock,
        widget_mock,
        button_overlay,
        limiter_overlay_mock):
    cc_layout_mock, model_mock = MagicMock(), MagicMock()
    col_mock, row_mock = MagicMock(), MagicMock()
    current_mods_mock = {LimiterDirection.COLUMN: col_mock, LimiterDirection.ROW: row_mock}
    opt_menu = StitchingOptMenuOverview("Testing", cc_layout_mock, model_mock, current_mods_mock)

    load_overlay_mock.assert_called_once_with("Testing", opt_menu)
    button_overlay.assert_called_once_with("Stitch This!")
    limiter_overlay_mock.assert_has_calls(
        [call(cc_layout_mock, LimiterDirection.COLUMN, col_mock, model_mock, opt_menu),
         call(cc_layout_mock, LimiterDirection.ROW, row_mock, model_mock, opt_menu)])
    widget_mock.assert_has_calls(
        [call(), call().setLayout(load_overlay_mock.return_value),
         call(), call().setLayout(limiter_overlay_mock.return_value),
         call(), call().setLayout(limiter_overlay_mock.return_value)])
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(widget_mock.return_value)])
    save_button_mock.assert_called_once_with(
        "Testing", model_mock,
        {LimiterDirection.COLUMN: limiter_overlay_mock().get_all_modifiers(),
         LimiterDirection.ROW: limiter_overlay_mock().get_all_modifiers()}, opt_menu)

    assert opt_menu.column_overlay == limiter_overlay_mock.return_value
    assert opt_menu.row_overlay == limiter_overlay_mock.return_value


@patch(f"{FILE_LOC}.LimiterOverlay")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.addWidget")
@patch(f"{FILE_LOC}.SaveButton")
@patch(f"{FILE_LOC}.LoadOverlay")
def test_load_stitch_view(
        load_overlay_mock,
        save_button_mock,
        add_widget_mock,
        widget_mock,
        button_overlay,
        limiter_overlay_mock):
    model_mock, parent_mock = MagicMock(), MagicMock()
    opt_menu = StitchingOptMenuOverview(
        "Testing", MagicMock(), model_mock, MagicMock(), parent_mock)
    opt_menu.load_stitch_view()
    parent_mock.assert_has_calls([call.load_stitch_view(model_mock)])


@patch(f"{FILE_LOC}.LoadOverlay")
@patch(f"{FILE_LOC}.LimiterOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.addWidget")
@patch(f"{FILE_LOC}.SaveButton")
def test_create_new_pattern_tab(
        load_overlay_mock, save_button_mock, add_widget_mock, widget_mock, overlay_mock):
    cc_layout_mock, model_mock, parent_mock = MagicMock(), MagicMock(), MagicMock()
    col_mock, row_mock = MagicMock(), MagicMock()
    new_model_mock, new_mod_mock = MagicMock(), MagicMock()
    current_mods_mock = {LimiterDirection.COLUMN: col_mock, LimiterDirection.ROW: row_mock}

    opt_menu = StitchingOptMenuOverview(
        "Testing", cc_layout_mock, model_mock, current_mods_mock, parent_mock)
    opt_menu.create_new_pattern_tab(new_model_mock, new_mod_mock)

    parent_mock.assert_has_calls([call.create_new_pattern_tab(new_model_mock, new_mod_mock)])


@patch(f"{FILE_LOC}.LoadOverlay")
@patch(f"{FILE_LOC}.LimiterOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.addWidget")
@patch(f"{FILE_LOC}.SaveButton")
def test_get_modifiers_for_direction(
        load_overlay_mock, save_button_mock, add_widget_mock, widget_mock, overlay_mock):
    cc_layout_mock, model_mock, parent_mock = MagicMock(), MagicMock(), MagicMock()
    col_mock, row_mock = MagicMock(), MagicMock()
    current_mods_mock = {LimiterDirection.COLUMN: col_mock, LimiterDirection.ROW: row_mock}

    opt_menu = StitchingOptMenuOverview(
        "Testing", cc_layout_mock, model_mock, current_mods_mock, parent_mock)

    opt_menu.get_modifiers_for_direction(LimiterDirection.COLUMN)
    opt_menu.column_overlay.assert_has_calls([call.get_all_modifiers()])

    opt_menu.get_modifiers_for_direction(LimiterDirection.ROW)
    opt_menu.row_overlay.assert_has_calls([call.get_all_modifiers()])


@patch(f"{FILE_LOC}.LoadOverlay")
@patch(f"{FILE_LOC}.LimiterOverlay")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.addWidget")
@patch(f"{FILE_LOC}.SaveButton")
@patch(f"{FILE_LOC}.StitchingOptMenuOverview.get_modifiers_for_direction")
def test_create_new_pattern_tab(
        get_mods_direction_mock,
        load_overlay_mock,
        save_button_mock,
        add_widget_mock,
        widget_mock,
        overlay_mock):
    cc_layout_mock, model_mock, parent_mock = MagicMock(), MagicMock(), MagicMock()
    col_mock, row_mock = MagicMock(), MagicMock()
    new_model_mock = MagicMock()
    current_mods_mock = {LimiterDirection.COLUMN: col_mock, LimiterDirection.ROW: row_mock}

    opt_menu = StitchingOptMenuOverview(
        "Testing", cc_layout_mock, model_mock, current_mods_mock, parent_mock)
    opt_menu.create_new_pattern_variant_tab(new_model_mock)

    get_mods_direction_mock.assert_has_calls(
        [call(LimiterDirection.ROW), call(LimiterDirection.COLUMN)])
    parent_mock.assert_has_calls(
        [call.create_new_pattern_variant_tab(
            new_model_mock, {LimiterDirection.ROW: get_mods_direction_mock.return_value,
                             LimiterDirection.COLUMN: get_mods_direction_mock.return_value})
        ])
