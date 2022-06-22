# Modification tests
import pytest
from PyQt6.QtWidgets import QLabel, QWidget

from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import \
    (
    LimiterCurrentlyApplied, Modification)
from gui.patterns_view.modifications.general_limiters.limiter_direction import LimiterDirection
from gui.patterns_view.modifications.general_limiters.limiter_mode import LimiterMode


@pytest.mark.parametrize(
    ("mode, values"),
    [(LimiterMode.NO_SELECTOR, []),
     (LimiterMode.BETWEEN, [1, 2]),
     (LimiterMode.FROM, [6]),
     (LimiterMode.TO, [45]),
     (LimiterMode.BETWEEN, [4, 3])]  # Should be passed in ordered value in practice but checking
)
def test_mod_init(mode, values):
    mod = Modification(mode, values)
    assert mod.mode == mode
    sorted_vals = sorted(values)
    assert mod.values == sorted_vals


@pytest.mark.parametrize(
    ("mode", "values", "expected_string"),
    [(LimiterMode.NO_SELECTOR, [], "None"),
     (LimiterMode.BETWEEN, [3, 4], "Between 4 and 5"),
     (LimiterMode.FROM, [20], "From: 21"),
     (LimiterMode.TO, [3], "To: 4")]
)
def test_mod_generate_label_str(mode, values, expected_string):
    mod = Modification(mode, values)
    assert mod.generate_label_str() == expected_string


@pytest.mark.parametrize(
    ("mode", "values"),
    [(LimiterMode.NO_SELECTOR, []),
     (LimiterMode.BETWEEN, [3, 4]),
     (LimiterMode.FROM, [4]),
     (LimiterMode.TO, [3])]
)
def test_mod_hash(mode, values):
    mod = Modification(mode, values)
    value_string = "".join([str(v) for v in values])
    assert mod.__hash__() == hash((mode, value_string))


def test_mod_eq():
    m1 = Modification(LimiterMode.NO_SELECTOR, [])
    m2 = Modification(LimiterMode.NO_SELECTOR, [])
    assert m1 == m2

    assert Modification(LimiterMode.FROM, [2]) != Modification(LimiterMode.TO, [2])
    assert Modification(LimiterMode.BETWEEN, [2, 3]) == Modification(LimiterMode.BETWEEN, [2, 3])
    assert Modification(LimiterMode.BETWEEN, [2, 3]) != Modification(LimiterMode.BETWEEN, [3, 4])
    assert Modification(LimiterMode.FROM, [2]) == Modification(LimiterMode.FROM, [2])
    assert Modification(LimiterMode.TO, [3]) == Modification(LimiterMode.TO, [3])


# Layout
@pytest.mark.parametrize("direction", list(LimiterDirection))
def test_init(direction):
    cur_app = LimiterCurrentlyApplied(direction)
    assert cur_app.direction == direction
    assert cur_app.parent is None
    assert len(cur_app.current_mods) == 1
    assert list(cur_app.current_mods.keys())[0].mode == LimiterMode.NO_SELECTOR
    assert cur_app.count() == 2

    test_widget = QWidget()
    test_widget.setLayout(cur_app)
    assert test_widget.children()[1].text() == "Limits Currently Applied:"


@pytest.mark.parametrize(
    ("mode", "values"),
    [(LimiterMode.NO_SELECTOR, [2]),
     (LimiterMode.BETWEEN, [3, 4]),
     (LimiterMode.FROM, [100]),
     (LimiterMode.TO, [100])]
)
def test_add_modification(mode, values):
    cur_app = LimiterCurrentlyApplied(LimiterDirection.COLUMN)
    created_mod = Modification(mode, values)
    cur_app.add_modification(mode, values)

    assert len(cur_app.current_mods) == 2
    assert created_mod in cur_app.current_mods
    assert type(cur_app.current_mods[created_mod]) == QLabel
    assert cur_app.current_mods[created_mod].text() == created_mod.generate_label_str()

    assert cur_app.count() == 3


def test_add_modification_multiple():
    cur_app = LimiterCurrentlyApplied(LimiterDirection.COLUMN)

    cur_app.add_modification(LimiterMode.FROM, [2])
    cur_app.add_modification(LimiterMode.TO, [5])
    created_mod_1 = Modification(LimiterMode.FROM, [2])
    created_mod_2 = Modification(LimiterMode.TO, [5])

    assert len(cur_app.current_mods) == 3
    assert cur_app.count() == 4
    assert created_mod_1 in cur_app.current_mods
    assert created_mod_2 in cur_app.current_mods
    assert cur_app.current_mods[created_mod_1].text() == created_mod_1.generate_label_str()
    assert cur_app.current_mods[created_mod_2].text() == created_mod_2.generate_label_str()
