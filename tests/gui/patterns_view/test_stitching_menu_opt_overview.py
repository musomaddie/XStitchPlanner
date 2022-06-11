from PyQt6.QtWidgets import QWidget

from gui.patterns_view.stitching_opt_menu_overview import \
    StitchingOptMenuOverview


def test_init(qtbot):
    test_widget = QWidget()
    opt_menu = StitchingOptMenuOverview()
    test_widget.setLayout(opt_menu)
    qtbot.addWidget(test_widget)

    assert opt_menu.parent is None
