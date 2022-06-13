from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_editor_view import PatternEditorView
from gui.patterns_view.stitching_opt_menu_overview import (
    StitchingOptMenuOverview)


class PatternDisplayOverlay(QHBoxLayout):
    """ Wraps all the different elements required for viewing the pattern.

   +-------------------------------------------------------------------+
   |                                                    |   STITCHING  |
   |        PATTERN EDITOR                              |   OPTIONS    |
   |                                                    |   MENU       |
   +-------------------------------------------------------------------+
   """
    pattern_title: str
    parent: 'ViewHierarchy'
    editor: PatternEditorView
    model: 'PatternDisplayModel'
    opt_menu: StitchingOptMenuOverview

    def __init__(
            self,
            pattern_name: str,
            pattern_model: 'PatternDisplayModel',
            parent: 'ViewHierarchy' = None):
        super().__init__()

        self.parent = parent
        self.model = pattern_model  # TODO: rename consistency to model
        self.editor = PatternEditorView(pattern_name, self.model, self)
        editor_layout_widget = QWidget()
        editor_layout_widget.setLayout(self.editor)
        self.addWidget(editor_layout_widget)

        self.opt_menu = StitchingOptMenuOverview(self)
        opt_menu_layout_widget = QWidget()
        opt_menu_layout_widget.setLayout(self.opt_menu)
        # TODO: make the width a bit more dynamic
        opt_menu_layout_widget.setMaximumSize(
            QSize(200, opt_menu_layout_widget.size().height()))
        self.addWidget(opt_menu_layout_widget)
