from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.editor_details.pattern_display_view import \
    PatternDisplayView

TESTING_DATA_3_3 = [['a', 'a', 'b'], ['b', 'b', 'c'], ['c', 'c', 'a']]


def test_init_view(qtbot):
    # TODO: I need a model
    model = PatternDisplayModel(TESTING_DATA_3_3)
    test_widget = PatternDisplayView("TESTING", model)
    qtbot.addWidget(test_widget)

    assert test_widget.pattern_name == "TESTING"
    assert test_widget.model == model

    assert test_widget.horizontalHeader().font().pointSize() == 8
