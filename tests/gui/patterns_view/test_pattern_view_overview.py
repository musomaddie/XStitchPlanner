from unittest.mock import patch

from PyQt6.QtWidgets import QWidget, QGridLayout

from gui.patterns_view.pattern_view_overview import \
    PatternViewOverviewLayout


@patch("gui.patterns_view.pattern_view_overview.PatternDisplayOverlay")
def test_init(child_mock, qtbot):
    child_mock.return_value = QGridLayout()
    test_widget = QWidget()
    test_widget.setLayout(PatternViewOverviewLayout("Testing"))
    qtbot.addWidget(test_widget)

    child_mock.assert_called_once_with(test_widget.layout())
    assert test_widget.layout().count() == 2
    assert test_widget.layout().pattern_title.text() == "Testing"
