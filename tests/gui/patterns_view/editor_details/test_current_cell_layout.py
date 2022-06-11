from PyQt6.QtWidgets import QWidget

from gui.patterns_view.editor_details.current_cell_layout import \
    CurrentCellLayout


def test_init(qtbot):
    test_widget = QWidget()
    current_cell_lay = CurrentCellLayout()
    test_widget.setLayout(current_cell_lay)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 3
