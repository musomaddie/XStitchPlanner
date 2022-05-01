from extractors.key_extractors.key_layout import KeyForm, KeyLayout

import pytest

@pytest.fixture
def key_layout():
    return KeyLayout(KeyForm.NO_LINES,
                     1, 2, 3, 4, 1, ["Symbol", "Number", "Colours"])


def test_KeyLayoutInit(key_layout):

    assert key_layout.key_form == KeyForm.NO_LINES
    assert key_layout.n_rows_start == 1
    assert key_layout.n_rows_end == 2
    assert key_layout.n_rows_start_pages == 3
    assert key_layout.n_rows_end_pages == 4
    assert key_layout.n_colours_per_row == 1
    assert key_layout.headings == ["Symbol", "Number", "Colours"]


def test_KeyFormFromString():
    assert KeyForm.from_string("full lines") == KeyForm.FULL_LINES
    assert KeyForm.from_string("only header line") == KeyForm.ONLY_HEADER_LINE
    assert KeyForm.from_string("no lines") == KeyForm.NO_LINES
    assert KeyForm.from_string("aghghgghg") == KeyForm.UNKNOWN

def test_KeyFormFromString_CaseInsensitive():
    assert KeyForm.from_string("FULL LINES") == KeyForm.FULL_LINES
    assert KeyForm.from_string("FuLl LiNeS") == KeyForm.FULL_LINES

def test_KeyFormFromString_PunctuationRemoved():
    assert KeyForm.from_string("full. lines!") == KeyForm.FULL_LINES
    assert KeyForm.from_string("!@#$%^&*()full lines") == KeyForm.FULL_LINES

def test_KeyFormFromString_WhitespaceRemoved():
    assert KeyForm.from_string("full    lines") == KeyForm.FULL_LINES
    assert KeyForm.from_string(" full lines ") == KeyForm.FULL_LINES
