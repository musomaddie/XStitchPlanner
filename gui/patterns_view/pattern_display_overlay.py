from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_editor_view import PatternEditorView
from gui.patterns_view.stitching_opt_menu_overview import StitchingOptMenuOverview
from pattern_cell import PatternCell


class PatternDisplayOverlay(QHBoxLayout):
    """ Wraps all the different elements required for viewing the pattern.

   +-------------------------------------------------------------------+
   |                                                    |   STITCHING  |
   |        PATTERN EDITOR                              |   OPTIONS    |
   |                                                    |   MENU       |
   +-------------------------------------------------------------------+
   """
    pattern_title: str
    parent: 'PatternViewTabContents'
    editor: PatternEditorView
    model: 'PatternDisplayModel'
    opt_menu: StitchingOptMenuOverview

    def __init__(
            self,
            pattern_name: str,
            model: 'PatternDisplayModel',
            current_mod: 'Modification',
            parent: 'PatternViewTabContents' = None):
        super().__init__()

        self.pattern_title = pattern_name
        self.parent = parent
        self.model = model
        self.editor = PatternEditorView(pattern_name, self.model, self)
        editor_layout_widget = QWidget()
        editor_layout_widget.setLayout(self.editor)
        self.addWidget(editor_layout_widget)

        self.opt_menu = StitchingOptMenuOverview(
            self.editor.get_current_cell_layout(), self.model, current_mod, self)
        opt_menu_layout_widget = QWidget()
        opt_menu_layout_widget.setLayout(self.opt_menu)
        # TODO: make the width a bit more dynamic
        # TODO: make this hide / show with a button (animations?)
        opt_menu_layout_widget.setMaximumSize(
            QSize(300, opt_menu_layout_widget.size().height()))
        self.addWidget(opt_menu_layout_widget)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modification: 'Modification') -> None:
        self.parent.create_new_pattern_tab(self.pattern_title, new_model, modification)
