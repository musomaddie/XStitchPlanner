from unittest.mock import call, patch

import pytest

from gui.patterns_view.modifications.variants_load_dropdown import VariantsLoadDropDown

FILE_LOC = "gui.patterns_view.modifications.variants_load_dropdown"


@patch(f"{FILE_LOC}.VariantsLoadDropDown.list_all_variants")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.addItems")
def test_init(add_items_mock, list_all_variants_mock):
    load_dropdown = VariantsLoadDropDown("testing")

    list_all_variants_mock.assert_called_once()
    add_items_mock.assert_called_once_with([])

    assert load_dropdown.original_pattern_name == "testing"
    assert load_dropdown.all_variants == list_all_variants_mock.return_value


@pytest.mark.parametrize(
    ("all_files", "expected_files"),
    [(["testing.pat",
       "testing--row--col--variant.pat",
       "testing-row-from[5]-col--variant.pat",
       "testing-row--col-between[2_3]-variant.pat",
       "testing-row-from[5]to[12]-col-from[3]to[5].pat"],
      ["testing-row-from[5]-col--variant",
       "testing-row--col-between[2_3]-variant",
       "testing-row-from[5]to[12]-col-from[3]to[5]"]),
     (["testing.pat"], []),
     (["testing.pat", "testing-not-a-pat-file"], []),
     (["testing.pat", "testing-row-from[5]-col--variant.pat"],
      ["testing-row-from[5]-col--variant"])]
)
@patch(f"{FILE_LOC}.VariantsLoadDropDown.addItems")
@patch(f"{FILE_LOC}.listdir")
@patch(f"{FILE_LOC}.isfile")
def test_find_all_variants(
        isfile_mock, listdir_mock, add_items_mock, all_files, expected_files):
    isfile_mock.return_value = True
    listdir_mock.return_value = all_files
    variants_dropdown = VariantsLoadDropDown("testing")
    assert variants_dropdown.find_all_variants_filenames() == expected_files


@pytest.mark.parametrize(
    ("variant_filename", "expected"),
    [("testing-row-from[5]-col--variant", "From row 5"),
     ("testing-row--col-from[5]-variant", "From column 5"),
     ("testing-row-from[3]to[10]-col--variant", "From row 3 to row 10"),
     ("testing-row--col-between[1_12]-variant", "Between columns 1 and 12"),
     ("testing-row-between[2_22]-col--variant", "Between rows 2 and 22"),
     ("testing-row-from[6]-col-to[3]-variant", "From row 6, to column 3")]
)
@patch(f"{FILE_LOC}.VariantsLoadDropDown.addItems")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.list_all_variants")
def test_make_label_text(list_all_variants_mock, add_items_mock, variant_filename, expected):
    variants_dropdown = VariantsLoadDropDown("testing")
    assert variants_dropdown.make_label_text(variant_filename) == expected


@patch(f"{FILE_LOC}.VariantsLoadDropDown.addItems")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.make_label_text")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.find_all_variants_filenames")
def test_list_all_variants(find_all_vars_fn_mock, make_label_text_mock, add_items_mock):
    # Adding return values, so I can check the dict at the end
    make_label_text_mock.side_effect = ["1", "2"]
    find_all_vars_fn_mock.side_effect = (
        [], ["testing-row-from[5]-col--variant", "testing-row--col-from[5]-variant"])

    variants_dropdown = VariantsLoadDropDown("testing")
    resulting_dict = variants_dropdown.list_all_variants()
    make_label_text_mock.assert_has_calls(
        [call("testing-row-from[5]-col--variant"),
         call("testing-row--col-from[5]-variant")])
    find_all_vars_fn_mock.assert_has_calls([call(), call()])

    assert len(resulting_dict) == 2
    assert "1" in resulting_dict
    assert "2" in resulting_dict


@patch(f"{FILE_LOC}.VariantsLoadDropDown.addItems")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.list_all_variants")
@patch(f"{FILE_LOC}.load_from_pattern_file")
@patch(f"{FILE_LOC}.VariantsLoadDropDown.currentText")
def test_get_pattern_model_from_selected_file(
        current_text_mock, load_from_pattern_file_mock, list_all_mock, add_items_mock):
    list_all_mock.return_value = {"From row 5": "testing-row-from[5]-col--variant"}
    current_text_mock.return_value = "From row 5"

    variants_dropdown = VariantsLoadDropDown("testing")
    variants_dropdown.get_pattern_model_from_selected_variant()

    load_from_pattern_file_mock.assert_called_once_with(
        "testing", "testing-row-from[5]-col--variant")
