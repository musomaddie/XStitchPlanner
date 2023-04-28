from unittest.mock import ANY, MagicMock, call, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget)
from allpairspy import AllPairs
from calleee import InstanceOf
from gui.patterns_view.modifications.general_limiters.limiter_value_selector import (
    LimiterValueSelector, ValueWidget)

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "old_gui.patterns_view.modifications.general_limiters" \
           ".limiter_value_selector"


# Helpers
def assert_prompt(prompt: QWidget, expected_str: str):
    assert type(prompt) == QLabel
    assert prompt.text() == expected_str


def assert_button(widget: QWidget, exp_button_str: str):
    assert type(widget.layout()) == QHBoxLayout
    assert widget.layout().count() == 2
    assert type(widget.children()[1]) == QLineEdit
    assert type(widget.children()[2]) == QPushButton
    assert widget.children()[2].text() == exp_button_str


def setup_mocks(creator_mock):
    m = MagicMock()
    m.get_current_value.return_value = 100
    creator_mock.return_value = QWidget()
    return MagicMock(), m


@pytest.mark.parametrize("direction", list(LimiterType))
def test_value_widget_init_no_selector(direction):
    cc_mock = MagicMock()
    value_wid = ValueWidget(cc_mock, direction, LimiterMode.NO_SELECTOR)

    assert value_wid.current_cell_layout == cc_mock
    assert value_wid.direction == direction
    assert value_wid.mode == LimiterMode.NO_SELECTOR
    assert value_wid.supplied_values == []
    assert value_wid.set_current_value_buttons == []


@pytest.mark.parametrize("direction", list(LimiterType))
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.QVBoxLayout")
@patch(f"{FILE_LOC}.QLineEdit")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QHBoxLayout")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.ValueWidget.setLayout")
def test_value_widget_init_from(
        set_layout_mock, widget_mock, hbox_layout_mock, button_mock,
        line_edit_mock, vbox_layout_mock, label_mock, direction):
    # TODO: fix test
    return
    cc_mock = MagicMock()
    value_wid = ValueWidget(cc_mock, direction, LimiterMode.FROM)

    label_mock.assert_called_once_with("From:")
    vbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(label_mock.return_value),
         call().addWidget(widget_mock.return_value)])
    line_edit_mock.assert_has_calls(
        [call(), call().setValidator(InstanceOf(QIntValidator))])
    button_mock_string = ("Use current column"
                          if direction == LimiterType.COLUMN
                          else "Use current row")
    button_mock.assert_has_calls([call(button_mock_string), call().clicked.connect(ANY)])
    hbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(line_edit_mock.return_value),
         call().addWidget(button_mock.return_value)])
    widget_mock.assert_has_calls([call(), call().setLayout(hbox_layout_mock.return_value)])
    set_layout_mock.assert_called_once_with(vbox_layout_mock.return_value)

    assert value_wid.current_cell_layout == cc_mock
    assert value_wid.direction == direction
    assert value_wid.mode == LimiterMode.FROM
    assert value_wid.supplied_values == [line_edit_mock.return_value]
    assert value_wid.set_current_value_buttons == [button_mock.return_value]


@pytest.mark.parametrize("direction", list(LimiterType))
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.QVBoxLayout")
@patch(f"{FILE_LOC}.QLineEdit")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QHBoxLayout")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.ValueWidget.setLayout")
def test_value_widget_init_to(
        set_layout_mock, widget_mock, hbox_layout_mock, button_mock,
        line_edit_mock, vbox_layout_mock, label_mock, direction):
    # TODO: fix test
    return
    cc_mock = MagicMock()
    value_wid = ValueWidget(cc_mock, direction, LimiterMode.TO)

    label_mock.assert_called_once_with("To:")
    vbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(label_mock.return_value),
         call().addWidget(widget_mock.return_value)])
    line_edit_mock.assert_has_calls(
        [call(), call().setValidator(InstanceOf(QIntValidator))])
    button_mock_string = ("Use current column"
                          if direction == LimiterType.COLUMN
                          else "Use current row")
    button_mock.assert_has_calls([call(button_mock_string), call().clicked.connect(ANY)])
    hbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(line_edit_mock.return_value),
         call().addWidget(button_mock.return_value)])
    widget_mock.assert_has_calls([call(), call().setLayout(hbox_layout_mock.return_value)])
    set_layout_mock.assert_called_once_with(vbox_layout_mock.return_value)

    assert value_wid.current_cell_layout == cc_mock
    assert value_wid.direction == direction
    assert value_wid.mode == LimiterMode.TO
    assert value_wid.supplied_values == [line_edit_mock.return_value]
    assert value_wid.set_current_value_buttons == [button_mock.return_value]


@pytest.mark.parametrize("direction", list(LimiterType))
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.QVBoxLayout")
@patch(f"{FILE_LOC}.QLineEdit")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QHBoxLayout")
@patch(f"{FILE_LOC}.QWidget")
@patch(f"{FILE_LOC}.ValueWidget.setLayout")
def test_value_widget_init_between(
        set_layout_mock, widget_mock, hbox_layout_mock, button_mock,
        line_edit_mock, vbox_layout_mock, label_mock, direction):
    # TODO: fix test
    return
    cc_mock = MagicMock()
    value_wid = ValueWidget(cc_mock, direction, LimiterMode.BETWEEN)

    label_mock.assert_has_calls([call("Between:"), call("&")])
    vbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(label_mock.return_value), call().addWidget(widget_mock.return_value),
         call().addWidget(label_mock.return_value), call().addWidget(widget_mock.return_value)])
    line_edit_mock.assert_has_calls(
        [call(), call().setValidator(InstanceOf(QIntValidator)),
         call(), call().setValidator(InstanceOf(QIntValidator))])
    button_mock_string = ("Use current column"
                          if direction == LimiterType.COLUMN
                          else "Use current row")
    button_mock.assert_has_calls(
        [call(button_mock_string), call().clicked.connect(ANY),
         call(button_mock_string), call().clicked.connect(ANY)])
    hbox_layout_mock.assert_has_calls(
        [call(),
         call().addWidget(line_edit_mock.return_value),
         call().addWidget(button_mock.return_value),
         call(),
         call().addWidget(line_edit_mock.return_value),
         call().addWidget(button_mock.return_value)])
    widget_mock.assert_has_calls(
        [call(), call().setLayout(hbox_layout_mock.return_value),
         call(), call().setLayout(hbox_layout_mock.return_value)])
    set_layout_mock.assert_called_once_with(vbox_layout_mock.return_value)


@pytest.mark.parametrize("direction", [LimiterType.COLUMN, LimiterType.ROW])
@patch(f"{FILE_LOC}.ValueWidget")
@patch(f"{FILE_LOC}.QPushButton")
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterValueSelector.addWidget")
def test_init_general(add_widget_mock, label_mock, button_mock, value_mock, direction):
    cc_layout_mock, applier_mock = MagicMock(), MagicMock()
    selector = LimiterValueSelector(
        cc_layout_mock, applier_mock, direction, LimiterMode.NO_SELECTOR)
    # TODO parameterize for all modes
    value_mock.assert_called_once_with(cc_layout_mock, direction, LimiterMode.NO_SELECTOR)
    button_mock.assert_has_calls([call("Apply!"), call().pressed.connect(ANY)])
    label_text = ("Removes any currently applied column limits"
                  if direction == LimiterType.COLUMN
                  else "Removes any currently applied row limits")
    label_mock.assert_has_calls([call(label_text), call().setWordWrap(True)])
    add_widget_mock.assert_has_calls(
        [call(label_mock.return_value),
         call(value_mock.return_value),
         call(button_mock.return_value)])


@pytest.mark.parametrize(
    ("direction", "mode"),
    [values for values in AllPairs(
        [
            [LimiterType.COLUMN, LimiterType.ROW],
            [LimiterMode.NO_SELECTOR, LimiterMode.BETWEEN, LimiterMode.TO, LimiterMode.FROM]
        ])
     ]
)
@patch(f"{FILE_LOC}.ValueWidget")
def test_init_explanation_text(value_mock, direction, mode):
    applier_mock, current_cc_layout_mock = setup_mocks(value_mock)
    selector = LimiterValueSelector(current_cc_layout_mock, applier_mock, direction, mode)
    test_widget = QWidget()
    test_widget.setLayout(selector)

    actual_text = test_widget.children()[1].text()

    if mode == LimiterMode.NO_SELECTOR:
        if direction == LimiterType.COLUMN:
            assert actual_text == "Removes any currently applied column limits"
        else:
            assert actual_text == "Removes any currently applied row limits"
    elif mode == LimiterMode.BETWEEN:
        if direction == LimiterType.COLUMN:
            assert actual_text == "Only shows the pattern between " \
                                  "(inclusive) the provided column values"
        else:
            assert actual_text == "Only shows the pattern between " \
                                  "(inclusive) the provided row values"
    elif mode == LimiterMode.FROM:
        if direction == LimiterType.COLUMN:
            assert actual_text == "Only shows the pattern right " \
                                  "(inclusive) of the provided column value"
        else:
            assert actual_text == "Only shows the pattern below " \
                                  "(inclusive) the provided row value"
    else:
        if direction == LimiterType.COLUMN:
            assert actual_text == "Only shows the pattern left (inclusive) " \
                                  "of the provided column value"
        else:
            assert actual_text == "Only shows the pattern above (inclusive) " \
                                  "the provided row value"


@pytest.mark.parametrize("direction", [LimiterType.COLUMN, LimiterType.ROW])
def test_use_current_value_button(direction, qtbot):
    def mock_get_cur_value_method(direction):
        if direction == LimiterType.COLUMN:
            return 100
        else:
            return 200

    current_cell_layout_mock = MagicMock()
    current_cell_layout_mock.get_current_value.side_effect = mock_get_cur_value_method
    wid = ValueWidget(current_cell_layout_mock, direction, LimiterMode.FROM)
    qtbot.addWidget(wid)

    qtbot.mouseClick(wid.children()[2].children()[2], Qt.MouseButton.LeftButton)
    expected_value = 101 if direction == LimiterType.COLUMN else 201
    assert str(expected_value) in wid.children()[2].children()[1].text()
