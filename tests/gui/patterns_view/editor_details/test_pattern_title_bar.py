from unittest.mock import MagicMock

from PyQt6.QtWidgets import QWidget

from gui.patterns_view.editor_details.pattern_title_bar import PatternTitleBar


def test_init(qtbot):
    mock_model = MagicMock()
    test_widget = QWidget()
    title_bar = PatternTitleBar("TESTING", mock_model)
    test_widget.setLayout(title_bar)
    qtbot.addWidget(test_widget)

    assert test_widget.layout().count() == 1
    assert title_bar.model == mock_model
