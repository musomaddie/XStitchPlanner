# Modification tests
from unittest.mock import ANY, MagicMock, call, patch

import pytest
from PyQt6.QtWidgets import QLabel
from allpairspy import AllPairs
from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import (
    LimiterCurrentlyApplied, Modification)

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.limiter_type import LimiterType

FILE_LOC = "old_gui.patterns_view.modifications.general_limiters.limiter_currently_applied"


@pytest.mark.parametrize("direction", list(LimiterType))
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied.addWidget")
@patch(f"{FILE_LOC}.LimitApplier")
def test_init(limiter_applier_mock, add_widget_mock, qlabel_mock, direction):
    model_mock = MagicMock()
    current_mods = [Modification(LimiterMode.NO_SELECTOR, [])]

    cur_applied = LimiterCurrentlyApplied(model_mock, direction, current_mods)

    qlabel_mock.assert_has_calls([call("Limits Currently Applied:"), call("None")])
    limiter_applier_mock.assert_called_once_with(direction, model_mock._data, current_mods)
    add_widget_mock.assert_has_calls(
        [call(qlabel_mock.return_value), call(qlabel_mock.return_value)])

    assert cur_applied.applier == limiter_applier_mock.return_value
    assert cur_applied.current_mods == {current_mods[0]: qlabel_mock.return_value}


@pytest.mark.parametrize(
    ("direction", "current_mods"),
    [values for values in AllPairs(
        [list(LimiterType),
         [[Modification(LimiterMode.NO_SELECTOR, [])],
          [Modification(LimiterMode.FROM, [2]), Modification(LimiterMode.TO, [3])],
          [Modification(LimiterMode.BETWEEN, [3, 4]),
           Modification(LimiterMode.TO, [2]),
           Modification(LimiterMode.FROM, [6])]]
         ])]
)
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied.addWidget")
@patch(f"{FILE_LOC}.LimitApplier")
def test_get_all_modifiers(applier_mock, add_widget_mock, qlabel_mock, direction, current_mods):
    model_mock = MagicMock()
    cur_app = LimiterCurrentlyApplied(model_mock, direction, current_mods)
    assert cur_app.get_all_modifiers() == current_mods


@pytest.mark.parametrize(
    ("mode", "values"),
    [(LimiterMode.BETWEEN, [3, 4]),
     (LimiterMode.FROM, [100]),
     (LimiterMode.TO, [100])]
)
@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied.addWidget")
@patch(f"{FILE_LOC}.LimitApplier")
def test_add_modification(applier_mock, add_widget_mock, qlabel_mock, mode, values):
    parent_mock = MagicMock()
    original_mod = [Modification(LimiterMode.NO_SELECTOR, [])]
    cur_app = LimiterCurrentlyApplied(
        MagicMock(), LimiterType.COLUMN, original_mod, parent_mock)
    created_mod = Modification(mode, values)
    cur_app.add_modification(mode, values)

    assert applier_mock.mock_calls == [call(ANY, ANY, original_mod),
                                       call().apply_limit(created_mod)]
    assert parent_mock.mock_calls == [call.create_new_pattern_tab(ANY, [created_mod])]


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied.addWidget")
@patch(f"{FILE_LOC}.LimitApplier")
def test_add_modification_multiple(applier_mock, add_widget_mock, qlabel_mock):
    parent_mock = MagicMock()
    original_mod = [Modification(LimiterMode.NO_SELECTOR, [])]
    cur_app = LimiterCurrentlyApplied(
        MagicMock(), LimiterType.COLUMN, original_mod, parent_mock)

    created_mod_1 = Modification(LimiterMode.FROM, [2])
    created_mod_2 = Modification(LimiterMode.TO, [5])
    cur_app.add_modification(LimiterMode.FROM, [2])
    # Manually updating  the cur_mods list as the full create_new_pattern_tab is not called only
    # mocked
    cur_app.current_mods = {created_mod_1: QLabel(created_mod_1.generate_label_str())}
    cur_app.add_modification(LimiterMode.TO, [5])

    assert applier_mock.mock_calls == [call(ANY, ANY, original_mod),
                                       call().apply_limit(created_mod_1),
                                       call().apply_limit(created_mod_2)]
    assert parent_mock.mock_calls == [
        call.create_new_pattern_tab(ANY, [created_mod_1]),
        call.create_new_pattern_tab(ANY, [created_mod_1, created_mod_2])]


@patch(f"{FILE_LOC}.QLabel")
@patch(f"{FILE_LOC}.LimiterCurrentlyApplied.addWidget")
@patch(f"{FILE_LOC}.LimitApplier")
def test_multiple_mods_init(applier_mock, add_widget_mock, qlabel_mock):
    model_mock = MagicMock()
    current_mods = [Modification(LimiterMode.TO, [6]),
                    Modification(LimiterMode.FROM, [2])]

    cur_applied = LimiterCurrentlyApplied(model_mock, LimiterType.COLUMN, current_mods)
    applier_mock.assert_called_once_with(LimiterType.COLUMN, model_mock._data, current_mods)
    add_widget_mock.assert_has_calls(
        [call(qlabel_mock.return_value),
         call(qlabel_mock.return_value),
         call(qlabel_mock.return_value)]
    )
    assert cur_applied.current_mods == {current_mods[0]: qlabel_mock.return_value,
                                        current_mods[1]: qlabel_mock.return_value}
