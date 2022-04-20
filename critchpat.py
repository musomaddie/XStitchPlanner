"""Cross Stitch Pattern Colorizer

Usage:
  critchpat.py extract [-v] [-m MODE] [-k PAGE | -K PATH] [-o OVERLAP] PDF WIDTH HEIGHT [STARTPAGE] [ENDPAGE]
  critchpat.py KEY PATTERN

Arguments:
  PDF         input pdf path
  WIDTH       width of pattern in stitches
  HEIGHT      height of pattern in stitches
  STARTPAGE   page number of first page of the pattern to parse [default: 1]
  ENDPAGE     page number of last page of the pattern to parse. If not provided and STARTPAGE is provided,
              parse only one page. If neither this nor STARTPAGE is provided, parse the whole PDF file.
  KEY         input file of tab-separated data where each row has symbol, dmc number, name, r, g, b
  PATTERN     input pattern where every character is a symbol in the key

Options:
  -h --help                     show this help message and exit
  -v --verbose                  print status messages
  -k PAGE --keypage=PAGE        attempt to extract the key from the given page number
  -K PATH --keypath=PATH        a file path to read the key from when extracting, used for "shape" mode only.
  -o OVERLAP --overlap=OVERLAP  number of rows/columns of overlap on each page to trim before concatenating pages
  -m MODE --mode=MODE           extraction mode, can be either "font" or "shape". [default: font]

  MODE:
    font:  The default extraction mode if MODE is not given. Identifies symbols in the pattern by extracting the
           text from the PDF.
    shape: Extract symbols from the PDF by attempting to identify and match reoccuring lines and shapes on the
           page. These identifiers are then matched up with arbitrary symbols for displaying in the pattern.
           This mode requires either --keypage or --keypath to also be given in order to generate the mapping
           of identifiers to symbols.
Examples:

  Extract a 300x400 pattern with text character symbols from all pages of pattern.pdf without generating a key
  critchpat.py extract -m shape pattern.pdf 300 400

  Extract a 300x400 pattern with text character symbols from all pages of pattern.pdf, and also extract a key from page 2
  critchpat.py extract -m shape -k 2 pattern.pdf 300 400

  Extract a 300x400 pattern with SVG shape object symbols from pages 2-10 of pattern.pdf using a key extracted from page 22
  critchpat.py extract -m shape -k 11 - pattern.pdf 300 400 2 10

  Extract a 300x400 pattern with SVG shape object symbols from all pages of pattern.pdf using a previously-generated key from key.tsv
  critchpat.py extract -m shape -K key.tsv - pattern.pdf 300 400
"""
from string import ascii_letters, punctuation
from io import BytesIO
from dataclasses import dataclass
from typing import Counter

import pdfplumber
from docopt import docopt
from PIL import Image
from domonic.html import *

@dataclass(order=True)
class Stitch:
    dmc_num: int
    name: str
    symbol: str
    rgb: tuple[int, int, int]

    def __post_init__(self):
        try:
            self.dmc_num = int(self.dmc_num)
        except ValueError:
            self.dmc_num = 0
        self.rgb = tuple(map(int, self.rgb))

        self.dmc_style = f".dmc{self.dmc_num} {{ background: rgb{self.rgb};"
        self.dmc_style += " }"
    
    @classmethod
    def default(self, symbol):
        return Stitch(0, "UNKNOWN", symbol, (255,255,255))

    def key_row(self):
        return tr(self.pattern_cell(), td(self.dmc_num), td(self.name))
    
    def pattern_cell(self):
        classes = f"stitch dmc{self.dmc_num}"
        if (max(self.rgb) + min(self.rgb)) / 2 <= 127:
            classes += " dark"
        return td(self.symbol, _class=classes, onclick=f"onClickStitch('{self.dmc_num}')")


class FontPatternExtractor:
    def __init__(self, pdf):
        self.pdf = pdf
    
    def get_rows(self, page_idx):
        return self.pdf.pages[page_idx].extract_table({"vertical_strategy": "lines_strict"})
    
    def extract_pattern(self, *args, **kwargs):
        return extract_pattern(self.get_rows, *args, **kwargs)

    @staticmethod
    def _rgb_from_img(pdf_img):
        """Return the color in the image extracted from the PDF image stream."""
        return Image.open(BytesIO(pdf_img["stream"].get_data())).getpixel((0, 0))

    def extract_key(self, key_page_idx):
        key_page = self.pdf.pages[key_page_idx]
        colour_imgs = key_page.images
        colour_data = []
        for row in key_page.extract_table()[1:]:
            colour_data.append(row[2:5])
            colour_data.append(row[7:])
        return [[*row, *self.rgb_from_img(img)] for row, img in zip(colour_data, colour_imgs)]


class ShapePatternExtractor:
    PATTERN_TABLE_SETTINGS = {
        "join_tolerance": 0,
        "snap_tolerance": 0,
        "intersection_tolerance": 0.1,
        "horizontal_strategy": "lines_strict",
        "vertical_strategy": "lines_strict",
        "edge_min_length": 200  # Hardcoded min edge length which should stop us from including stitch symbols
    } 
    COLOR_TABLE_SETTINGS = {"horizontal_strategy": "text", "vertical_strategy": "text", "keep_blank_chars": True} 
    PLACEHOLDERS = ascii_letters + punctuation

    def __init__(self, pdf):
        self.pdf = pdf
        self.ident_map = None
    
    @staticmethod
    def bbox_to_ident(page, bbox):
        def objs_ident(objs, prefix):
            return [prefix + "".join(sorted([f"x{int(x - obj['x0'])}y{int(y - obj['y0'])}" for x, y in obj['pts']])) for obj in objs]
        page_sect = page.within_bbox(bbox)
        return "-".join(sorted(objs_ident(page_sect.curves, "c") + objs_ident(page_sect.lines, "l")))
    
    def get_rows(self, page_idx):
        def get_symbol(page, cell):
            ident = self.bbox_to_ident(page, cell)
            assert ident in self.ident_map, f"Encountered unknown identifier '{ident}' not found in key."
            return self.ident_map[ident]
        page = self.pdf.pages[page_idx]
        table = page.find_tables(self.PATTERN_TABLE_SETTINGS)[0]
        return [[get_symbol(page, cell) for cell in row.cells] for row in table.rows]

    def extract_pattern(self, *args, **kwargs):
        if not self.ident_map:
            raise ValueError("Cannot extract pattern before generating or loading a key.")
        return extract_pattern(self.get_rows, *args, **kwargs)
    
    def load_ident_map(self, path):
        ident_map = {}
        with open(path) as f:
            for row in f:
                symbol, *_, ident = row.split("\t")
                ident_map[ident] = symbol
        self.ident_map = ident_map
    
    def extract_key(self, key_page_idx):

        def filter_majority_rects(rects):
            """Return the rects with the majority size to try to guess at which rects hold the right key components."""
            majority_width, majority_height = Counter([(int(r["width"]), int(r["height"])) for r in rects]).most_common(1)[0][0]
            return [r for r in rects if int(r["width"]) == majority_width and int(r["height"]) == majority_height]
        
        key_page = self.pdf.pages[key_page_idx]

        idents = filter_majority_rects([r for r in key_page.rects if not r["fill"]])
        idents = [self.bbox_to_ident(key_page, (r["x0"], r["top"], r["x1"], r["bottom"])) for r in idents]
        assert len(idents) <= len(self.PLACEHOLDERS), "Too many symbols to automatically generate all symbols"

        colors = filter_majority_rects([r for r in key_page.rects if r["fill"]])
        colors = [[int(c*255) for c in r["non_stroking_color"]] for r in colors]
        assert len(idents) == len(colors), f"Number of colors extracted does not equal number of symbols extracted ({len(colors)} vs {len(idents)})"

        key_table = key_page.extract_table(self.COLOR_TABLE_SETTINGS)
        stitches = []
        last_col_stitches = []
        for row in key_table:
            if row[2] and row[1]:
                stitches.append({"name": row[2], "dmc_num": row[1]})
            if row[3] and row[4]:
                last_col_stitches.append({"name": row[5], "dmc_num": row[4]})
        stitches += last_col_stitches
        assert len(stitches) == len(idents), f"Number of rows extracted does not equal number of colors extracted ({len(stitches)} vs {len(colors)})"

        symbols = list(self.PLACEHOLDERS)
        for stitch in stitches:
            stitch["symbol"] = symbols.pop(0)
            stitch["color"] = colors.pop(0)
            stitch["ident"] = idents.pop(0)
        
        self.ident_map = {s["ident"]: s["symbol"] for s in stitches}

        return [(s["symbol"], s["dmc_num"], s["name"], *s["color"], s["ident"]) for s in stitches]

def extract_pattern(get_rows_fn, width, height, start_page_idx=None, end_page_idx=None, overlap=0, verbose=False):
    all_pages = end_page_idx is None and start_page_idx is None
    if end_page_idx is None and start_page_idx is not None:
        end_page_idx = start_page_idx

    if all_pages:
        start_page_idx = 0
        end_page_idx = len(pdf.pages) - 1

    pattern = []

    cur_x = 0
    cur_y = 0
    for page_idx in range(start_page_idx, end_page_idx+1):
        rows = get_rows_fn(page_idx)

        if cur_y > 0:
            rows = rows[overlap:]
        if cur_x > 0:
            rows = [row[overlap:] for row in rows]

        page_width = len(rows[0])
        page_height = len(rows)

        if cur_x == 0:
            expected_page_height = page_height

        cur_width = cur_x + page_width
        cur_height = cur_y + page_height

        assert all(len(row) == page_width for row in rows), f"Pattern uneven width on page {page_idx+1}"
        assert page_height == expected_page_height or cur_height == height, f"Pattern {page_height} tall on page {page_idx+1} when expected {expected_page_height} or {height - cur_y}"
        assert cur_width <= width and cur_height <= height, f"Page {page_idx+1} ({page_width}x{page_height}) results in exceeded pattern dimensions ({cur_width}x{cur_height} vs {width}x{height})"

        if verbose:
            print(f"Extracting page {page_idx+1} ({page_width}x{page_height}), pat size {cur_width}x{cur_height}", end="")

        if cur_x != 0 and pattern:
            # New columns, so need to add these to end of existing rows
            for pat_row, page_row in zip(pattern[cur_y : cur_y + page_height], rows):
                pat_row += page_row
        else:
            # New rows, so just need to add them to end of existing pattern
            pattern += rows
            if verbose:
                print(f" (new rows)", end="")

        if verbose:
            print()

        cur_x += len(rows[0])
        if cur_x == width:
            cur_x = 0
            cur_y += page_height
    
    if all_pages:
        assert len(pattern) == height, f"{len(pattern)} stitches high but expected {height} after parsing whole pattern"
        assert len(pattern[0]) == width, f"{len(pattern[0])} stitches high but expected {width} after parsing whole pattern"

    return pattern

def save_pattern(pattern, path):
    with open(path, "w", encoding="utf-8") as f:
        print(*["".join(row) for row in pattern], sep="\n", file=f)

def load_pattern(path):
    with open(path, encoding="utf-8") as f:
        pattern = [line.strip("\n") for line in f]
    return pattern

def save_key(key, path):
    with open(path, "w", encoding="utf-8") as f:
        for row in key:
            print(*row, sep="\t", file=f)

def load_key(path):
    stitches = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            sym, num, name, r, g, b = line.strip("\n").split("\t")[:6]
            stitches[sym] = Stitch(num, name, sym, (r, g, b))
    return stitches

def gen_html(stitches, pattern):
    stitches_by_dmc = sorted(stitches.values())
    width = len(pattern[0])
    height = len(pattern)
    with open("style-embedded.css") as f:
        styles = f.read()
    pat_table = table(
        tr(th(), *[th(i) for i in range(1, width+1)]),
        *[tr(th(i+1), *[stitches.get(symbol, Stitch.default(symbol)).pattern_cell()
                        for symbol in row]) for i, row in enumerate(pattern)],
        _class="pattern",
        style=f"width: {width}px")
    pat_table[height//2].className = "middle-row"
    for row in pat_table:
        cell = row[width//2]
        cell.className = "middle-col" if not cell.className else cell.className + " middle-col"
    return html(
        meta(charset="ascii"),
        script("""
        var selectedDmcNum = null;
        function onClickStitch(dmcNum) {
            var stitches = document.querySelectorAll('.dmc'+dmcNum);
            var patternElem = document.getElementsByClassName('pattern')[0];
            if (selectedDmcNum == dmcNum) {
                stitches.forEach(elem => elem.classList.remove('selected'));
                patternElem.classList.remove('selecting');
                selectedDmcNum = null;
            } else if (selectedDmcNum == null) {
                stitches.forEach(elem => elem.classList.add('selected'));
                patternElem.classList.add('selecting');
                selectedDmcNum = dmcNum;
            } else {
                stitches.forEach(elem => elem.classList.add('selected'));
                document.querySelectorAll('.dmc'+selectedDmcNum).forEach(elem => elem.classList.remove('selected'));
                selectedDmcNum = dmcNum;
            }
        }
        """),
        style(styles + "\n".join(stitch.dmc_style for stitch in stitches_by_dmc)),
        details(
            summary("Key"),
            table(tr(th("Sym."), th("No."), th("Name")),
                *[stitch.key_row() for stitch in stitches_by_dmc])),
        pat_table)

def save_html(site, path):
    with open(path, "w") as f:
        print(site, file=f)

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["extract"]:
        with pdfplumber.open(args["PDF"]) as pdf:
            if args["--mode"] == "font":
                extractor = FontPatternExtractor(pdf)
            elif args["--mode"] == "shape":
                extractor = ShapePatternExtractor(pdf)
                keypath = args["--keypath"]
                if not keypath and not args["--keypage"]:
                    keypath = args["PDF"].replace(".pdf", "_key.tsv")
                if keypath:
                    extractor.load_ident_map(keypath)

            if args["--keypage"]:
                key = extractor.extract_key(int(args["--keypage"]) - 1)
                save_key(key, args["PDF"].replace(".pdf", "_key.tsv"))
            pat = extractor.extract_pattern(
                int(args["WIDTH"]), int(args["HEIGHT"]),
                start_page_idx=int(args["STARTPAGE"])-1 if args["STARTPAGE"] else None,
                end_page_idx=int(args["ENDPAGE"])-1 if args["ENDPAGE"] else None,
                overlap=int(args["--overlap"]) if args["--overlap"] else 0,
                verbose=bool(args["--verbose"]))
    
        if args["--verbose"]:
            print(*[f"{i: 10}" for i in range(10, len(pat[0])+1, 10)], sep="")
            print(*["".join(row) for row in pat], sep="\n")
            print(len(pat[0]), "x", len(pat), "stitches",
                    "(uneven)" if any(len(row) != len(pat[0]) for row in pat) else "")
            if args["--keypage"]:
                print(key)
    
        save_pattern(pat, args["PDF"].replace(".pdf", ".pat"))
    else:
        site = gen_html(load_key(args["KEY"]), load_pattern(args["PATTERN"]))
        save_html(site, args["PATTERN"].replace(".pat", ".html"))
