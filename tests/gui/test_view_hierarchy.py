from unittest.mock import patch, MagicMock

from PyQt6.QtWidgets import QVBoxLayout

from gui.view_hierarchy import ViewHierarchy


@patch("gui.view_hierarchy.PatternSelectorLayout")
def test_init(layout_child_mock, qtbot):
    layout_child_mock.return_value = QVBoxLayout()
    toolbar_ref = MagicMock()
    test_widget = ViewHierarchy(toolbar_ref)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 2

    layout_child_mock.assert_called_once_with(test_widget)
    assert test_widget.currentIndex() == 0


@patch("gui.view_hierarchy.PatternSelectorLayout")
@patch("gui.view_hierarchy.PatternDisplayModel.load_from_pattern_file")
@patch("gui.view_hierarchy.PatternViewOverviewLayout")
def test_pattern_chosen(view_child_mock, model_mock, layout_child_mock, qtbot):
    layout_child_mock.return_value = QVBoxLayout()
    view_child_mock.return_value = QVBoxLayout()
    toolbar_ref = MagicMock()

    test_widget = ViewHierarchy(toolbar_ref)
    qtbot.addWidget(test_widget)

    test_widget.pattern_chosen("Testing")
    assert view_child_mock.called == 1
    assert test_widget.currentIndex() == 1
