from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from gui.pattern_display_model import PatternDisplayModel
from gui.patterns_view.pattern_editor_view import PatternEditorView
from gui.patterns_view.stitching_opt_menu_overview import StitchingOptMenuOverview
from pattern_cell import PatternCell
from pattern_modifiers.limiters.limiter_direction import LimiterDirection


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
            current_mods: dict[LimiterDirection, list['Modification']],
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
            self.editor.get_current_cell_layout(), self.model, current_mods, self)
        opt_menu_layout_widget = QWidget()
        opt_menu_layout_widget.setLayout(self.opt_menu)
        # TODO: make the width a bit more dynamic
        # TODO: make this hide / show with a button (animations?)
        # TODO: update this to include the actual window size: getting the height of this widget
        #  is wrong -> drastically so
        opt_menu_layout_widget.setMaximumSize(
            QSize(300, opt_menu_layout_widget.maximumSize().height()))
        self.addWidget(opt_menu_layout_widget)

    def create_new_pattern_tab(
            self,
            new_model: list[list[PatternCell]],
            modifications: dict[LimiterDirection, list['Modification']]) -> None:
        self.parent.create_new_pattern_tab(new_model, modifications)
