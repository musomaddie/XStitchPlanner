from unittest.mock import MagicMock, call, patch

from gui.patterns_view.modifications.load_overlay import LoadOverlay

FILE_LOC = "gui.patterns_view.modifications.load_overlay"


@patch(f"{FILE_LOC}.VariantsLoadDropDown")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
@patch(f"{FILE_LOC}.QPushButton")
def test_init(button_mock, add_widget_mock, dropdown_mock):
    overlay = LoadOverlay("testing")

    dropdown_mock.assert_called_once_with("testing")
    button_mock.assert_called_once_with("Load This Variant")
    add_widget_mock.assert_has_calls(
        [call(dropdown_mock.return_value), call(button_mock.return_value)])

    assert overlay.variants_dropdown == dropdown_mock.return_value
    assert overlay.load_impl_button == button_mock.return_value


@patch(f"{FILE_LOC}.VariantsLoadDropDown")
@patch(f"{FILE_LOC}.LoadOverlay.addWidget")
@patch(f"{FILE_LOC}.QPushButton")
def test_load_variant(button_mock, add_widget_mock, dropdown_mock):
    parent_mock = MagicMock()
    overlay = LoadOverlay("testing", parent_mock)
    overlay.load_variant()

    dropdown_mock.assert_has_calls(
        [call("testing"), call().get_pattern_model_from_selected_variant()]
    )
    parent_mock.assert_has_calls(
        [call.create_new_pattern_variant_tab(
            dropdown_mock().get_pattern_model_from_selected_variant())])
