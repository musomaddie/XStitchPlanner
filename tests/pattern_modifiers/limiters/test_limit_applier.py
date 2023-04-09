import pytest

from gui.patterns_view.modifications.general_limiters.limiter_currently_applied import Modification
from pattern_cells.pattern_cell import PatternCell
from pattern_modifiers.limiters.limit_applier import LimitApplier
from pattern_modifiers.limiters.limiter_direction import LimiterType
from pattern_modifiers.limiters.limiter_mode import LimiterMode


@pytest.fixture()
def pattern():
    """ 3x3 pattern
    A A D
    A B D
    B B D
    """
    return [
        [PatternCell("A", "310", (0, 0), ""), PatternCell("A", "310", (1, 0), ""),
         PatternCell("D", "666", (2, 0), "")],
        [PatternCell("A", "310", (0, 1), ""), PatternCell("B", "550", (1, 1), ""),
         PatternCell("D", "666", (2, 1), "")],
        [PatternCell("B", "550", (0, 2), ""), PatternCell("B", "550", (1, 2), ""),
         PatternCell("D", "666", (2, 2), "")]
    ]


@pytest.fixture()
def og_mod():
    return Modification(LimiterMode.NO_SELECTOR, [])


@pytest.fixture()
def applier_larger_pattern(direction, og_mod):
    """
    Pattern is:
    ABBA
    BAAB
    DDDD
    DABD
   """
    return LimitApplier(
        direction,
        [[PatternCell("A", "", (0, 0), ""), PatternCell("B", "", (1, 0), ""),
          PatternCell("B", "", (2, 0), ""), PatternCell("A", "", (3, 0), "")],
         [PatternCell("B", "", (0, 1), ""), PatternCell("A", "", (1, 1), ""),
          PatternCell("A", "", (2, 1), ""), PatternCell("B", "", (3, 1), "")],
         [PatternCell("D", "", (0, 2), ""), PatternCell("D", "", (1, 2), ""),
          PatternCell("D", "", (2, 2), ""), PatternCell("D", "", (3, 2), "")],
         [PatternCell("D", "", (0, 3), ""), PatternCell("A", "", (1, 3), ""),
          PatternCell("B", "", (2, 3), ""), PatternCell("D", "", (3, 3), "")]], [og_mod])


@pytest.fixture()
def applier(pattern, og_mod, direction):
    return LimitApplier(direction, pattern, [og_mod])


@pytest.mark.parametrize("direction", list(LimiterType))
def test_init(pattern, og_mod, applier):
    assert applier.currently_applied == [og_mod]
    assert applier.original_pattern == pattern
    assert applier.pattern_current_state == pattern
    assert applier.pattern_current_state == applier.original_pattern

    # Confirm copy
    pattern[0][0].display_symbol = "B"
    assert pattern[0][0].display_symbol == "B"
    assert applier.original_pattern[0][0].display_symbol == "A"
    assert applier.original_pattern != pattern

    applier.original_pattern[0][1].display_symbol = "C"
    assert pattern[0][1].display_symbol != "C"
    assert applier.pattern_current_state[0][1].display_symbol != "C"
    assert applier.original_pattern != applier.pattern_current_state


@pytest.mark.parametrize("direction", list(LimiterType))
def test_apply_limit_from(applier):
    pat = applier.apply_limit(Modification(LimiterMode.FROM, [1]))

    assert pat == applier.pattern_current_state
    assert len(applier.currently_applied) == 1
    assert applier.currently_applied[0] == Modification(LimiterMode.FROM, [1])

    if applier.direction == LimiterType.ROW:
        assert len(pat) == 2
        assert len(pat[0]) == 3
        assert "".join([c.display_symbol for c in pat[0]]) == "ABD"
        assert "".join([c.display_symbol for c in pat[1]]) == "BBD"
    else:
        assert len(pat) == 3
        assert len(pat[0]) == 2
        assert "".join([c.display_symbol for c in pat[0]]) == "AD"
        assert "".join([c.display_symbol for c in pat[1]]) == "BD"
        assert "".join([c.display_symbol for c in pat[2]]) == "BD"


@pytest.mark.parametrize("direction", list(LimiterType))
def test_apply_limit_no_selections(pattern, applier):
    applier.apply_limit(Modification(LimiterMode.TO, [2]))
    pat = applier.apply_limit(Modification(LimiterMode.NO_SELECTOR, []))

    assert pat == pattern
    assert applier.pattern_current_state == applier.original_pattern
    applier.pattern_current_state[0][0].display_symbol = "C"
    assert pat != applier.pattern_current_state


@pytest.mark.parametrize("direction", list(LimiterType))
def test_apply_limit_to(applier):
    pat = applier.apply_limit(Modification(LimiterMode.TO, [1]))

    assert pat == applier.pattern_current_state
    assert len(applier.currently_applied) == 1
    assert applier.currently_applied[0] == Modification(LimiterMode.TO, [1])

    if applier.direction == LimiterType.ROW:
        assert len(pat) == 2
        assert len(pat[0]) == 3
        assert "".join([c.display_symbol for c in pat[0]]) == "AAD"
        assert "".join([c.display_symbol for c in pat[1]]) == "ABD"
    else:
        assert len(pat) == 3
        assert len(pat[0]) == 2
        assert "".join([c.display_symbol for c in pat[0]]) == "AA"
        assert "".join([c.display_symbol for c in pat[1]]) == "AB"
        assert "".join([c.display_symbol for c in pat[2]]) == "BB"


@pytest.mark.parametrize("direction", list(LimiterType))
def test_apply_limit_between(applier_larger_pattern):
    mod = Modification(LimiterMode.BETWEEN, [1, 2])
    pat = applier_larger_pattern.apply_limit(mod)

    assert pat == applier_larger_pattern.pattern_current_state
    assert len(applier_larger_pattern.currently_applied) == 1
    assert applier_larger_pattern.currently_applied[0] == mod

    if applier_larger_pattern.direction == LimiterType.ROW:
        assert len(pat) == 2
        assert len(pat[0]) == 4
        assert "".join([c.display_symbol for c in pat[0]]) == "BAAB"
        assert "".join([c.display_symbol for c in pat[1]]) == "DDDD"
    else:
        assert len(pat) == 4
        assert len(pat[0]) == 2
        assert "".join([c.display_symbol for c in pat[0]]) == "BB"
        assert "".join([c.display_symbol for c in pat[1]]) == "AA"
        assert "".join([c.display_symbol for c in pat[2]]) == "DD"
        assert "".join([c.display_symbol for c in pat[3]]) == "AB"


@pytest.mark.parametrize("direction", list(LimiterType))
def test_apply_multiple_limits(applier_larger_pattern):
    mod_1 = Modification(LimiterMode.TO, [2])
    mod_2 = Modification(LimiterMode.FROM, [1])

    applier_larger_pattern.apply_limit(mod_1)
    pat = applier_larger_pattern.apply_limit(mod_2)

    assert len(applier_larger_pattern.currently_applied) == 2
    assert applier_larger_pattern.currently_applied == [mod_1, mod_2]

    if applier_larger_pattern.direction == LimiterType.ROW:
        assert len(pat) == 2
        assert len(pat[0]) == 4
        assert "".join([c.display_symbol for c in pat[0]]) == "BAAB"
        assert "".join([c.display_symbol for c in pat[1]]) == "DDDD"
    else:
        assert len(pat) == 4
        assert len(pat[0]) == 2
        assert "".join([c.display_symbol for c in pat[0]]) == "BB"
        assert "".join([c.display_symbol for c in pat[1]]) == "AA"
        assert "".join([c.display_symbol for c in pat[2]]) == "DD"
        assert "".join([c.display_symbol for c in pat[3]]) == "AB"
