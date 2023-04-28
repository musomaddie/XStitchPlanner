from unittest.mock import MagicMock, call, patch

import pytest
from gui.patterns_view.modifications.save_button import SaveButton

from pattern_cells.pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType
from pattern_modifiers.limiters.modification import Modification

FILE_LOC = "old_gui.patterns_view.modifications.save_button"


@patch(f"{FILE_LOC}.SaveButton.setText")
def test_init(set_text_mock):
    save_button = SaveButton(
        "Testing", None, {LimiterType.ROW: [Modification(LimiterMode.NO_SELECTOR, [])],
                          LimiterType.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])]})

    set_text_mock.assert_called_once_with("Save these modifications")
    assert len(save_button.applied_modifications) == 2


@pytest.mark.parametrize(
    ("modifications, expected_filename"),
    [({LimiterType.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])],
       LimiterType.ROW: [Modification(LimiterMode.NO_SELECTOR, [])]},
      "Testing-row--col--variant"),
     ({LimiterType.COLUMN: [Modification(LimiterMode.BETWEEN, [2, 3])],
       LimiterType.ROW: [
           Modification(LimiterMode.FROM, [5]), Modification(LimiterMode.TO, [12])]},
      "Testing-row-from[5]to[12]-col-between[2_3]-variant")]
)
@patch(f"{FILE_LOC}.SaveButton.setText")
def test_make_filename(set_text_mock, modifications, expected_filename):
    save_button = SaveButton("Testing", None, modifications)
    assert save_button._make_filename() == expected_filename


@patch(f"{FILE_LOC}.SaveButton.setText")
@patch(f"{FILE_LOC}.save_pattern")
@patch(f"{FILE_LOC}.QLabel")
def test_save_pattern_variant(label_mock, save_pattern_mock, set_text_mock):
    model_mock = MagicMock()
    parent_mock = MagicMock()
    pa = PatternCell("a", "310", (0, 0), "a")
    pb = PatternCell("b", "550", (0, 0), "b")
    # model_mock._data = [["a", "a", "b"], ["b", "b", "a"], ["a", "b", "a"]]
    model_mock._data = [[pa, pa, pb], [pb, pb, pa], [pa, pb, pa]]
    save_button = SaveButton(
        "Testing",
        model_mock,
        {LimiterType.ROW: [Modification(LimiterMode.NO_SELECTOR, [])],
         LimiterType.COLUMN: [Modification(LimiterMode.NO_SELECTOR, [])]},
        parent_mock
    )
    save_button.save_pattern_variant()

    save_pattern_mock.assert_called_once_with(
        "Testing-row--col--variant", [["a", "a", "b"], ["b", "b", "a"], ["a", "b", "a"]])

    label_mock.assert_called_once_with("Successfully saved pattern as Testing-row--col--variant")
    parent_mock.assert_has_calls([call.addWidget(label_mock.return_value)])
