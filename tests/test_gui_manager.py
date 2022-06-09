from unittest.mock import patch

from PyQt6.QtWidgets import QStackedWidget

import resources.gui_strings as s
from gui_manager import MainWindow


@patch("gui_manager.ViewHierarchy")
def test_init(view_hier_mock, qtbot):
    # TODO: I should be able to test the toolbar now that it no longer seg
    #  faults
    view_hier_mock.return_value = QStackedWidget()
    test_widget = MainWindow()
    qtbot.addWidget(test_widget)

    assert test_widget.windowTitle() == s.program_title()
    assert test_widget.layout().count() == 2

    view_hier_mock.assert_called_once_with(test_widget.toolbar, test_widget)

    pass
