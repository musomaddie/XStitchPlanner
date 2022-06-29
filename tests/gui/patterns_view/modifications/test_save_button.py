from unittest.mock import MagicMock, patch

import pytest

from gui.patterns_view.modifications.save_button import SaveButton
from pattern_modifiers.limiters.limiter_direction import LimiterDirection
from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.modification import Modification

FILE_LOC = "gui.patterns_view.modifications.save_button"


@patch(f"{FILE_LOC}.SaveButton.setText")
def test_init(set_text_mock):
    save_button = SaveButton(
        "Testing", None, {LimiterDirection.ROW: [Modification(LimiterMode.NO_SELECTOR, [])],
                          LimiterDirection.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])]})

    set_text_mock.assert_called_once_with("Save these modifications")
    assert len(save_button.applied_modifications) == 2


@pytest.mark.parametrize(
    ("modifications, expected_filename"),
    [({LimiterDirection.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])],
       LimiterDirection.ROW: [Modification(LimiterMode.NO_SELECTOR, [])]},
      "Testing-row--col--variant"),
     ({LimiterDirection.COLUMN: [Modification(LimiterMode.BETWEEN, [2, 3])],
       LimiterDirection.ROW: [
           Modification(LimiterMode.FROM, [5]), Modification(LimiterMode.TO, [12])]},
      "Testing-row-from[5]to[12]-col-between[2_3]-variant")]
)
@patch(f"{FILE_LOC}.SaveButton.setText")
def test_make_filename(set_text_mock, modifications, expected_filename):
    save_button = SaveButton("Testing", None, modifications)
    assert save_button._make_filename() == expected_filename


@patch(f"{FILE_LOC}.SaveButton.setText")
@patch(f"{FILE_LOC}.save_pattern")
def test_save_pattern_variant(save_pattern_mock, set_text_mock):
    model_mock = MagicMock()
    model_mock._data = [["a", "a", "b"], ["b", "b", "a"], ["a", "b", "a"]]
    save_button = SaveButton(
        "Testing",
        model_mock,
        {LimiterDirection.ROW: [Modification(LimiterMode.NO_SELECTOR, [])],
         LimiterDirection.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])]}
    )
    save_button.save_pattern_variant()

    save_pattern_mock.assert_called_once_with("Testing-row--col--variant", model_mock._data)
