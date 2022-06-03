from unittest.mock import patch

import pytest

from gui.patterns_layout.pattern_selector_dropdown import find_all_patterns


@pytest.mark.parametrize(
    ("pat_files", "key_files", "expected_pattern_names"),
    ((["first_file.pat", "second_file.pat"],
      ["first_file.key", "second_file.key"],
      ["first_file", "second_file"]),
     (["first_file.pat", "second_file.pat"],
      ["first_file.key"], ["first_file"]),
     (
             ["first_file.pat"], ["first_file.key", "second_file.key"],
             ["first_file"]),
     (["first_file.pat"], ["second_file.key"], [])
     ))
@patch("gui.patterns_layout.pattern_selector_dropdown.listdir")
@patch("gui.patterns_layout.pattern_selector_dropdown.isfile")
def test_find_all_patterns(isfile_mock, listdir_mock,
                           pat_files, key_files, expected_pattern_names):
    isfile_mock.return_value = True
    listdir_mock.return_value = pat_files + key_files
    result = find_all_patterns()

    assert len(result) == len(expected_pattern_names)
    for expected in expected_pattern_names:
        assert expected in result


@patch("gui.patterns_layout.pattern_selector_dropdown.listdir")
@patch("gui.patterns_layout.pattern_selector_dropdown.isfile")
def test_find_all_patterns_sorted(isfile_mock, listdir_mock):
    isfile_mock.return_value = True
    listdir_mock.return_value = [
        "b.pat", "c.pat", "d.pat", "e.pat", "a.pat",
        "b.key", "c.key", "d.key", "e.key", "a.key"]
    expected_names = ["a", "b", "c", "d", "e"]
    result = find_all_patterns()

    assert len(result) == len(expected_names)
    for actual, expected in zip(result, expected_names):
        assert actual == expected
