from unittest.mock import MagicMock, call, patch

from gui.view_hierarchy import ViewHierarchy

FILE_LOC = "gui.view_hierarchy"


@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.ViewHierarchy.load_stitch_view")  # TODO: delete when init updates
def test_init(load_stitch_view_mock, add_widget_mock, selector_layout_mock, widget_mock):
    view_hierarchy = ViewHierarchy()

    widget_mock.assert_has_calls(
        [call(), call().setLayout(selector_layout_mock.return_value)])
    selector_layout_mock.assert_called_once_with(view_hierarchy)
    add_widget_mock.assert_called_once_with(widget_mock.return_value)
    assert load_stitch_view_mock.called

    assert view_hierarchy.model is None


@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.PatternDisplayModel.load_from_pattern_file")
@patch(f"{FILE_LOC}.PatternViewTabList")
@patch(f"{FILE_LOC}.ViewHierarchy.setCurrentWidget")
@patch(f"{FILE_LOC}.ViewHierarchy.load_stitch_view")  # TODO: delete when init updates
def test_pattern_chosen(
        load_stitch_view_mock,
        current_widget_mock,
        tab_list_mock,
        model_load_mock,
        add_widget_mock,
        selector_layout_mock,
        widget_mock):
    view_hierarchy = ViewHierarchy()
    view_hierarchy.pattern_chosen("Testing")

    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(tab_list_mock.return_value)])
    model_load_mock.assert_has_calls(
        [call("hp-row-between[126_392]-col-to[39]-variant"), call("Testing")]
    )
    # model_load_mock.assert_called_once_with("hp") TODO: uncomment when init updates
    tab_list_mock.assert_called_once_with("Testing", model_load_mock.return_value, view_hierarchy)
    current_widget_mock.assert_called_once_with(tab_list_mock.return_value)

    assert view_hierarchy.model == model_load_mock.return_value


@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.ViewHierarchy.pattern_chosen")  # TODO: delete when init updates
@patch(f"{FILE_LOC}.StitchingOverlay")
@patch(f"{FILE_LOC}.PrepareStitchingDisplayModel")
@patch(f"{FILE_LOC}.ViewHierarchy.addWidget")
@patch(f"{FILE_LOC}.ViewHierarchy.setCurrentWidget")
@patch(f"{FILE_LOC}.PatternDisplayModel.load_from_pattern_file")
def test_load_stitch_view(
        pattern_file_load_mock,
        current_wid_mock,
        add_widget_mock,
        display_model_mock,
        stitching_overlay_mock,
        pattern_chosen_mock,
        selector_layout_mock,
        widget_mock):
    og_model_mock = MagicMock()
    view_hierarchy = ViewHierarchy()
    # view_hierarchy.load_stitch_view("Testing", og_model_mock)  # TODO: uncomment when init changes

    widget_mock.assert_has_calls(
        [call(), call().setLayout(selector_layout_mock.return_value),
         call(), call().setLayout(stitching_overlay_mock.return_value)])
    stitching_overlay_mock.assert_called_once_with(
        "hp", display_model_mock.return_value, view_hierarchy)
    # "Testing", display_model_mock.return_value, view_hierarchy) TODO: uncomment when init
    #  changes
    # display_model_mock.assert_called_once_with(og_model_mock._data) TODO: uncomment when init
    #  changes
    display_model_mock.assert_called_once_with(pattern_file_load_mock()._data)
    add_widget_mock.assert_has_calls(
        [call(widget_mock.return_value), call(widget_mock.return_value)])
    current_wid_mock.assert_called_once_with(widget_mock.return_value)
