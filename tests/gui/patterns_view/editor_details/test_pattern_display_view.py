from unittest.mock import MagicMock, call, patch

from gui.patterns_view.editor_details.pattern_display_view import PatternDisplayView

FILE_LOC = "gui.patterns_view.editor_details.pattern_display_view"


@patch(f"{FILE_LOC}.PatternDisplayView.setModel")
def test_init_view(set_model_mock):
    model_mock = MagicMock()
    display_view = PatternDisplayView(model_mock, MagicMock())

    set_model_mock.assert_called_once_with(model_mock)
    model_mock.assert_has_calls([call.add_display(display_view)])

    assert display_view.horizontalHeader().defaultSectionSize() == 20
    assert display_view.verticalHeader().defaultSectionSize() == 20

    assert display_view.horizontalHeader().font().pointSize() == 8
    assert display_view.verticalHeader().font().pointSize() == 8
