from unittest.mock import MagicMock, call

from PyQt6.QtWidgets import QMainWindow

from gui.pattern_view_toolbar import PatternViewToolBar


def test_init(qtbot):
    test_window = QMainWindow()
    toolbar = PatternViewToolBar()
    test_window.addToolBar(toolbar)
    qtbot.addWidget(test_window)

    assert toolbar.parent is None
    assert toolbar.model is None
    assert toolbar.colour_on.text() == "Enable Colour Background"
    assert toolbar.colour_off.text() == "Disable Colour Background"


def test_model_on_triggered(qtbot):
    test_window = QMainWindow()
    toolbar = PatternViewToolBar()
    test_window.addToolBar(toolbar)
    qtbot.addWidget(test_window)

    model_mock = MagicMock()
    toolbar.pattern_chosen(model_mock)

    toolbar.colour_on.trigger()
    toolbar.colour_off.trigger()
    assert model_mock.mock_calls == [call.set_colour_mode(True),
                                     call.change_pattern_visible_gridlines(False),
                                     call.set_colour_mode(False),
                                     call.change_pattern_visible_gridlines(True)]
