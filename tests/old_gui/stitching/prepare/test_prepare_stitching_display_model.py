from gui.stitching.prepare.prepare_stitching_display_model import PrepareStitchingDisplayModel
from pattern_cells.pattern_cell import PatternCell

TESTING_DATA_3_2 = [
    [PatternCell("a", "310", (0, 0), "000000"),
     PatternCell("a", "310", (0, 1), "000000"),
     PatternCell("b", "666", (0, 2), "FF0000")],
    [PatternCell("b", "666", (1, 0), "FF0000"),
     PatternCell("b", "666", (1, 1), "FF0000"),
     PatternCell("a", "310", (1, 2), "000000")]]


def test_init():
    model = PrepareStitchingDisplayModel(TESTING_DATA_3_2)
    assert model._data == TESTING_DATA_3_2
    assert model.display is None
    assert model.show_colours
