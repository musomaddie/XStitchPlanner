from PyQt6.QtWidgets import QWidget

from gui.patterns_view.pattern_display_overlay import PatternDisplayOverlay


def test_init(qtbot):
    test_widget = QWidget()
    test_widget.setLayout(PatternDisplayOverlay())
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 0
