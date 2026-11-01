"""
Page-reduction pass for the final binders.

  trim_ada(path, out)        - Tab K: keep only the court's FILED order / response pages of each
                               Rule 1.100 packet (OCR-classified); drop the MC-410 request copies,
                               e-mail printouts and other attachments that the court stapled behind
                               its order and that already live elsewhere in the binder.
  trim_subpoena(path, out)   - Tab I: keep SUBP-002 page 1 (the subpoena) and page 2 (declaration),
                               plus the typed attachment pages; drop the blank proof-of-service page.
                               Form pages are rasterized so phone / Chrome viewers that lack the
                               Judicial Council form fonts show the full form, not just the filled fields.
  streamlined_statement(path)- Replaces the 30-page Integrated Statement in Tab A with the
                               streamlined Statement of the Case (four independent bars + chronology).
  dedupe_pages(doc)          - Removes byte-identical page images that recur across exhibits.
"""
import os, re, sys, hashlib, warnings
warnings.filterwarnings("ignore")
import fitz
import numpy as np
from reportlab.platypus import Spacer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, grid, signature, TMP, COURT, DEPT
from build_notice import body, h2, h3, phase, box

_OCR = None


def ocr_page(page, dpi=90):
    global _OCR
    if _OCR is None:
        from rapidocr_onnxruntime import RapidOCR
        _OCR = RapidOCR()
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    res, _ = _OCR(img)
    return " ".join(r[1] for r in (res or []))


COURT_PAT = re.compile(r"FILED|SUPERIOR ?COURT|Deputy Clerk|IT IS (SO )?ORDERED|ORDERED|Judge of the Superior|RESPONSE TO|Dept\.? ?\d{3}|Courtroom|DENIED|GRANTED", re.I)
# The MC-410 form itself (the court's orders are titled "Order re Disability Accommodation Request", so that phrase alone is not a request page).
REQUEST_PAT = re.compile(r"MC-?410|Clerk receives and date stamps|Court fills out below|If you have a disability and need an accommodation|Important! ?If ?your ?case", re.I)
EMAIL_PAT = re.compile(r"Subject:|From:|Sent:|gmail|Re:\s|wrote:|Inbox", re.I)


def classify(text):
    if re.search(r"FILED|Deputy Clerk|Judge of the Superior|IT IS (SO )?ORDERED", text, re.I) and not re.search(r"MC-?410", text, re.I):
        return "court"
    if REQUEST_PAT.search(text):
        return "request"
    if EMAIL_PAT.search(text) and not re.search(r"IT IS (SO )?ORDERED|Judge of the Superior", text, re.I):
        return "email"
    if COURT_PAT.search(text):
        return "court"
    return "other"


def trim_ada(path, out):
    """Keep the court's own pages: from the first FILED/court page, continuing while pages are
    court text (a multi-page order), stopping at the first MC-410 copy or e-mail printout."""
    d = fitz.open(path)
    kinds = [classify(ocr_page(d[i])) for i in range(len(d))]
    # Keep every page the court itself produced (stamped/ordered pages), plus unclassified pages that
    # directly continue a court page (the body of a multi-page order). MC-410 copies and e-mails are dropped.
    keep = []
    for i, k in enumerate(kinds):
        if k == "court" or (k == "other" and i > 0 and (i - 1) in keep):
            keep.append(i)
    if not keep:
        # No stamped court page found: fall back to the first non-request page.
        keep = [i for i, k in enumerate(kinds) if k != "request"][:2] or [0]
    o = fitz.open()
    for i in keep:
        o.insert_pdf(d, from_page=i, to_page=i)
    o.save(out, garbage=3, deflate=True)
    print(f"  ADA {os.path.basename(path)}: {len(d)} -> {len(keep)} pages  [{''.join(k[0] for k in kinds)}]")
    return out


def trim_subpoena(path, out, dpi=150):
    d = fitz.open(path)
    o = fitz.open()
    for i in range(len(d)):
        pg = d[i]
        txt = pg.get_text() or ""
        # The Judicial Council form is always the first three pages of the packet; attachments follow.
        is_form = i < 3 and "ATTACHMENT 3" not in txt
        if is_form:
            if i == 2:
                continue  # blank proof-of-service page of the Judicial Council form
            pix = pg.get_pixmap(dpi=dpi, annots=True)
            np_ = o.new_page(width=pg.rect.width, height=pg.rect.height)
            np_.insert_image(np_.rect, pixmap=pix)
        else:
            o.insert_pdf(d, from_page=i, to_page=i)
    o.save(out, garbage=3, deflate=True)
    return out


def dedupe_pages(doc, protect_first=0):
    """Delete pages whose rendered content repeats an earlier page (byte-identical xref image or
    identical low-res raster). Keeps the first occurrence. Returns number removed."""
    seen, drop = set(), []
    for i in range(len(doc)):
        if i < protect_first:
            continue
        pg = doc[i]
        txt = (pg.get_text() or "").strip()
        if txt.startswith("EXHIBIT ") or txt.startswith("TAB "):
            continue  # exhibit sheets / tab pages are intentionally similar
        pix = pg.get_pixmap(dpi=20, colorspace=fitz.csGRAY)
        h = hashlib.md5(pix.samples).hexdigest()
        if h in seen:
            drop.append(i)
        else:
            seen.add(h)
    for i in reversed(drop):
        doc.delete_page(i)
    return len(drop)


S = "\u00a7"
TITLE = ["STREAMLINED STATEMENT OF THE CASE;", "FOUR INDEPENDENT STATUTORY BARS TO POSSESSION;", "CONCISE CHRONOLOGY"]

STATEMENT = [
    ("phase", "TRIAL CALL: NOVEMBER 2, 2026, 9:00 A.M., DEPARTMENT 606. DEFENDANT IN PRO PER: DR. DONNY GILLSON, ED.D. "
              "ALL RECORD CITATIONS ARE TO THE FILED DOCKET (R01\u2013R10, TAB H) AND TO BATES-NUMBERED EXHIBITS (TABS A\u2013M)."),
    ("h2", "I. Nature of the Action and Summary of Defenses"),
    ("n", "This is a residential unlawful detainer action brought by Swords to Plowshares against a service-connected disabled veteran, "
          "Dr. Donny Gillson, Ed.D., for possession of Unit 301A at 1030 Girard Road, San Francisco (R01, Tab H-1). "
          "Defendant appears in propria persona and uses an ADA-recognized cognitive assistive device for TBI/PTSD pacing (Tab J)."),
    ("n", "Defendant maintains that the action is barred in its entirety on four independent statutory grounds, each of which is sufficient alone:"),
    ("h3", "1. Statutory retaliation (Civ. Code " + S + " 1942.5)"),
    ("n", "The April 8, 2026 notice to quit issued within 180 days of protected habitability complaints (SF 311 Case 101003004371, Tab L), "
          "administrative filings (Tab M), and the restraining-order proceeding CCH-26-589086. The notice itself cites defendant's court filings and "
          "accommodated e-mail volume as grounds (Fig. 1, Tab A-2). A notice that recites protected activity as its reason is presumptively retaliatory on its face."),
    ("h3", "2. Defective notice and service (Code Civ. Proc. " + S + S + " 1161, 1162, 415.45)"),
    ("n", "The notice does not state the facts of the claimed breach with statutory particularity, and the proof of service (R05, Tab H-5) does not show "
          "personal service on the named defendant; the declarant's dates and the posting sequence are internally inconsistent (Index of Irregularities, Tab B, rows 2\u20135). "
          "The referenced Exhibit 3 to the complaint is absent from the filed record (Tab B, row 6)."),
    ("h3", "3. Failure to accommodate (Cal. Rules of Court, rule 1.100; 42 U.S.C. " + S + " 12132)"),
    ("n", "Management departed from the written communication protocol agreed December 23, 2025 for defendant's TBI and PTSD (Tab L), culminating in the "
          "verbal \u201cstop or else\u201d confrontation of January 2\u20133, 2026 (Tab C, witness Landrum). This Court's own rule 1.100 orders (Tab K) confirm the accommodations in force."),
    ("h3", "4. Void default judgment (Code Civ. Proc. " + S + S + " 473(d), 585)"),
    ("n", "Default and judgment were entered June 30, 2026 (R03\u2013R04, Tabs H-3, H-4) while defendant's responsive paper and rule 1.100 requests were pending, "
          "and without personal service of the summons (R05). A judgment entered without jurisdiction over the person is void and may be set aside at any time."),
    ("h2", "II. Concise Chronology"),
    ("table", [["Date", "Event", "Record"],
               ["Nov. 19, 2025", "SF 311 Case 101003004371 opened: rodent and cockroach infestation", "Tab L"],
               ["Dec. 23, 2025", "Written reasonable-accommodation consensus: e-mail-only communication", "Tab L"],
               ["Jan. 2\u20133, 2026", "\u201cStop or else\u201d threat and confrontation by William Landrum", "Tab C; Tab I-3"],
               ["Feb. 25, 2026", "Elder/dependent-adult restraining-order application filed (CCH-26-589086)", "Tab K-12, K-13"],
               ["Apr. 8, 2026", "Notice to quit issued, citing court filings and e-mail volume", "Fig. 1; Tab A-2"],
               ["May 5, 2026", "Summons and complaint filed", "R01; Tab H-1"],
               ["May 19, 2026", "Plaintiff's ex parte application for order to post", "R02; Tab H-2"],
               ["June 30, 2026", "Request for entry of default; judgment; proof of service filed same day", "R03\u2013R05; Tabs H-3\u2013H-5"],
               ["July 1, 2026", "Notice of entry of judgment; writ of possession", "R06\u2013R07; Tabs H-6, H-7"],
               ["July 7\u20138, 2026", "Defendant's emergency ex parte application; order thereon", "R08\u2013R10; Tabs H-8\u2013H-10"],
               ["Oct. 30, 2026", "Emergency department places defendant off work through Nov. 3", "Tab J-2 (confidential)"],
               ["Nov. 2, 2026", "Trial call, Dept. 606", "\u2014"]],
     [1.15 * 72, 3.9 * 72, 1.45 * 72]),
    ("h2", "III. Relief Requested"),
    ("n", "Judgment for defendant on the complaint; alternatively, dismissal without prejudice for defective notice and service; an order confirming the rule 1.100 "
          "accommodations for all further proceedings; and such further relief as is just. The Master Trial Brief (Tab A-1) supplies the authorities and the line-by-line record index."),
]


def streamlined_statement(path):
    f = caption("<br/>".join(TITLE))
    f.append(P(f"TO: {COURT}, {DEPT}, and to plaintiff and its counsel of record.", body))
    n = 0
    for item in STATEMENT:
        kind = item[0]
        if kind == "phase": f.append(P(item[1], phase))
        elif kind == "h2":
            n = 0; f.append(P(item[1], h2))
        elif kind == "h3": f.append(P(item[1], h3))
        elif kind == "n":
            n += 1; f.append(P(f"{n}. {item[1]}", body))
        elif kind == "box": f.append(P(item[1], box))
        elif kind == "table":
            f.append(Spacer(1, 6)); f.append(grid(item[1], item[2])); f.append(Spacer(1, 8))
    f.append(Spacer(1, 10)); f.extend(signature())
    return rl(f, path, "Streamlined Statement of the Case")


if __name__ == "__main__":
    out = streamlined_statement(os.path.join(TMP, "streamlined_statement.pdf"))
    print(out, len(fitz.open(out)), "pages")
