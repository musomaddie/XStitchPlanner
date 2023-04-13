from unittest.mock import ANY, MagicMock, call, patch

from PyQt6.QtWidgets import QTabWidget

from gui.patterns_view.pattern_view_tab_list import PatternViewTabList
from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "gui.patterns_view.pattern_view_tab_list"


@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.Modification")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternViewTabList.setTabPosition")
@patch(f"{FILE_LOC}.PatternViewTabList.addTab")
def test_init(add_tab_mock, set_tab_pos_mock, widget_mock, mod_mock, contents_mock):
    # TODO: fix test
    return
    model_mock = MagicMock()
    view_tab = PatternViewTabList("Testing", model_mock)

    contents_mock.assert_called_once_with(
        "Testing", model_mock,
        {LimiterType.ROW: [mod_mock.return_value],
         LimiterType.COLUMN: [mod_mock.return_value]},
        view_tab)
    mod_mock.assert_has_calls(
        [call(LimiterMode.NO_SELECTOR, []), call(LimiterMode.NO_SELECTOR, [])])
    widget_mock.assert_has_calls([call(), call().setLayout(contents_mock.return_value)])
    set_tab_pos_mock.assert_called_once_with(QTabWidget.TabPosition.North)
    add_tab_mock.assert_called_once_with(widget_mock.return_value, "Testing (Original)")

    assert view_tab.original_layout == contents_mock.return_value
    assert len(view_tab.tab_list) == 0
    assert len(view_tab.tab_counts) == 2
    assert view_tab.tab_counts["modifications"] == 0
    assert view_tab.tab_counts["variants"] == 0


@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.Modification")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternViewTabList.setTabPosition")
@patch(f"{FILE_LOC}.PatternViewTabList.addTab")
def test_load_stitch_view(add_tab_mock, set_tab_pos_mock, widget_mock, mod_mock, contents_mock):
    model_mock, parent_mock = [MagicMock() for _ in range(2)]
    view_tab = PatternViewTabList("Testing", MagicMock(), parent_mock)
    view_tab.load_stitch_view(model_mock)
    parent_mock.assert_has_calls([call.load_stitch_view("Testing", model_mock)])


@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.Modification")
@patch(f"{FILE_LOC}.PatternDisplayModel")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternViewTabList.setTabPosition")
@patch(f"{FILE_LOC}.PatternViewTabList.addTab")
@patch(f"{FILE_LOC}.PatternViewTabList.setCurrentIndex")
def test_create_new_tab_with_modifications(
        set_cur_index_mock,
        add_tab_mock,
        set_tab_pos_mock,
        widget_mock,
        display_model_mock,
        mod_mock,
        contents_mock):
    # TODO: fix test
    return
    model_data_mock = MagicMock()
    new_mod_mock = MagicMock()
    model_mock = MagicMock()

    view_tab_list = PatternViewTabList("Testing", model_mock)
    view_tab_list.create_new_tab_with_modifications(model_data_mock, new_mod_mock)

    display_model_mock.assert_called_once_with(model_data_mock)
    contents_mock.assert_has_calls(
        [call(
            "Testing", model_mock, {LimiterType.ROW: [mod_mock.return_value],
                                    LimiterType.COLUMN: [mod_mock.return_value]},
            view_tab_list),
            call("Testing", display_model_mock.return_value, new_mod_mock, view_tab_list)])

    widget_mock.assert_has_calls(
        [call(), call().setLayout(contents_mock.return_value),
         call(), call().setLayout(contents_mock.return_value)])
    add_tab_mock.assert_has_calls(
        [call(widget_mock.return_value, "Testing (Original)"),
         call(widget_mock.return_value, "Testing (1)")])
    set_cur_index_mock.assert_called_once_with(1)

    assert len(view_tab_list.tab_list) == 1
    assert view_tab_list.tab_list[0] == contents_mock.return_value
    assert view_tab_list.tab_counts["modifications"] == 1
    assert view_tab_list.tab_counts["variants"] == 0


@patch(f"{FILE_LOC}.Modification")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.PatternViewTabList.setTabPosition")
@patch(f"{FILE_LOC}.PatternViewTabList.addTab")
@patch(f"{FILE_LOC}.PatternDisplayModel")
@patch(f"{FILE_LOC}.PatternViewTabContents")
@patch(f"{FILE_LOC}.PatternViewTabList.setCurrentIndex")
def test_create_new_tab_with_variant(
        set_current_index_mock,
        contents_mock,
        display_model_mock,
        add_tab_mock,
        set_tab_pos_mock,
        widget_mock,
        mod_mock):
    model_data_mock = MagicMock()
    new_model_data_mock = MagicMock()
    new_mods_mock = MagicMock()

    view_tab_list = PatternViewTabList("Testing", model_data_mock)
    view_tab_list.create_new_tab_with_variant(new_model_data_mock, new_mods_mock)

    display_model_mock.assert_called_once_with(new_model_data_mock)
    contents_mock.assert_has_calls(
        [call("Testing", model_data_mock, ANY, view_tab_list),
         call("Testing", display_model_mock.return_value, new_mods_mock, view_tab_list)])
    widget_mock.assert_has_calls(
        [call(), call().setLayout(contents_mock.return_value),
         call(), call().setLayout(contents_mock.return_value)])
    add_tab_mock.assert_has_calls(
        [call(widget_mock.return_value, "Testing (Original)"),
         call(widget_mock.return_value, "Testing variant #1")])
    set_current_index_mock.assert_called_once_with(1)

    assert len(view_tab_list.tab_list) == 1
    assert view_tab_list.tab_list[0] == contents_mock.return_value
    assert view_tab_list.tab_counts["modifications"] == 0
    assert view_tab_list.tab_counts["variants"] == 1
