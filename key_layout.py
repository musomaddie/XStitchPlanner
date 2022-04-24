from dataclasses import dataclass

@dataclass
class KeyLayout:
    """ A dataclass for storing information about the layout of the key.
    n_rows_start        int     the row where the key starts on the first page
    n_rows_end          int     the row where the key stops on the first page
    n_rows_start_pages  int     the number of the row where the key starts for
                                the pages that aren't the first page. 0 if this
                                is not a multi-page key.
    n_rows_end_pages    int     the row where the key ends for pages that
                                aren't the first page. 0 if this is not a
                                multi-page key.
    headings            list[str]   an ordered list of every heading in the key
                                    column.
    """
    n_rows_start: int
    n_rows_end: int
    n_rows_start_pages: int
    n_rows_end_pages: int
    n_colours_per_row: int
    headings: list[str]
