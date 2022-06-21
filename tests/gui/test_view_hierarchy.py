from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.view_hierarchy import ViewHierarchy

FILE_LOC = "gui.view_hierarchy"


@patch(f"{FILE_LOC}.PatternSelectorLayout")
def test_init(layout_child_mock):
    layout_child_mock.return_value = QVBoxLayout()
    toolbar_ref = MagicMock()
    test_widget = ViewHierarchy(toolbar_ref)

    assert test_widget.layout().count() == 2

    layout_child_mock.assert_called_once_with(test_widget)
    # assert test_widget.currentIndex() == 0
    # Changed to reflect the temp hard coded call
    assert test_widget.currentIndex() == 1


@patch(f"{FILE_LOC}.PatternSelectorLayout")
@patch(f"{FILE_LOC}.PatternDisplayModel.load_from_pattern_file")
@patch(f"{FILE_LOC}.PatternViewTab")
def test_pattern_chosen(view_child_mock, model_mock, layout_child_mock):
    layout_child_mock.return_value = QVBoxLayout()
    view_child_mock.return_value = QWidget()
    toolbar_ref = MagicMock()

    test_widget = ViewHierarchy(toolbar_ref)

    test_widget.pattern_chosen("Testing")
    assert view_child_mock.called == 1
    assert test_widget.currentIndex() == 1
