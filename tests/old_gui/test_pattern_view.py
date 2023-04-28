from unittest.mock import MagicMock, call, patch

from gui.pattern_view import PatternView

FILE_LOC = "old_gui.pattern_view"


@patch(f"{FILE_LOC}.PatternView.setModel")
def test_init(set_model_mock, qtbot):
    # Crashes without including qtbot
    model_mock = MagicMock()
    display_view = PatternView(model_mock)
    #
    set_model_mock.assert_called_once_with(model_mock)
    model_mock.assert_has_calls([call.add_display(display_view)])

    assert display_view.horizontalHeader().defaultSectionSize() == 20
    assert display_view.verticalHeader().defaultSectionSize() == 20

    assert display_view.horizontalHeader().font().pointSize() == 8
    assert display_view.verticalHeader().font().pointSize() == 8
