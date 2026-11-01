"""
Record reference slides. One short exhibit per filed document (R01-R10) in place of the full copy:
a reference sheet (what it is, when filed, where the full copy lives, how many pages) followed by
the excerpted pages already cropped as Figures in the Integrated Statement.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer, Image, KeepTogether
from reportlab.lib import colors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_integrated as I
from build_allinone import P, rl, grid, h1, body, small, cen, TMP, CASE_NO, COURT, FILINGS, FIL

FIGDIR = os.path.join(TMP, "fig")
PAGE_W = 6.5 * inch
cap = ParagraphStyle("rcap", parent=small, fontSize=9.5, leading=13, textColor=colors.HexColor("#333333"), spaceBefore=4, spaceAfter=12)
ref = ParagraphStyle("rref", parent=body, fontSize=11.5, leading=16.5, firstLineIndent=0)
where = ParagraphStyle("rwhere", parent=small, leftIndent=12, rightIndent=12, borderColor=colors.HexColor("#555555"), borderWidth=0.6, borderPadding=8,
                       spaceBefore=8, spaceAfter=12)


def figs_for(code):
    return [(k, pg, c) for k, src, pg, _, c in I.FIGS if os.path.basename(src).startswith(code)]


def fig_image(key):
    path = os.path.join(FIGDIR, f"{key}.png")
    with fitz.open(path) as im:
        w, h = im[0].rect.width, im[0].rect.height
    iw = PAGE_W; ih = iw * h / w
    if ih > 3.4 * inch:
        ih = 3.4 * inch; iw = ih * w / h
    return Image(path, width=iw, height=ih)


def record_ref(code, dt, desc, fn, out):
    full = os.path.join(FIL, fn)
    npages = len(fitz.open(full)) if os.path.exists(full) else 0
    figs = figs_for(code)
    f = [P(f"RECORD REFERENCE {code}", h1), P(f"<b>Filed:</b> {dt}", ref), P(f"<b>Document:</b> {desc}", ref),
         P(f"<b>Length of full document:</b> {npages} pages (not reproduced).", ref), Spacer(1, 6),
         P(f"<b>Where the full document is.</b> On file with the Clerk, {COURT}, Case No. {CASE_NO} (Register of Actions); a true copy is held in defendant's "
           f"timestamped record system as <i>{fn}</i> and will be produced to the Court or to counsel on request or by order. "
           f"The pages reproduced below are the pages relied on; page numbers are the PDF page numbers of the filed document.", where)]
    if figs:
        f.append(P("<b>Excerpted pages</b>", ref))
        f.append(grid([["Fig.", "Page", "What the page shows"]] + [[k[1:], str(pg), c.split("\u2014", 1)[-1].strip()[:160] + ("\u2026" if len(c) > 160 else "")] for k, pg, c in figs],
                      [0.5 * inch, 0.6 * inch, 5.4 * inch]))
        for k, pg, c in figs:
            f.append(KeepTogether([Spacer(1, 10), fig_image(k), P(f"<b>Figure {k[1:]}.</b> {c}", cap)]))
    else:
        f.append(P("No page of this document is excerpted; it is listed for the completeness of the chronology and is cited by its R-number in Tab A.", small))
    return rl(f, out, f"Record Reference {code}")


def record_items():
    items = []
    for code, dt, desc, fn in FILINGS:
        out = record_ref(code, dt, desc, fn, os.path.join(TMP, f"recref_{code}.pdf"))
        items.append((f"{code} \u2013 {dt} \u2013 {desc}", out))
    return items


if __name__ == "__main__":
    for lab, p in record_items():
        print(len(fitz.open(p)), "pp", lab[:70])
