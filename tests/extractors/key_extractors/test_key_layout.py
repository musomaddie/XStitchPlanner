import pytest

from extractors.key_extractors.key_layout import KeyForm, KeyLayout


@pytest.fixture
def key_layout():
    return KeyLayout(KeyForm.NO_LINES, 1, 2, 3, 4, 1, ["Symbol", "Number", "Colours"])


def test_key_layout_init(key_layout):
    assert key_layout.key_form == KeyForm.NO_LINES
    assert key_layout.n_rows_start == 1
    assert key_layout.n_rows_end == 2
    assert key_layout.n_rows_start_pages == 3
    assert key_layout.n_rows_end_pages == 4
    assert key_layout.n_colours_per_row == 1
    assert key_layout.headings == ["Symbol", "Number", "Colours"]


@pytest.mark.parametrize(
    ("fline", "hline", "nline", "unknown"),
    [("full lines", "only header line", "no lines", "aghhghghghg"),
     ("FULL LINES", "oNlY hEaDeR lInE", "no LINES", "AAAAAAAAAAAAAAA"),
     ("full lines!", ".only.header.line.", "!@#&%^&*()no!l!i!n!es,,,,,,,", ""),
     ("full     lines", " only header line ", "no  lines", "")]
)
def test_key_form_from_string(fline, hline, nline, unknown):
    assert KeyForm.from_string(fline) == KeyForm.FULL_LINES
    assert KeyForm.from_string(hline) == KeyForm.ONLY_HEADER_LINE
    assert KeyForm.from_string(nline) == KeyForm.NO_LINES
    assert KeyForm.from_string(unknown) == KeyForm.UNKNOWN
