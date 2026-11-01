"""
Snippet engine for scanned filings.

OCR each page, find the lines that carry the operative language (granted / denied / ordered ...),
crop the page to the region around those lines, paint a translucent yellow highlight over the
matched words, and lay the crops out two-or-more to a letter page with a caption that states the
source document and page.  Proof-of-service and blank pages are dropped.  Pages with no operative
language are reproduced at reduced scale so nothing in the court's response is silently omitted.
"""
import os, io, json, re, hashlib, warnings
warnings.filterwarnings("ignore")
import fitz
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "tmp", "ocr_cache"); os.makedirs(CACHE, exist_ok=True)
DPI = 150
LETTER = (612, 792)
MARGIN_X, TOP, BOTTOM = 54, 60, 60
CONTENT_W = LETTER[0] - 2 * MARGIN_X
HL = (255, 230, 0, 110)

_ocr = None
def ocr_page(page):
    """OCR a page -> list of (bbox[x0,y0,x1,y1] in pixels @DPI, text)."""
    global _ocr
    # key on the rendered page content, not the file path/mtime, so regenerated intermediates reuse the cache
    key = hashlib.md5(page.get_pixmap(dpi=40).samples).hexdigest()
    cp = os.path.join(CACHE, key + ".json")
    if os.path.exists(cp):
        return json.load(open(cp))
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    pix = page.get_pixmap(dpi=DPI)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    buf = io.BytesIO(); img.save(buf, "PNG")
    res, _ = _ocr(buf.getvalue())
    out = []
    for box, text, conf in (res or []):
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        out.append([[min(xs), min(ys), max(xs), max(ys)], text])
    json.dump(out, open(cp, "w"))
    return out


POS_RE = re.compile(r"proof\s*of\s*service|postage|declare under penalty|deposited|mailing address", re.I)


def page_kind(lines):
    txt = " ".join(t for _, t in lines)
    if len(txt.strip()) < 20:
        return "blank"
    if POS_RE.search(txt) and not re.search(r"granted|denied|ordered", txt, re.I):
        return "pos"
    return "content"


def regions_for(lines, kw_re, page_px_h, pad=70, gap=170, max_frac=0.6):
    hits = [b for b, t in lines if kw_re.search(t)]
    if not hits:
        return [], []
    hits.sort(key=lambda b: b[1])
    clusters, cur = [], [hits[0]]
    for b in hits[1:]:
        if b[1] - cur[-1][3] > gap:
            clusters.append(cur); cur = [b]
        else:
            cur.append(b)
    clusters.append(cur)
    xs0 = min(b[0] for b, _ in lines); xs1 = max(b[2] for b, _ in lines)
    regs = []
    for c in clusters:
        y0 = max(0, min(b[1] for b in c) - pad); y1 = min(page_px_h, max(b[3] for b in c) + pad)
        if y1 - y0 > max_frac * page_px_h:
            y1 = y0 + max_frac * page_px_h
        regs.append([max(0, xs0 - 20), y0, xs1 + 20, y1])
    # merge overlapping regions
    merged = []
    for r in regs:
        if merged and r[1] <= merged[-1][3]:
            merged[-1][3] = max(merged[-1][3], r[3])
        else:
            merged.append(r)
    return merged, hits


def render_snippets(page, kw_re, fallback_scale=0.72):
    """Return list of (PIL image, note) for one scanned page."""
    lines = ocr_page(page)
    kind = page_kind(lines)
    if kind in ("blank", "pos"):
        return [], kind
    pix = page.get_pixmap(dpi=DPI)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("RGBA")
    regs, hits = regions_for(lines, kw_re, pix.height)
    if hits:
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for b in hits:
            d.rectangle([b[0] - 4, b[1] - 3, b[2] + 4, b[3] + 3], fill=HL)
        img = Image.alpha_composite(img, ov)
    img = img.convert("RGB")
    if not regs:
        # no operative language found: keep the page, reduced, so the response is still complete
        w, h = img.size
        return [(img.resize((int(w * fallback_scale), int(h * fallback_scale)), Image.LANCZOS), "page reproduced in full (reduced); no operative language detected by OCR")], kind
    out = []
    for r in regs:
        out.append((img.crop((int(r[0]), int(r[1]), int(r[2]), int(r[3]))), "excerpt; highlights added"))
    return out, kind


def layout(snips, out_pdf, title, src_label):
    """snips: list of (PIL image, caption). Stack onto letter pages at content width."""
    doc = fitz.open()
    page = None; y = TOP
    def new_page():
        nonlocal page, y
        page = doc.new_page(width=LETTER[0], height=LETTER[1]); y = TOP
        page.insert_textbox(fitz.Rect(MARGIN_X, 28, LETTER[0] - MARGIN_X, 52), title, fontsize=9, fontname="hebo", color=(0.25, 0.25, 0.25))
    new_page()
    for img, cap in snips:
        w, h = img.size
        scale = CONTENT_W / w
        dh = h * scale
        max_h = LETTER[1] - TOP - BOTTOM - 30
        if dh > max_h:
            scale = max_h / h; dh = max_h
        dw = w * scale
        need = dh + 34
        if y + need > LETTER[1] - BOTTOM and y > TOP:
            new_page()
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=82, optimize=True)
        x0 = MARGIN_X + (CONTENT_W - dw) / 2
        r = fitz.Rect(x0, y, x0 + dw, y + dh)
        page.insert_image(r, stream=buf.getvalue())
        page.draw_rect(r, color=(0.55, 0.55, 0.55), width=0.5)
        page.insert_textbox(fitz.Rect(MARGIN_X, y + dh + 3, LETTER[0] - MARGIN_X, y + dh + 30), cap, fontsize=8.5, fontname="tiro", color=(0.2, 0.2, 0.2))
        y += need + 8
    doc.save(out_pdf, garbage=3, deflate=True); doc.close()
    return out_pdf


RULING_RE = re.compile(r"grant|denied|deny|order|moot|approved", re.I)
MED_RE = re.compile(r"off work|return|diagnos|strain|discharge|follow|november|rest|activity|fall|CT|work", re.I)


def snippet_pdf(src_pdf, out_pdf, title, src_label, kw_re=RULING_RE, pages=None):
    d = fitz.open(src_pdf); n = len(d)
    snips = []; dropped = 0
    for p in d:
        if pages is not None and (p.number + 1) not in pages:
            continue
        imgs, kind = render_snippets(p, kw_re)
        if not imgs:
            dropped += 1; continue
        for k, (img, note) in enumerate(imgs):
            snips.append((img, f"{src_label}, p. {p.number + 1} of {n}" + (f" ({k + 1} of {len(imgs)})" if len(imgs) > 1 else "") + f" - {note}."))
    if not snips:
        # nothing survived (all proofs of service); reproduce the first page reduced
        pix = d[0].get_pixmap(dpi=DPI); img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        snips = [(img.resize((int(img.width * 0.72), int(img.height * 0.72))), f"{src_label}, p. 1 of {n} - page reproduced in full (reduced).")]
    layout(snips, out_pdf, title + f"   |   {n} filed page(s); proof-of-service and blank pages omitted ({dropped})", src_label)
    return out_pdf
