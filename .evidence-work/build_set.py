"""
One build -> six binders (B1-B5 + B6 Solano MC-410), each with its own cover, master index, tab sheets,
bookmarks and continuous Bates numbering (B1-0001 ...).  Video files are staged by process_videos.py.
"""
import os, sys, re, json, glob, hashlib, shutil, datetime, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz
from PIL import Image, ImageOps
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Spacer, Image as RLImage, Table, TableStyle, PageBreak
import build_allinone as A
from build_allinone import P, rl, grid, h1, cen, small, TMP, ART, COMP, HERE, FIL, FILINGS, CASE_NO, COURT, DEPT, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED
import build_integrated as I, build_notice as N, build_brief as B, build_record_refs as RR, trim as T
import build_mil as M, build_notice_service as NS, build_opening as OP, build_notice_lodgment as NL
import build_notice_telemetry as NT, build_service_log as SL, build_translog as TL, snip, build_lead_memo as LM
from build import CATEGORIES
from build_binders import WITNESSES, ADA_EXHIBITS, make_mc410, make_subpoena, medical_exhibit, compress_scans
from build_final import cover_sol

B4DIR = "/tmp/b4"; VIDEO_DIR = os.path.join(B4DIR, "Binder3_Videos"); STILLS = os.path.join(B4DIR, "stills")
OUT = {n: os.path.join(ART, f) for n, f in {
    1: "Gillson_FINAL_Binder1_Statement_of_the_Case.pdf", 2: "Gillson_FINAL_Binder2_Motions.pdf",
    3: "Gillson_FINAL_Binder3_Witness_List_and_Subpoenas.pdf", 4: "Gillson_FINAL_Binder4_Evidence_Photos_and_Videos.pdf",
    5: "Gillson_FINAL_Binder5_CONFIDENTIAL_Medical_VA.pdf", 6: "Gillson_FINAL_Binder6_Solano_County_MC-410.pdf"}.items()}
ORANGE = ParagraphStyle("conf", parent=cen, fontSize=13, leading=18, textColor=colors.HexColor("#8B0000"), fontName="Helvetica-Bold")
mono = ParagraphStyle("mono", parent=small, fontName="Courier", fontSize=7.5, leading=9)
CELL8 = ParagraphStyle("c8", parent=small, fontSize=7.5, leading=9)
CELL8B = ParagraphStyle("c8b", parent=CELL8, fontName="Helvetica-Bold")
BATES = {}  # binder -> {label: (first, last)}


# ---------------------------------------------------------------- assembler
def assemble(num, cover_pdf, sections, footer, front=None, make_index_pages=None):
    """sections: [(letter, title, [item])]; item = (label, path[, exhibit_no[, 'nosheet']])."""
    prefix = f"B{num}"; out = OUT[num]; bates_of = {}

    def build(toc_pdf):
        doc = fitz.open(); bookmarks = []; rows = []; bates = 1; page_tab = {}
        def add(path, bookmark=None, level=1):
            nonlocal bates
            src = fitz.open(path); start = len(doc); doc.insert_pdf(src)
            if bookmark:
                bookmarks.append([level, bookmark, start + 1])
            first = bates; bates += len(src); src.close()
            return first, bates - 1
        add(cover_pdf, "Cover")
        for lab, p in (front or []):
            add(p, lab)
        if toc_pdf:
            add(toc_pdf, "Master Index of Exhibits")
        for ti, (letter_, title, items) in enumerate(sections):
            tab_start = len(doc)
            add(A.tab_page(os.path.join(TMP, f"set_tab_{prefix}_{letter_}.pdf"), letter_, title), f"Tab {letter_} \u2013 {title}")
            rows.append([letter_, f"<b>{title}</b>", "", ""])
            for k, it in enumerate(items, 1):
                label, path = it[0], it[1]
                no = it[2] if len(it) > 2 and it[2] else f"{letter_}-{k}"
                nosheet = len(it) > 3 and it[3] == "nosheet"
                n_pages = len(fitz.open(path))
                conf = ("MC-410" in title or "Medical" in title or "CONFIDENTIAL" in label.upper() or num == 5)
                if nosheet:
                    a, b = add(path, f"Ex. {no} \u2013 {label}", 2)
                else:
                    add(A.exhibit_sheet(os.path.join(TMP, f"set_ex_{prefix}_{letter_}_{k}.pdf"), no, label, n_pages, conf), f"Exhibit {no} \u2013 {label}", 2)
                    a, b = add(path)
                bates_of[label] = (a, b)
                rows.append([no, label, f"{prefix}-{a:04d} \u2013 {prefix}-{b:04d}", str(n_pages)])
            for pi in range(tab_start, len(doc)):
                page_tab[pi] = (letter_, ti)
        n_tabs = len(sections)
        for i, page in enumerate(doc):
            if page.rect.width > page.rect.height:
                page.set_rotation((page.rotation + 90) % 360)
            r = page.rect; dm = page.derotation_matrix; rot = page.rotation
            if i in page_tab:
                letter_, ti = page_tab[i]
                usable = r.height - 2.0 * inch; step = usable / max(n_tabs, 1); bh = min(step, 0.6 * inch); y0 = 1.0 * inch + ti * step
                shape = page.new_shape(); shape.draw_rect(fitz.Rect(r.width - 0.32 * inch, y0, r.width, y0 + bh) * dm)
                shape.finish(color=None, fill=A.tab_rgb(letter_)); shape.commit()
                page.insert_text(fitz.Point(r.width - 0.25 * inch, y0 + bh / 2 + 4) * dm, letter_, fontsize=11, fontname="hebo", color=(1, 1, 1), rotate=rot)
            page.insert_text(fitz.Point(r.width - 1.9 * inch, r.height - 0.35 * inch) * dm, f"{prefix}-{i+1:04d}", fontsize=8, fontname="helv", rotate=rot)
            page.insert_text(fitz.Point(0.75 * inch, r.height - 0.35 * inch) * dm, footer, fontsize=7, fontname="helv",
                             color=(0.55, 0, 0) if num == 5 else (0.3, 0.3, 0.3), rotate=rot)
        doc.set_toc(bookmarks)
        return doc, rows

    tocp = os.path.join(TMP, f"set_toc_{prefix}.pdf")
    d, rows = build(None); d.close()
    A.toc(tocp, rows, footer)
    for _ in range(4):
        d, rows = build(tocp); n_toc = len(fitz.open(tocp)); d.close()
        A.toc(tocp, rows, footer)
        if len(fitz.open(tocp)) == n_toc:
            break
    d, _ = build(tocp); d.save(out, garbage=3, deflate=True); n = len(d); d.close()
    BATES[num] = bates_of
    return n


def cover(num, path, title_lines, sub_lines, blurb, confidential=False):
    f = [Spacer(1, 1.0 * inch), P(f"BINDER {num} OF 6", ParagraphStyle("bn", parent=cen, fontSize=12, leading=16)), Spacer(1, 6)]
    for t in title_lines:
        f.append(P(t, ParagraphStyle("big", parent=h1, fontSize=24, leading=30)))
    if confidential:
        f += [Spacer(1, 10), P("CONFIDENTIAL \u2013 MEDICAL INFORMATION", ORANGE),
              P("Protected health information. Cal. Rules of Court, rule 1.100(c)(4); Civ. Code, \u00a7 56 et seq.; 38 U.S.C. \u00a7 7332. Do not file publicly; lodge conditionally under seal.", small)]
    f += [Spacer(1, 18)] + [P(s, ParagraphStyle("c1", parent=cen, fontSize=12, leading=18)) for s in sub_lines]
    f += [Spacer(1, 22), P(f"Submitted by {NAME}, Defendant in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen),
          Spacer(1, 22), P(blurb, small), Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


def xref_page(path, title, intro, rows):
    return rl([P(title, h1), Spacer(1, 6), P(intro, small), Spacer(1, 8), grid([["Item", "Where it is", "Bates / location"]] + rows, [2.6 * inch, 2.2 * inch, 1.7 * inch])], path, title)


def rng(num, label_fragment):
    for lab, (a, b) in BATES[num].items():
        if label_fragment in lab:
            return f"B{num}-{a:04d} \u2013 B{num}-{b:04d}"
    raise KeyError(label_fragment)


# ---------------------------------------------------------------- Binder 4 pieces
EVID = {
    "photo": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410 (authenticated by the photographer's testimony that it fairly and accurately depicts the scene); \u00a7\u00a7 1552-1553 (digital image / printed representation presumed accurate)",
    "screen": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410, 1421 (content known to the author); \u00a7\u00a7 1552-1553 (printed representation of digital data presumed accurate)",
    "writing": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410, 1413 (witness who received / observed the writing), 1414 (adoption by the opposing party), 1421; \u00a7\u00a7 1552-1553; party admissions \u00a7\u00a7 1220, 1222",
    "record": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410, 1552-1553; official / agency record \u00a7\u00a7 1530, 1532, 1280 (admissibility of content reserved)",
    "medimg": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410, 1552-1553 (photograph of the record); content under \u00a7\u00a7 1271, 1280, 1560-1562 (custodian declaration)",
    "video": "Evid. Code \u00a7\u00a7 250 (writing includes video), 1400-1401, 1410, 1413 (witness to the events recorded), 1552-1553; recorded statements of the opposing party and its agents \u00a7\u00a7 1220, 1222",
}
CAT_BASIS = {"A": "writing", "B": "photo", "C": "photo", "D": "medimg", "E": "writing", "F": "record", "I": "photo", "G": "screen", "H": "photo"}
CAT_TYPE = {"A": "Photo of writing", "B": "Photograph", "C": "Photograph", "D": "Photo of record", "E": "Photo of writing", "F": "Photo of record", "I": "Photograph", "G": "Screenshot", "H": "Photograph"}
CAT_SOURCE = {"A": "Notice/grievance as submitted to property management; photographed by the resident", "B": "Photographed by the resident inside Unit, 1030 Girard Rd.",
              "C": "Photographed by the resident (service animal)", "D": "Photographed by the resident (injuries / medical documents)",
              "E": "Correspondence received from Swords to Plowshares management; photographed or captured by the resident",
              "F": "Government agency record received by the resident; photographed or captured by the resident", "I": "Photographed by the resident at the premises parking lot",
              "G": "Screen capture taken by the resident on his mobile phone", "H": "Photographed by the resident, building common areas"}


def when_from(fn):
    m = re.search(r"(\d{4})(\d{2})(\d{2})[_-](\d{2})(\d{2})(\d{2})", fn)
    return datetime.datetime(*map(int, m.groups())) if m else None


def photo_exhibits():
    os.makedirs(os.path.join(B4DIR, "photos"), exist_ok=True); out = []; n = 0
    for cat, ctitle, items in CATEGORIES:
        for fn, desc in items:
            n += 1; srcp = os.path.join(HERE, "src", fn); jp = os.path.join(B4DIR, "photos", f"Ex{n:02d}.jpg")
            h = hashlib.sha256(open(srcp, "rb").read()).hexdigest()
            im = ImageOps.exif_transpose(Image.open(srcp)).convert("RGB")      # keep full color
            im.thumbnail((2000, 2000), Image.LANCZOS); im.save(jp, "JPEG", quality=92, subsampling=0, optimize=True)
            w, hgt = im.size; s = min(6.3 * inch / w, 5.0 * inch / hgt)
            dt = when_from(fn); dts = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "see description"
            basis = EVID[CAT_BASIS[cat]]
            flow = [P(f"EXHIBIT {n}", h1), P(f"Category {cat}: {ctitle}", ParagraphStyle("k", parent=cen, fontSize=10, leading=13)), Spacer(1, 6),
                    RLImage(jp, width=w * s, height=hgt * s), Spacer(1, 8),
                    grid([["Field", "Detail"], ["Exhibit no.", f"Ex. {n}"], ["Description", desc], ["Date / time taken", f"{dts} (device capture stamp in file name {fn})"],
                          ["Source", f"{CAT_SOURCE[cat]}. Original native file {fn}; SHA-256 {h[:32]}\u2026"],
                          ["Authentication basis", basis]], [1.3 * inch, 5.2 * inch])]
            pdf = rl(flow, os.path.join(TMP, f"set_photo_{n:02d}.pdf"), f"Exhibit {n}")
            out.append({"n": n, "cat": cat, "pdf": pdf, "desc": desc, "date": dts[:16] if dt else "n/a", "type": CAT_TYPE[cat], "basis": basis, "sha": h})
    return out


def fmt_dur(s):
    return f"{int(s//60)}:{int(s%60):02d}" if s is not None else "n/a"


def video_slips():
    man = json.load(open(os.path.join(B4DIR, "video_manifest.json"))); out = []
    for r in man:
        ex = r["exhibit"]; pages = []
        local = ""
        if r.get("created"):
            try:
                dtu = datetime.datetime.fromisoformat(r["created"].replace("Z", "+00:00")); off = int(r.get("utc_offset") or 0) / 100 if r.get("utc_offset") else None
                local = f"{r['created'][:19].replace('T', ' ')} UTC" + (f" ({(dtu + datetime.timedelta(hours=off)).strftime('%Y-%m-%d %H:%M')} local, UTC{r['utc_offset']})" if off is not None else "")
            except Exception:
                local = r["created"]
        kind = {"video": "Video recording (MP4)", "audio": "Audio-only recording (3GPP)", "image": "Still image (JPEG) designated within the video suite", "duplicate": "Video recording \u2013 duplicate file"}[r["kind"]]
        flow = [P(f"EXHIBIT {ex}", h1), P(f"{r['title']}", ParagraphStyle("vt", parent=cen, fontSize=12, leading=16)), Spacer(1, 6)]
        sp = os.path.join(STILLS, ex + ".jpg")
        if os.path.exists(sp):
            w, h = Image.open(sp).size; s = min(5.0 * inch / w, 2.9 * inch / h)
            flow += [RLImage(sp, width=w * s, height=h * s), P("Still frame extracted from the file (full color).", small), Spacer(1, 6)]
        else:
            flow += [P("Audio-only recording \u2013 no video frame exists.", small), Spacer(1, 6)]
        if r["kind"] == "duplicate":
            fn = f"Binder3_Videos/{r['duplicate_of']}.mp4 (byte-identical to Ex. {r['duplicate_of']}; same SHA-256; not duplicated in the ZIP)"
        else:
            fn = f"Binder3_Videos/{r['filename']}"
        rows = [["Field", "Detail"], ["Exhibit no.", ex], ["Type", kind], ["Filename (in ZIP)", fn],
                ["Duration", fmt_dur(r.get("duration")) if r["kind"] != "image" else "n/a (still image)"],
                ["Date / time recorded", local or "Not embedded in file metadata; designated and served Oct. 29, 2026 (see Tab D notices)"],
                ["File size", f"{r['bytes']:,} bytes ({r['bytes']/1048576:.1f} MB)"],
                ["Description", r["desc"]], ["Source", "Recorded by the resident (native device file); originally served as a Google Drive link in the Oct. 29-30, 2026 notices; link: " + r["url"]],
                ["Evidence Code basis", EVID["video"]], ["SHA-256", r["sha256"]]]
        data = [[c if not isinstance(c, str) else P(c, mono if (i == len(rows) - 1 and j == 1) else (CELL8B if j == 0 or i == 0 else CELL8)) for j, c in enumerate(rw)] for i, rw in enumerate(rows)]
        t = Table(data, colWidths=[1.3 * inch, 5.2 * inch], repeatRows=1)
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6"))]))
        flow.append(t)
        pdf = rl(flow, os.path.join(TMP, f"set_video_{ex}.pdf"), f"Exhibit {ex}")
        out.append({"ex": ex, "pdf": pdf, "title": r["title"], "date": (r.get("created") or "")[:10] or "10/29/2026 (served)", "type": kind.split(" (")[0], "basis": "Evid. Code \u00a7\u00a7 250, 1400-1401, 1410, 1413, 1552-1553, 1220, 1222", "label": f"Ex. {ex} \u2013 {r['title']}"})
    return out


def evidentiary_index(path, photos, vids, bates):
    rows = [[P(h, CELL8B) for h in ["Exhibit No.", "Description", "Date", "Type", "Evidence Code basis", "Bates"]]]
    def br(lbl):
        a = bates.get(lbl); return f"B4-{a[0]:04d}\u2013{a[1]:04d}" if a else "\u2014"
    for p in photos:
        rows.append([P(f"Ex. {p['n']}", CELL8), P(p["desc"][:230] + ("\u2026" if len(p["desc"]) > 230 else ""), CELL8), P(p["date"], CELL8), P(p["type"], CELL8),
                     P(p["basis"].split(" (")[0], CELL8), P(br(f"Ex. {p['n']} \u2013 {p['cat']}"), CELL8)])
    for v in vids:
        rows.append([P(f"Ex. {v['ex']}", CELL8), P(v["title"], CELL8), P(v["date"], CELL8), P(v["type"], CELL8), P(v["basis"], CELL8), P(br(v["label"]), CELL8)])
    t = Table(rows, colWidths=[0.6 * inch, 2.55 * inch, 0.8 * inch, 0.8 * inch, 1.05 * inch, 0.7 * inch], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#808080")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return rl([P("EVIDENTIARY INDEX \u2013 PHOTOGRAPHS AND AUDIO-VISUAL EXHIBITS", h1),
               P("Evidence Code foundations: photographs and digital images \u2014 \u00a7\u00a7 1400, 1401, 1410-1413, 1552-1553; writings (incl. video and photographs) \u2014 \u00a7 250. "
                 "The notices served Oct. 29-30, 2026 (Exs. 72-91) are indexed in the Master Index under Tab D. Videos are in the ZIP folder Binder3_Videos, named by exhibit number.", small),
               Spacer(1, 6), t], path, "Evidentiary Index")


# ---------------------------------------------------------------- medical correlation (Binder 5)
EVENTS = [("2026-05-05", "Summons and UD complaint filed", "R01"), ("2026-05-19", "Plaintiff ex parte for service by posting", "R02"),
          ("2026-06-30", "Default entered; default judgment", "R03-R05"), ("2026-07-07", "Defendant's emergency ex parte application", "R08-R09"),
          ("2026-07-08", "Order re ex parte", "R10")]
for fn in sorted(os.listdir(os.path.join(HERE, "ada"))):
    d = fn[:8]; EVENTS.append((f"{d[:4]}-{d[4:6]}-{d[6:]}", "Rule 1.100 accommodation request / court response", "Binder 2, Tab F"))
EVENTS += [("2026-09-17", "ER visit (VA Palo Alto)", "Binder 5"), ("2026-10-30", "John Muir ED visit after fall; off work through Nov. 3", "Binder 5, Tab B"),
           ("2026-10-29", "Opening papers and notices served", "Binder 2, Tabs A-E"), ("2026-11-02", "Trial call, Dept. 606", "Binder 1")]
KW = re.compile(r"cockroach|roach|rats?\b|evict|housing|landlord|swords|retaliat|harass|court|PTSD|TBI|concussion|suicid|fall\b|sleep|anxiety|PHQ|trial|homeless|HCHV", re.I)
DATE_RE = re.compile(r"(?:Date entered|DATE OF NOTE|Date of note)\W+([A-Z][a-z]+ \d{1,2}, \d{4}|[A-Z]{3}\s?\d{1,2},\s?\d{4}|\d{2}/\d{2}/\d{4})", re.I)
TITLE_RE = re.compile(r"^(?:[A-Z][A-Z0-9 /&\-\(\)]{8,60})$", re.M)


def parse_date(s):
    for f in ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%b %d,%Y"):
        try:
            return datetime.datetime.strptime(s.strip().title() if "/" not in s else s.strip(), f).date()
        except Exception:
            pass
    return None


def correlation(path, excerpts_pdf, bates_start_label):
    d = fitz.open(excerpts_pdf); rows = []; cur = None; title = ""
    for i, pg in enumerate(d):
        t = pg.get_text(); m = DATE_RE.search(t)
        if m:
            dd = parse_date(m.group(1)); cur = dd or cur
        tm = TITLE_RE.search(t); title = tm.group(0).strip() if tm else title
        hit = KW.search(t)
        if not hit:
            continue
        s0 = max(0, hit.start() - 70); snippet = " ".join(t[s0:hit.end() + 110].split())
        near = []
        if cur:
            for ed, et, ref in EVENTS:
                e = datetime.date.fromisoformat(ed)
                if abs((e - cur).days) <= 10:
                    near.append(f"{e.strftime('%m/%d/%Y')} {et} ({ref})")
        rows.append([cur.strftime("%m/%d/%Y") if cur else "undated", f"VA Blue Button report (excerpt p. {i+1}) \u2013 {title or 'clinical note'}", "\u2026" + snippet + "\u2026",
                     "; ".join(near[:3]) or "Condition history; see Binder 1 chronology"])
    t = Table([[P(h, CELL8B) for h in ["Date", "VA record", "Snippet (highlighted in Tab C)", "Related event / exhibit"]]] +
              [[P(c, CELL8) for c in r] for r in rows], colWidths=[0.7 * inch, 1.5 * inch, 2.6 * inch, 1.7 * inch], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#808080")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6"))]))
    rl([P("MEDICAL CORRELATION INDEX \u2013 CONFIDENTIAL", h1),
        P("Each row ties a finding in the VA record to the dates of the conditions and events in this case. The \u201cRelated event\u201d column lists case events within ten days of the note date "
          "(temporal correlation only; it is not a statement of causation). Snippet pages follow in Tab C.", small), Spacer(1, 6), t], path, "Correlation Index")
    return path, len(rows)


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    figs = I.render_figs(); I.build_pdf(figs, I.OUT_PDF); I.build_docx(figs, I.OUT_DOCX)
    notice = N.build_notice(os.path.join(TMP, "notice_opening.pdf")); mil = M.build_mil(os.path.join(TMP, "mil_1.pdf"))
    svc_notice = NS.build(os.path.join(TMP, "notice_failure_to_serve.pdf")); opening = OP.build(os.path.join(TMP, "opening_statement.pdf"))
    lodgment = NL.build(os.path.join(TMP, "notice_lodgment.pdf")); telemetry = NT.build(os.path.join(TMP, "notice_telemetry.pdf"))
    svclog = SL.build(os.path.join(TMP, "service_log.pdf")); translog = TL.build(os.path.join(TMP, "translog.pdf"))
    photo_counts = {l: len(items) for l, _, items in CATEGORIES}; record_items = RR.record_items()
    brief = B.build_brief(os.path.join(TMP, "trial_brief.pdf")); streamlined = T.streamlined_statement(os.path.join(TMP, "streamlined_statement.pdf"))
    tabB = A.irregularities(os.path.join(TMP, "two_B.pdf")); tabC = A.witness_list(os.path.join(TMP, "two_C.pdf"))
    tabD = A.evidence_list(os.path.join(TMP, "two_D.pdf"), photo_counts); tabE = A.video_list(os.path.join(TMP, "two_E.pdf"))
    tabF = A.points_authorities(os.path.join(TMP, "two_F.pdf")); tabG = A.closing(os.path.join(TMP, "two_G.pdf"))
    med_ex = medical_exhibit(os.path.join(TMP, "two_medical_exhibit.pdf"))
    ada_items, seen = [], set()
    for fn, lab in ADA_EXHIBITS:
        path = os.path.join(HERE, "ada", fn); h = hashlib.md5(open(path, "rb").read()).hexdigest()
        if h in seen:
            continue
        seen.add(h); k = len(ada_items) + 1
        trimmed = T.trim_ada(path, os.path.join(TMP, f"two_ada_{k:02d}.pdf"))
        snipped = snip.snippet_pdf(trimmed, os.path.join(TMP, f"two_ada_{k:02d}_snip.pdf"), f"Binder 2, Tab F, Ex. {k} - {lab}", f"Ex. {k}")
        ada_items.append((f"Ex. {k}. {lab} \u2013 operative language only (highlighted excerpts)", snipped))
    mc_sf_merged = A.merge(make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} \u2014 {DEPT}",
        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall."],
        "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further proceedings in this case.", "Defendant", "Unlawful detainer",
        "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings."), os.path.join(TMP, "two_mc_sf.pdf"))
    CASE = ["<i>Swords to Plowshares v. Gillson</i>", f"{COURT} \u2014 {DEPT}", f"Case No. {CASE_NO} \u2014 Trial call November 2, 2026, 9:00 a.m."]
    FOOT = f"Gillson \u2013 {CASE_NO} \u2013 "

    # ===== Binder 1: Statement of the Case
    lead_memo = LM.build(os.path.join(TMP, "lead_memo.pdf"))
    b1 = [("L", "Lead Memorandum of Points and Authorities \u2013 Statutory Bars, Mandatory Federal Exhaustion, Federal Grant Audit Demand (Nov. 1, 2026)",
           [("Lead Memorandum of Points and Authorities in Support of Emergency Dismissal, Mandatory Audit of Federal Grant Funds, and Injunctive Relief", lead_memo)]),
          ("A", "Master Integrated Statement of the Case and Trial Brief; Index of Record Irregularities; Summary of Exhibits (LEAD DOCUMENT)",
           [("Master Integrated Statement of the Case and Trial Brief (with Index of Record Irregularities and Summary of Exhibits)", brief)]),
          ("B", "Index of Record Irregularities and Indicia of Fraud (line-by-line)", [("Line-by-line index of record irregularities", tabB)]),
          ("C", "Summary of Exhibits", [("Exhibit and evidence list (summary of exhibits)", tabD)]),
          ("D", "Streamlined Statement of the Case", [("Four independent statutory bars and concise chronology", streamlined)]),
          ("E", "Record References \u2013 Filed Court Record (R01\u2013R10), Key Pages Only", record_items),
          ("F", "Points and Authorities", [("Memorandum with table of authorities", tabF)]),
          ("G", "Closing Argument", [("Closing argument outline", tabG)])]
    n1 = assemble(1, cover(1, os.path.join(TMP, "set_cover1.pdf"), ["STATEMENT OF THE CASE"], CASE, "Full judicial binder: the Lead Memorandum of Points and Authorities (Tab L), the Master Integrated Statement of the Case and Trial Brief (lead document), the line-by-line Index of Record Irregularities, the Summary of Exhibits, and the filed court record. Motions are in Binder 2; witnesses and subpoenas in Binder 3; photographs and videos in Binder 4; confidential medical records in Binder 5; the Solano MC-410 in Binder 6."), b1, FOOT + "Binder 1 \u2013 Statement of the Case")
    print("B1", n1)

    # ===== Binder 2: Motions
    b2 = [("A", "Opening Statement and Emergency Application for Reasonable Accommodation and Emergency Judicial Access (Vesco) \u2013 Emergency Hearing Papers",
           [("Opening Statement; Application for Reasonable Accommodation and Emergency Judicial Access (Vesco) (Nov. 1, 2026)", opening)]),
          ("B", "Emergency Motion in Limine No. 1", [("Emergency Motion in Limine No. 1 \u2013 Disqualify Zanghi Torres Adams LLP; Exclude VA-Derived Evidence; Rule 1.100 Accommodation; Declaration; [Proposed] Order", mil)]),
          ("C", "Notice of Government Claims; Request for Judicial Notice; Verified Statement of Disqualification",
           [("Notice of Government Claims; Request for Judicial Notice; Verified Statement of Disqualification; Notice of Federal Rights; Points and Authorities", notice)]),
          ("D", "Related Notices", [("Notice of Lodgment of Digital Case Repository and IP Protections; Notice of Hard-Copy Service (Nov. 1, 2026)", lodgment),
                                     ("Supplemental Notice of Active Monitoring, Digital Telemetry, and ESI Logs (Nov. 1, 2026)", telemetry),
                                     ("Notice of Plaintiff's Failure to Serve Statement of the Case and Pretrial Trial Materials; Objection (Nov. 1, 2026)", svc_notice)]),
          ("E", "Electronic Service Log Declaration and Transmission Log (Oct. 29 \u2013 Nov. 1, 2026)",
           [("Declaration re Electronic Service Log, Oct. 29 - Nov. 1, 2026", svclog), ("Transmission Log \u2013 E-mail Service Record; Declaration of Service", translog)]),
          ("F", "ADA Requests and Responses Filed in San Francisco (Rule 1.100)", [("Request for Accommodations \u2013 MC-410 (San Francisco) with Attachment", mc_sf_merged)] + ada_items)]
    n2 = assemble(2, cover(2, os.path.join(TMP, "set_cover2.pdf"), ["MOTIONS"], CASE, "All motions and emergency papers: the Vesco emergency application, Emergency Motion in Limine No. 1, the Notice of Government Claims, Request for Judicial Notice and Verified Statement of Disqualification, related notices, the Electronic Service Log declaration, and the ADA requests and responses filed in San Francisco."), b2, FOOT + "Binder 2 \u2013 Motions")
    print("B2", n2)

    # ===== Binder 3: Witness list and subpoenas
    sub_items = [(f"Civil Subpoena (Duces Tecum) \u2013 {w['name']}",
                  T.trim_subpoena(A.merge(make_subpoena(w), os.path.join(TMP, f"two_subp_{w['tag']}.pdf")), os.path.join(TMP, f"two_subp_{w['tag']}_trim.pdf"))) for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY", h1), grid([["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES], [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "two_svc.pdf"))
    b3 = [("A", "Witness List, Offers of Proof, and Section VIII Amendment", [("Witness list and offer of proof (including Section VIII amendment and preservation request)", tabC)]),
          ("B", "Notice to Counsel and Preservation Demand", [("Notice to Francisco Torres, Esq., October 31, 2026", os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf"))]),
          ("C", "Civil Subpoenas (SUBP-002) with Attachment 3, Service Directory and Proof of Service", [("Service directory", svc)] + sub_items)]
    n3 = assemble(3, cover(3, os.path.join(TMP, "set_cover3.pdf"), ["WITNESS LIST", "AND SUBPOENAS"], CASE, "The full witness list (with the Section VIII amendment, stated on information and belief), offers of proof, the notice and preservation demand to opposing counsel, and every subpoena with its proof-of-service form."), b3, FOOT + "Binder 3 \u2013 Witness List and Subpoenas")
    print("B3", n3)

    # ===== Binder 4: Evidence (photos and videos) - full color, never passed through compress_scans
    photos = photo_exhibits(); vids = video_slips()
    old = fitz.open(os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))
    def part(a, b, name):
        d = fitz.open(); d.insert_pdf(old, from_page=a - 1, to_page=b - 1); p = os.path.join(TMP, name); d.save(p); d.close(); return p
    decl = part(1, 3, "set_old_decl.pdf"); notices_old = part(45, 79, "set_old_notices.pdf"); va_old = part(80, 114, "set_old_va.pdf")
    photo_items = [(f"Ex. {p['n']} \u2013 {p['cat']}: {p['desc'][:90]}", p["pdf"], str(p["n"]), "nosheet") for p in photos]
    vid_items = [(v["label"], v["pdf"], v["ex"], "nosheet") for v in vids]
    bates_prev = {}
    for _ in range(3):
        idx = evidentiary_index(os.path.join(TMP, "set_evid_index.pdf"), photos, vids, bates_prev)
        # labels in the index lookup use the same prefix text as the item labels
        b4 = [("A", "Evidentiary Index and Foundation Declaration", [("Evidentiary index table (Exhibit | Description | Date | Type | Evidence Code basis | Bates)", idx, "IDX", "nosheet"),
                                                                    ("Declaration of Donald Ernest Gillson authenticating Exhibits 1-92 (as originally served)", decl)]),
              ("B", "Photographic Exhibits \u2013 Exhibits 1-71 (full color)", photo_items),
              ("C", "Audio-Visual Exhibits \u2013 Slip Sheets (files in ZIP folder Binder3_Videos)", [("Audio-visual exhibit list and publication plan", tabE)] + vid_items),
              ("D", "Evidentiary Notices Served on Opposing Counsel, Oct. 29-30, 2026 (Exhibits 72-91, as served)", [("Evidentiary notices and video designations as served (Exs. 72-91)", notices_old)])]
        n4 = assemble(4, cover(4, os.path.join(TMP, "set_cover4.pdf"), ["EVIDENCE", "PHOTOGRAPHS AND VIDEOS"], CASE,
                               "All photographs reproduced in full color (no grayscale, no lossy color reduction), each with exhibit number, description, date and time taken, source, and Evidence Code authentication basis. "
                               "PDF cannot play video: each recording has a slip sheet with a still frame, filename, duration, date, description, Evidence Code basis and SHA-256 hash; the files are in the ZIP folder Binder3_Videos, named by exhibit number."),
                      b4, FOOT + "Binder 4 \u2013 Evidence")
        cur = {}
        for lab, rng_ in BATES[4].items():
            cur[lab] = rng_
        # normalise label keys used by the index
        norm = {}
        for p in photos:
            for lab, r_ in cur.items():
                if lab.startswith(f"Ex. {p['n']} \u2013 {p['cat']}:"):
                    norm[f"Ex. {p['n']} \u2013 {p['cat']}"] = r_
        for v in vids:
            norm[v["label"]] = cur[v["label"]]
        if norm == bates_prev:
            break
        bates_prev = norm
    print("B4", n4)

    # ===== Binder 5: Confidential medical (VA)
    excerpts = os.path.join(HERE, "docs", "VA_Blue_Button_Report_EXCERPTS.pdf")
    corr, n_corr = correlation(os.path.join(TMP, "set_corr.pdf"), excerpts, "")
    snips = snip.snippet_pdf(excerpts, os.path.join(TMP, "set_va_snips.pdf"), "VA Blue Button report \u2013 findings correlated to case events", "VA excerpts", kw_re=KW)
    xr = xref_page(os.path.join(TMP, "set_xref5.pdf"), "FRONT-OF-BINDER CROSS-REFERENCE \u2013 EMERGENCY (VESCO) HEARING, MOTIONS IN LIMINE, STATEMENT OF THE CASE",
                   "Per the instruction that these papers appear at the front of the medical binder, and so that no document is duplicated, each is cross-referenced to the binder that holds it.",
                   [["Emergency Vesco application / Opening Statement (Nov. 1, 2026)", "Binder 2, Tab A", rng(2, "Opening Statement")],
                    ["Emergency Motion in Limine No. 1 (exclude VA-derived evidence; disqualification; accommodation)", "Binder 2, Tab B", rng(2, "Emergency Motion in Limine")],
                    ["Notice of Government Claims; RJN; Verified Statement of Disqualification", "Binder 2, Tab C", rng(2, "Notice of Government Claims")],
                    ["Master Integrated Statement of the Case and Trial Brief", "Binder 1, Tab A", rng(1, "Master Integrated")],
                    ["Streamlined Statement of the Case", "Binder 1, Tab D", rng(1, "Four independent")],
                    ["Photographs of ED documents, injuries (Category D, Exs. 44-70 range)", "Binder 4, Tab B", "see Binder 4 Evidentiary Index"],
                    ["John Muir ED record and wristband photographs (Oct. 30, 2026)", "This binder, Tab B", "see Master Index"]])
    va_full = os.path.join(HERE, "docs", "VA_Blue_Button_Report_2026-11-01.pdf")
    b5 = [("A", "Medical Correlation Index and Cross-References", [("Cross-reference: Vesco hearing, motions in limine, Statement of the Case", xr), ("Correlation index (date | VA record | snippet | related event / exhibit)", corr)]),
          ("B", "Private Medical Records \u2013 John Muir Health ED (Oct. 30, 2026) \u2013 CONFIDENTIAL", [("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)]),
          ("C", "VA Findings Correlated to Case Dates \u2013 Highlighted Snippet Pages", [("Highlighted snippet pages from the VA Blue Button report", snips)]),
          ("D", "VA Blue Button Report \u2013 Complete (Nov. 1, 2026) and Excerpts as Served", [("VA Blue Button report \u2013 complete (215 pages)", va_full), ("VA excerpts as served Oct. 29-30, 2026 (Evidence Ex. 92)", va_old)]),
          ("E", "VA Retaliation Investigation and Related Agency Complaints", [("BBS Complaint 2002026002097 \u2013 Kolby Losik", os.path.join(COMP, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
                                                                              ("BBS Complaint 2002026002098 \u2013 Mark Villalobos", os.path.join(COMP, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))])]
    n5 = assemble(5, cover(5, os.path.join(TMP, "set_cover5.pdf"), ["MEDICAL RECORDS (VA)"], CASE, "Private medical records, VA Blue Button report, highlighted snippet pages, and the correlation index tying findings to the dates of the conditions and events in the case. "
                           "The Vesco hearing papers, motions in limine and Statement of the Case are cross-referenced at the front (Tab A).", confidential=True), b5,
                   "CONFIDENTIAL \u2013 MEDICAL INFORMATION \u2013 " + FOOT + "Binder 5")
    print("B5", n5, "correlation rows", n_corr)

    # ===== Binder 6: Solano MC-410
    mc_sol = A.merge(make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)", "Superior Court of California, County of Solano \u2013 Civil Harassment (Code Civ. Proc., \u00a7 527.6)",
        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall."],
        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings."), os.path.join(TMP, "two_mc_sol.pdf"))
    xr6 = xref_page(os.path.join(TMP, "set_xref6.pdf"), "CROSS-REFERENCE \u2013 MATERIALS HELD IN OTHER BINDERS", "This binder is filed in a different court, so Tabs C-H repeat the San Francisco materials that the Solano application relies on. The full evidence set is not repeated; it is held as follows.",
                    [["Photographs and videos (Exs. 1-71, V1/V2)", "Binder 4", "B4 Evidentiary Index"], ["VA and private medical records, correlation index", "Binder 5 (confidential)", "B5 Tab A"],
                     ["Witness list and subpoenas", "Binder 3", "B3 Tabs A-C"], ["Emergency / Vesco papers and motions", "Binder 2", "B2 Tabs A-E"]])
    b6 = [("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order",
           [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
          ("B", "Request for Accommodations \u2013 MC-410 (Solano County) \u2013 CONFIDENTIAL IN PART", [("MC-410 with Attachment", mc_sol), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
          ("C", "Course of Conduct \u2013 Opening Notice and Integrated Statement of the Case (San Francisco, CUD-26-682107)", [("Transmission Log", translog), ("Master Integrated Statement of the Case", brief), ("Emergency Motion in Limine No. 1", mil)]),
          ("D", "Index of Record Irregularities (San Francisco record)", [("Line-by-line index", tabB)]),
          ("E", "Video Evidence \u2013 Audio-Visual Exhibit List, Foundation, Publication Plan", [("Audio-visual exhibit list", tabE)]),
          ("F", "Points and Authorities \u2013 Table of Authorities with Case Summaries", [("Memorandum", tabF)]),
          ("G", "Record References \u2013 San Francisco Court Record (R01\u2013R10), Key Pages Only", record_items),
          ("H", "San Francisco Superior Court Rule 1.100 Orders and Responses (July\u2013October 2026)", ada_items),
          ("I", "Cross-Reference to Evidence and Medical Binders", [("Materials held in Binders 2-5", xr6)])]
    n6 = assemble(6, cover_sol(os.path.join(TMP, "set_cover6.pdf")), b6, "Gillson \u2013 Binder 6 \u2013 Solano County MC-410 \u2013 Confidential in part (CRC 1.100(c)(4))")
    print("B6", n6)
    for n in (1, 2, 3, 6):
        compress_scans(OUT[n])
    print("done")
