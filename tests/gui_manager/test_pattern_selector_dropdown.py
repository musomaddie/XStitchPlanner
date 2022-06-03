import pytest

from unittest.mock import patch

from gui.patterns_ui.pattern_selector_dropdown import find_all_patterns


@pytest.mark.parametrize(
    ("pat_files", "key_files", "expected_pattern_names"),
    ((["first_file.pat", "second_file.pat"], ["first_file.key", "second_file.key"],
      ["first_file", "second_file"]),
     (["first_file.pat", "second_file.pat"], ["first_file.key"], ["first_file"]),
     (
     ["first_file.pat"], ["first_file.key", "second_file.key"], ["first_file"]),
     (["first_file.pat"], ["second_file.key"], [])
     ))
@patch("gui.patterns.pattern_selector.listdir")
@patch("gui.patterns.pattern_selector.isfile")
def test_find_all_patterns(isfile_mock, listdir_mock,
                           pat_files, key_files, expected_pattern_names):
    isfile_mock.return_value = True
    listdir_mock.return_value = pat_files + key_files
    result = find_all_patterns()

    assert len(result) == len(expected_pattern_names)
    for expected in expected_pattern_names:
        assert expected in result