""" This file contains any common utils that are required by both the shape key
extractor and the pattern key extractor. (Within reason).
"""

def bbox_to_ident(page, bbox):
    """ Given a symbol in the PDF made up of lines and curves and
    transforms it into a string that will be consistently recognised as an
    identifier across the pattern.

    Parameters:
        page:   pdfplumber.Page     the page we are interested in.
        bbox:                       the bounding box containing the symbol.
    Returns:
        ident:  string      the string identifier generated from the list
                            of lines and curves.
    """
    def objs_ident(objs, prefix):
        return [
            prefix + "".join(sorted(
                [f"x{int(x - obj['x0'])}y{int(y - obj['y0'])}"
                    for x, y in obj['pts']])) for obj in objs]
    page_sect = page.within_bbox(bbox)
    return "-".join(sorted(
        objs_ident(page_sect.curves, "c") + objs_ident(
            page_sect.lines, "l")))
