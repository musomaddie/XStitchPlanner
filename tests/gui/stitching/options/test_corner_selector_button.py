from unittest.mock import MagicMock, call, patch

import pytest

from gui.stitching.options.corner_selector_button import CornerSelectorButton
from stitching_technique.starting_corner import BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT

FILE_LOC = "gui.stitching.options.corner_selector_button"


@pytest.mark.parametrize("corner", [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
@patch(f"{FILE_LOC}.CornerSelectorButton.setText")
@patch(f"{FILE_LOC}.CornerSelectorButton.setStyleSheet")
def test_init(set_style_mock, set_text_mock, corner):
    button = CornerSelectorButton(corner)

    set_style_mock.assert_called_once_with("background-color: gray")
    set_text_mock.assert_called_once_with(corner.description.title())

    assert button.corner == corner


@patch(f"{FILE_LOC}.CornerSelectorButton.setText")
@patch(f"{FILE_LOC}.CornerSelectorButton.setStyleSheet")
def test_eq(set_style_mock, set_text_mock):
    button_1 = CornerSelectorButton(TOP_LEFT)
    button_2 = CornerSelectorButton(TOP_LEFT)
    button_3 = CornerSelectorButton(TOP_RIGHT)
    button_4 = CornerSelectorButton(BOTTOM_LEFT)
    button_5 = CornerSelectorButton(BOTTOM_RIGHT)

    assert button_1 == button_2
    assert button_1 != button_3
    assert button_2 != button_4
    assert button_5 != button_4


@pytest.mark.parametrize("corner", [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
@patch(f"{FILE_LOC}.CornerSelectorButton.setText")
@patch(f"{FILE_LOC}.CornerSelectorButton.setStyleSheet")
def test_select(set_style_mock, set_text_mock, corner):
    parent_mock = MagicMock()
    button = CornerSelectorButton(corner, parent_mock)
    button.select()

    set_style_mock.assert_has_calls(
        [call("background-color: gray"), call("background-color: " "blue")])
    parent_mock.assert_has_calls(([call.select_corner(button)]))


@pytest.mark.parametrize("corner", [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
@patch(f"{FILE_LOC}.CornerSelectorButton.setText")
@patch(f"{FILE_LOC}.CornerSelectorButton.setStyleSheet")
def test_deselect(set_style_mock, set_text_mock, corner):
    button = CornerSelectorButton(corner)
    button.deselect()

    set_style_mock.assert_has_calls(
        [call("background-color: gray"), call("background-color: gray")]
    )
