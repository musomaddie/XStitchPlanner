import pytest

from pattern_modifiers.limiters.limiter_mode import LimiterMode
from pattern_modifiers.limiters.modification import Modification

FILE_LOC = "pattern_modifiers.limiters.modification"


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


@pytest.mark.parametrize(
    ("mod", "expected_string"),
    [(Modification(LimiterMode.NO_SELECTOR, []), "NO ()"),
     (Modification(LimiterMode.BETWEEN, [2, 3]), "BETWEEN (2, 3)"),
     (Modification(LimiterMode.FROM, [1]), "FROM (1)"),
     (Modification(LimiterMode.TO, [6]), "TO (6)")]
)
def test_repr(mod, expected_string):
    assert mod.__repr__() == expected_string
