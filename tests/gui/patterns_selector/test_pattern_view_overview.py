from PyQt6.QtWidgets import QWidget

from gui.patterns_selector.pattern_view_overview import \
    PatternViewOverviewLayout


def test_init(qtbot):
    # TODO: setup method??
    test_widget = QWidget()
    test_widget.setLayout(PatternViewOverviewLayout("Testing"))
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 1
    assert test_widget.layout().pattern_title.text() == "Testing"
