"""
Amended 5-binder build (Binder I-V). Each binder: cover, master index, tab sheets, bookmarks, continuous Bates B<n>-0001...
"""
import os, sys, re, json, glob, hashlib, shutil, datetime, warnings
from xml.sax.saxutils import escape as esc
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Spacer, Table, TableStyle, PageBreak
import build_set as BS
import build_binders as BB
from build_set import (A, P, rl, grid, h1, cen, small, TMP, ART, COMP, HERE, CASE_NO, COURT, DEPT, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED,
                       I, N, B, RR, T, M, NS, OP, NL, NT, SL, TL, snip, LM, CATEGORIES, WITNESSES, ADA_EXHIBITS, make_mc410, make_subpoena,
                       medical_exhibit, compress_scans, cover_sol, CELL8, CELL8B, ORANGE, photo_exhibits, video_slips, evidentiary_index,
                       correlation, KW)

INC = os.path.join(HERE, "incoming")
OUT5 = {n: os.path.join(ART, f) for n, f in {
    1: "Gillson_FINAL_Binder1_Statement_Motions_ADA_Solano_Calendar.pdf",
    2: "Gillson_FINAL_Binder2_Witness_List_and_Subpoenas.pdf",
    3: "Gillson_FINAL_Binder3_Master_Exhibit_Directory.pdf",
    4: "Gillson_FINAL_Binder4_CONFIDENTIAL_Medical.pdf",
    5: "Gillson_FINAL_Binder5_Solano_MC-410_and_Restraining_Order.pdf"}.items()}
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
TITLES = {1: "STATEMENT OF THE CASE, MOTIONS, EMERGENCY / ADA, SOLANO COURT & UPCOMING APPOINTMENTS",
          2: "WITNESS LIST & SUBPOENAS", 3: "MASTER EXHIBIT DIRECTORY (MULTIMEDIA & PHOTOGRAPHIC)",
          4: "CONFIDENTIAL MEDICAL & HEALTH PRESERVATION BINDER", 5: "SOLANO COUNTY / MC-410 FRAMEWORK, RESTRAINING ORDER & MALICIOUS PROSECUTION NEXUS"}
BG = {}          # binder -> {label: (first, last)}
BLANKS = []      # fields the Defendant must complete by hand
CAP = ["IN THE SUPERIOR COURT OF CALIFORNIA", "COUNTY OF SAN FRANCISCO"]
SUBDATE = "November 1, 2026"
ESIGN = "/s/ Dr. Donald Ernest Gillson, Ed.D."


def look(num, frag):
    for lab, (a, b) in BG.get(num, {}).items():
        if frag in lab:
            return f"B{num}-{a:04d} \u2013 B{num}-{b:04d}"
    return f"B{num}-0000 \u2013 B{num}-0000"


def tbl(rows, widths, size=7.5):
    st = ParagraphStyle("t", parent=CELL8, fontSize=size, leading=size + 2); stb = ParagraphStyle("tb", parent=st, fontName="Helvetica-Bold")
    data = [[c if not isinstance(c, str) else P(c, stb if i == 0 else st) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return t


# ------------------------------------------------------------------ assembler
def index_pdf(path, rows, num):
    data = [[P(h, CELL8B) for h in ["Tab / Item", "Document", "Bates", "Pp."]]]; st = []
    for r in rows:
        if r[0] == "tab":
            c = colors.Color(*A.tab_rgb(r[1]), alpha=0.28)
            data.append([P(f"<b>{r[2]}</b>", CELL8), P(f"<b>{esc(r[3])}</b>", CELL8), "", ""]); st.append(("BACKGROUND", (0, len(data) - 1), (-1, len(data) - 1), c))
        else:
            data.append([P(r[1], CELL8), P(esc(r[2]), CELL8), P(r[3], CELL8), P(str(r[4]), CELL8)])
    t = Table(data, colWidths=[0.55 * inch, 3.65 * inch, 1.7 * inch, 0.6 * inch], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#808080")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)] + st))
    return rl([P(f"BINDER {ROMAN[num]} \u2013 MASTER INDEX", h1), P("Every entry shows the Bates range of its first and last page (prefix B%d-). Bookmarks in the PDF match this index." % num, small), Spacer(1, 6), t], path, "Index")


def assemble5(num, cover_pdf, tabs, footer, conf=False):
    """tabs: [(no, title, items, sub)]; item = (label, path | callable -> path)."""
    prefix = f"B{num}"; out = OUT5[num]; tocp = os.path.join(TMP, f"s5_toc_{prefix}.pdf")

    def build(toc_pdf):
        doc = fitz.open(); bm = []; rows = []; bates = 1; page_tab = {}; bo = {}
        def add(path, bookmark=None, level=1):
            nonlocal bates
            src = fitz.open(path); start = len(doc); doc.insert_pdf(src)
            if bookmark:
                bm.append([level, bookmark, start + 1])
            first = bates; bates += len(src); n = len(src); src.close()
            return first, bates - 1, n
        add(cover_pdf, "Cover")
        if toc_pdf:
            add(toc_pdf, "Binder Index")
        for ti, (no, title, items, sub) in enumerate(tabs):
            key = chr(65 + ti % 14); t0 = len(doc)
            add(A.tab_page(os.path.join(TMP, f"s5_tab_{prefix}_{no}.pdf"), no, title, sub), f"Tab {no} \u2013 {title}")
            rows.append(("tab", key, no, title))
            for k, (label, path) in enumerate(items, 1):
                if callable(path):
                    path = path()
                a, b, n = add(path, label, 2)
                bo[label] = (a, b)
                rows.append(("doc", f"{no}.{k}" if False else f"{no}-{k}", label, f"{prefix}-{a:04d} \u2013 {prefix}-{b:04d}", n))
            for pi in range(t0, len(doc)):
                page_tab[pi] = (no, key, ti)
        nt = len(tabs)
        for i, page in enumerate(doc):
            if page.rect.width > page.rect.height:
                page.set_rotation((page.rotation + 90) % 360)
            r = page.rect; dm = page.derotation_matrix; rot = page.rotation
            if i in page_tab:
                no, key, ti = page_tab[i]
                usable = r.height - 2.0 * inch; step = usable / max(nt, 1); bh = min(step, 0.6 * inch); y0 = 1.0 * inch + ti * step
                sh = page.new_shape(); sh.draw_rect(fitz.Rect(r.width - 0.32 * inch, y0, r.width, y0 + bh) * dm)
                sh.finish(color=None, fill=A.tab_rgb(key)); sh.commit()
                page.insert_text(fitz.Point(r.width - 0.30 * inch, y0 + bh / 2 + 3) * dm, no, fontsize=8.5, fontname="hebo", color=(1, 1, 1), rotate=rot)
            page.insert_text(fitz.Point(r.width - 1.9 * inch, r.height - 0.35 * inch) * dm, f"{prefix}-{i+1:04d}", fontsize=8, fontname="helv", rotate=rot)
            page.insert_text(fitz.Point(0.75 * inch, r.height - 0.35 * inch) * dm, footer, fontsize=7, fontname="helv", color=(0.55, 0, 0) if conf else (0.3, 0.3, 0.3), rotate=rot)
        doc.set_toc(bm); BG[num] = bo
        return doc, rows

    d, rows = build(None); d.close(); index_pdf(tocp, rows, num); used = rows
    for _ in range(8):
        d, rows = build(tocp)
        if rows == used:
            break
        d.close(); index_pdf(tocp, rows, num); used = rows
    d.save(out, garbage=3, deflate=True); n = len(d); d.close()
    return n


# ------------------------------------------------------------------ generic generated pages
def cover5(num, path, conf=False):
    big = ParagraphStyle("big", parent=h1, fontSize=22, leading=28)
    f = [Spacer(1, 0.5 * inch)] + [P(c, ParagraphStyle("cp", parent=cen, fontSize=13, leading=17, fontName="Helvetica-Bold")) for c in CAP]
    f += [Spacer(1, 8), P(f"<i>Swords to Plowshares v. Gillson</i> \u2013 Case No. {CASE_NO}", cen), P(f"{DEPT} \u2013 Trial call November 2, 2026, 9:00 a.m.", cen), Spacer(1, 26),
          P(f"BINDER {ROMAN[num]} OF V", ParagraphStyle("bn", parent=cen, fontSize=12, leading=16)), Spacer(1, 6), P(TITLES[num], big)]
    if conf:
        f += [Spacer(1, 10), P("CONFIDENTIAL \u2013 MEDICAL INFORMATION", ORANGE),
              P("Protected health information. Cal. Rules of Court, rule 1.100(c)(4); Civ. Code, \u00a7 56 et seq.; 38 U.S.C. \u00a7 7332. Do not file publicly; lodge conditionally under seal.", small)]
    f += [Spacer(1, 30), P(f"Submitted by {NAME}, Defendant in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 18),
          P(f"Dated: {SUBDATE}", cen), P(ESIGN, cen)]
    return rl(f, path, "Cover")


def reserved(path, headline, extra=None, rows=None, title="Reserved"):
    f = [Spacer(1, 1.2 * inch), P(headline, ParagraphStyle("rs", parent=h1, fontSize=20, leading=26))]
    if extra:
        f += [Spacer(1, 10), P(extra, small)]
    if rows:
        f += [Spacer(1, 14), tbl([["Related material already in this set", "Where", "Bates"]] + rows, [3.0 * inch, 1.9 * inch, 1.6 * inch])]
    return rl(f, path, title)


def xref_table(path, title, intro, rows):
    return rl([P(title, h1), Spacer(1, 6), P(intro, small), Spacer(1, 8), tbl([["Document", "Where it is", "Bates"]] + rows, [3.0 * inch, 1.9 * inch, 1.6 * inch], 8)], path, title)


def mentions(path, pat):
    try:
        d = fitz.open(path); hit = any(re.search(pat, pg.get_text(), re.I) for pg in d); d.close(); return hit
    except Exception:
        return False


def docx_to_pdf(src, out, title):
    import docx
    d = docx.Document(src); f = [P(title, h1), Spacer(1, 6)]
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        sname = (p.style.name if p.style is not None else "").lower()
        head = sname.startswith(("heading", "title")) or bool(p.runs and all(r.bold for r in p.runs if r.text.strip()))
        f.append(P(f"<b>{esc(t)}</b>" if head else esc(t), small))
        f.append(Spacer(1, 3))
    for tb in d.tables:
        f.append(tbl([[c.text for c in r.cells] for r in tb.rows], [6.5 * inch / max(len(tb.rows[0].cells), 1)] * len(tb.rows[0].cells)))
    return rl(f, out, title)


# ------------------------------------------------------------------ calendar (Tab 1.6)
def calendar_pdf(path):
    acc = "Rule 1.100 accommodations per MC-410 and Oct. 14, 2026 order (assistive N.E.W.T. device announced, rest breaks, service animal; remote option requested) \u2013 see Tab 1.4"
    rows = [
        ["2026-07-07 / 07-08", "not stated", "SF Superior Court", "400 McAllister St., San Francisco", "Defendant's emergency ex parte application (Jul. 7) and order (Jul. 8) \u2013 past", "n/a (past)"],
        ["2026-09-17", "not stated", "VA Palo Alto (ER visit)", "VA Palo Alto", "Emergency room visit \u2013 past", "n/a (past)"],
        ["2026-10-14", "n/a", "SF Superior Court (Hon. Charles F. Haines)", "400 McAllister St.", "Signed ruling on Oct. 9 MC-410; protections for designated medical appointment times \u2013 past", "n/a (past)"],
        ["2026-10-19", "not stated", "SF Superior Court, Dept. 501", "400 McAllister St.", "Defense motions taken off calendar; discovery motion denied; trial reassigned \u2013 past", "n/a (past)"],
        ["2026-10-20 / 10-21", "10-21: 9:00 a.m.", "SF Superior Court, Dept. 505 then Dept. 501", "400 McAllister St.", "Hearings continued Oct. 20 to Oct. 21 (per docket entry made Oct. 28) \u2013 past", "n/a (past)"],
        ["2026-10-22", "3:00 p.m.", "VA (telephone appointment; provider not stated in source)", "Telephone", "VA appointment \u2013 past", "Court to protect designated medical appointment times"],
        ["2026-10-26", "2:00 p.m.", "VA (telephone appointment; provider not stated in source)", "Telephone", "VA appointment \u2013 past", "Same"],
        ["2026-10-27", "9:00 a.m.", "Martinez VA", "Martinez VA clinic", "VA appointment \u2013 past (the MC-410 attachment also records neuropsychological testing on 10/27/2026; time and provider not stated)", "Same"],
        ["2026-10-27", "2:00 p.m.", "San Francisco VA Medical Center", "San Francisco VA Medical Center", "VA appointment \u2013 past", "Same"],
        ["2026-10-28", "9:52 a.m. (assignment)", "SF Superior Court, Dept. 501 \u2192 Dept. 606", "400 McAllister St.", "Short-cause trial assigned to Dept. 606 jury calendar; Dept. 606 heard matter, continued to Oct. 29 for motions in limine \u2013 past", "n/a (past)"],
        ["2026-10-29", "not stated", "SF Superior Court, Dept. 501 / Dept. 606", "400 McAllister St.", "$2,500 sanctions motion transferred to Dept. 606; matter continued to Nov. 2 \u2013 past", "n/a (past)"],
        ["2026-10-30", "not stated", "John Muir Health \u2013 Concord Emergency Department", "Concord, CA", "ED visit after fall; off work through Nov. 3, return no earlier than Nov. 4 \u2013 past", "Medical orders to rest (MC-410 attachment)"],
        ["2026-11-01 (on or about)", "not stated", "David Grant USAF Medical Center (Travis AFB)", "Travis AFB, CA", "Follow-up directed by John Muir ED; extension of rest anticipated", "Medical orders to rest"],
        ["2026-11-02", "9:00 a.m.", "SF Superior Court, Dept. 606", "400 McAllister Street, San Francisco, CA 94102", "TRIAL CALL \u2013 Swords to Plowshares v. Gillson, CUD-26-682107", acc],
        ["2026-11-07", "n/a (deadline)", "Zanghi Torres Adams LLP (written response requested)", "n/a", "Response date requested in Defendant's Oct. 31, 2026 notice to counsel", "n/a"],
        ["2026-11-10", "2:00 p.m.", "San Francisco VA Medical Center", "San Francisco VA Medical Center", "VA appointment (in person)", "Protect designated medical appointment time"],
        ["To be set", "To be set", "Solano County Superior Court", "600 Union Avenue, Fairfield, CA 94533", "First hearing on civil harassment petition (CCP \u00a7 527.6) \u2013 date not yet set", "MC-410 (Solano) \u2013 see Tab 1.5 / Binder V"],
    ]
    blank = [["", "", "", "", "to be added by Defendant", ""] for _ in range(6)]
    f = [P("UPCOMING APPOINTMENTS & HEARING CALENDAR", h1),
         P("Chronological. Built only from dates that appear in the source records (docket, court orders, MC-410 attachment, VA and medical records, Defendant's Oct. 31 notice). "
           "No date has been added that the sources do not contain. Past entries are retained so the sequence is complete; blank rows at the end are for Defendant to complete. Status as of November 1, 2026.", small), Spacer(1, 6),
         tbl([["Date", "Time", "Court / Provider", "Location", "Matter", "Accommodation needed"]] + rows + blank,
             [0.8 * inch, 0.7 * inch, 1.25 * inch, 1.1 * inch, 1.65 * inch, 1.0 * inch], 7)]
    BLANKS.append("Binder I, Tab 1.6: six blank calendar rows; any appointment time marked \u201cnot stated\u201d (VA/John Muir/Travis follow-up times and locations)")
    return rl(f, path, "Calendar")


# ------------------------------------------------------------------ witnesses
W4 = [
    dict(tag="wallingford", name="David Wallingford", affil="U.S. Park Police (responding personnel)", short="David Wallingford",
         role="Park Police contact; firsthand observations and any incident reports concerning police contacts with Defendant at 1030 Girard Road, Presidio of San Francisco.",
         why="Roster: \u201cDavid Wallingford and responding U.S. Park Police personnel \u2013 police contacts and any specific incident reports or observations [agency/conditional].\u201d The docket lists a Defendant filing on Oct. 13, 2026: \u201cSupplemental Wallingford Statement; Protective-Order Advice; Subpoena References.\u201d",
         offer="Offer of proof (on information and belief): Mr. Wallingford will testify to the police contacts at the premises and to what he observed, and will authenticate any incident, CAD or contact reports held by his agency; relevant to the retaliation, habitability and notice-service issues and to the credibility of Plaintiff's account.",
         records=["All incident, contact, dispatch/CAD and supplemental reports concerning any contact with Donald Ernest Gillson at or about 1030 Girard Road, Presidio of San Francisco, 2025 to present.",
                  "All communications between the U.S. Park Police and Swords to Plowshares, its property managers, or its counsel concerning Donald Ernest Gillson.",
                  "Any statement, note or report by David Wallingford referring to Donald Ernest Gillson, including any protective-order advice.",
                  "Any body-worn or dash camera recordings of contacts with Donald Ernest Gillson, if they exist."],
         basis="Record basis for SUBP-002: roster refers to \u201cspecific incident reports.\u201d Drop the duces tecum if no reports exist."),
    dict(tag="whittaker", name="Calvin Whittaker", affil="San Francisco Housing Authority (custodian)", short="Calvin Whittaker",
         role="San Francisco Housing Authority custodian: housing-subsidy / voucher records and rent calculation for Defendant's tenancy.",
         why="Roster item 10: \u201cCalvin Whittaker / San Francisco Housing Authority custodian.\u201d Defendant disputes tenant-share, assistance-credit and account calculations (prior binder reports a monthly tenant share of $1,186).",
         offer="Offer of proof (on information and belief): Mr. Whittaker, or the custodian he designates, will testify to the subsidy/voucher terms, the contract rent and tenant share, payments received from the Authority, and communications with Swords to Plowshares about Defendant; relevant to the rent-demand figures in the notices and to retaliation.",
         records=["All records of Donald Ernest Gillson's housing subsidy / voucher, including HAP contract, tenant-share and rent-portion calculations, payment history to Swords to Plowshares, 2025 to present.",
                  "All communications between the San Francisco Housing Authority and Swords to Plowshares concerning Donald Ernest Gillson, including any grievance or complaint.",
                  "All notices, inspections and reasonable-accommodation records for the tenancy at 1030 Girard Road.",
                  "A custodian-of-records declaration (Evid. Code \u00a7\u00a7 1271, 1560)."],
         basis="Record basis for SUBP-002: roster identifies him as a custodian of Housing Authority records."),
    dict(tag="timms", name="Jeffrey Timms", affil="San Francisco Adult Protective Services (APS)", short="Jeffrey Timms",
         role="APS contact handling Defendant's reopened APS matter (spelling variants in the record: \u201cJeffrey Tims,\u201d \u201cTimms Jeffrey\u201d); confirm role and scope.",
         why="Roster: \u201cJeffrey Timms \u2013 reported APS contact \u2026 confirm role and scope [Potential APS records].\u201d Docket (Defendant filing): \u201cSupplemental APS Statement; Jeffrey Observations; Regina Gibbs / Transition Planning.\u201d",
         offer="Offer of proof (on information and belief): Mr. Timms will testify to his observations and contacts with Defendant, the APS referral history including the Dec. 5, 2025 letter, and APS communications with Swords to Plowshares; relevant to retaliation, habitability, and the condition of the unit.",
         records=["The APS case file concerning Donald Ernest Gillson, including intake, referrals, case notes, home-visit observations and closure/reopening records, 2025 to present.",
                  "All communications between APS and Swords to Plowshares, its staff or counsel concerning Donald Ernest Gillson.",
                  "The December 5, 2025 APS letter and all drafts, routing and transmittal records.",
                  "A custodian-of-records declaration (Evid. Code \u00a7\u00a7 1271, 1560). Defendant waives nothing; APS may redact third-party information."],
         basis="Record basis for SUBP-002: roster flags \u201cpotential APS records.\u201d"),
    dict(tag="gibson", name="Regina Gibson", affil="San Francisco Adult Protective Services (APS)", short="Regina Gibson",
         role="APS contact (spelling variants in the record: \u201cRegina Gibbs,\u201d \u201cGibson Ragina\u201d); transition-planning communications; confirm actual spelling before service.",
         why="Roster: \u201cRegina Gibbs / Gibson \u2013 APS contact; user records contain spelling variants and reversed order; confirm actual \u2026\u201d. Docket: \u201cSupplemental APS Statement; Jeffrey Observations; Regina Gibbs / Transition Planning.\u201d",
         offer="Offer of proof (on information and belief): Ms. Gibson will testify to APS contacts with Defendant and with Swords to Plowshares, and to transition-planning and housing-stability discussions; relevant to retaliation and to the circumstances surrounding the notices.",
         records=["All APS records, notes, referrals and transition-planning documents concerning Donald Ernest Gillson authored or held by Regina Gibson, 2025 to present.",
                  "All communications between Regina Gibson and Swords to Plowshares, its staff or counsel, or the Housing Authority concerning Donald Ernest Gillson.",
                  "A custodian-of-records declaration (Evid. Code \u00a7\u00a7 1271, 1560)."],
         basis="Record basis for SUBP-002: roster flags APS records; the APS matter is described as handled by Timms and Gibson."),
]
STP = [("Izzy", "(full name to be confirmed)", "Alleged management contact (\u201cDeclaration re: Dwayne and Izzy \u2013 Party Admission\u201d on docket); verify identity"),
       ("Cedric", "(full name to be confirmed)", "Named in docket entry \u201cIzzy / Dwayne / Cedric \u2013 SFHA and SSVF\u201d; verify identity and role"),
       ("Dwayne", "(full name to be confirmed)", "Alleged management contact; verify identity"),
       ("Rochelle", "(full name to be confirmed)", "Defendant's current case manager (per Defendant; not otherwise identified in the written record)"),
       ("Vincent Reyes", "", "Named in earlier Plaintiff witness materials. Defendant's instruction read \u201cVincent Rates\u201d; the record spells \u201cReyes\u201d \u2013 confirm spelling"),
       ("William \u201cWill\u201d Landrum", "", "Property management; notices, inspection coordination, complaints (Assistant Property Manager)"),
       ("Jerome Bradford", "", "Property management; February and April notice history, tenancy accounting"),
       ("Michael Blecker", "", "Executive Director, Swords to Plowshares (per custodian subpoena)"),
       ("Marissa Blecker", "", "Named staff/contact; role to be verified"),
       ("Carrie Sullivan", "", "Named nonprofit contact; role to be verified"),
       ("Kolby Losik", "", "Reported case manager; Dec. 11, 2025 communication-method message (Ex. AB); BBS Complaint 2002026002097"),
       ("Mark Villalobos", "", "Swords to Plowshares clinician named in BBS Complaint 2002026002098"),
       ("Brittany Mares", "", "Former management contact; notice of infestation (conditional)"),
       ("Elena Kim", "", "Property staff; firsthand communications or records (identity/employment to be confirmed)"),
       ("Joel Champion", "", "Named in earlier Plaintiff witness materials; subject not verified"),
       ("Jong Lee", "", "Named in earlier Plaintiff witness materials; subject not verified"),
       ("Tramecia Garner", "", "Named in housing-related notices; role to be verified"),
       ("Jose Sanchez", "", "Named as possible property/staff participant; affiliation not established")]


def make_subp5(w):
    """SUBP-002 for a Nov. 1 packet; mirrors BB.make_subpoena with the new date and a blank address for Defendant to complete."""
    ww = dict(w); ww["short"] = f"{w['name']}, {w['affil']} \u2013 address to be completed by Defendant (see Attachment 3)"
    ww["addr"] = "(to be completed by Defendant before service)"; ww["items"] = w["records"]
    return ww


def att3_pdf(w, path):
    f = [P("ATTACHMENT 3 TO SUBPOENA (SUBP-002) \u2013 RECORDS TO BE PRODUCED", h1),
         P(f"<i>Swords to Plowshares v. Gillson</i>, Case No. {CASE_NO}, {COURT}, {DEPT}. Trial: November 2, 2026, 9:00 a.m.", small), Spacer(1, 6),
         P(f"<b>Witness / custodian:</b> {esc(w['name'])} \u2013 {esc(w['affil'])}", small), P("<b>Address for service:</b> ______________________________________________ (to be completed by Defendant)", small), Spacer(1, 6),
         P("<b>Documents, electronically stored information and things to be produced at the time and place of trial:</b>", small)]
    for i, it in enumerate(w["records"], 1):
        f.append(P(f"{i}. {esc(it)}", small))
    f += [Spacer(1, 6), P("<b>Good cause and materiality (CCP \u00a7 1985(b)):</b> " + esc(w["why"]) + " The records are material to the issues set for trial, including retaliation, habitability, notice and service, and Defendant's affirmative defenses.", small),
          P(f"Dated: {SUBDATE}", small), P(ESIGN + " \u2013 Defendant in propria persona (electronic signature)", small)]
    return rl(f, path, "Attachment 3")


def subp001_pdf(w, path):
    vals = {"AttyPartyInfo[0].TextField1[0]": f"{NAME}, Defendant in pro per\n{ADDR1}, {ADDR2}", "AttyPartyInfo[0].Phone[0]": PHONE, "AttyPartyInfo[0].Email[0]": EMAIL,
            "CourtInfo[0].nameofcrt[0]": "SUPERIOR COURT OF CALIFORNIA, COUNTY OF SAN FRANCISCO", "CourtInfo[0].CrtStreet[0]": "400 McAllister Street", "CourtInfo[0].CrtMailingAdd[0]": "400 McAllister Street",
            "CourtInfo[0].CrtCityZip[0]": "San Francisco, CA 94102", "CourtInfo[0].CrtBranch[0]": "Civic Center Courthouse",
            "TitlePartyName[0].Party1[0]": "SWORDS TO PLOWSHARES, Plaintiff", "TitlePartyName[0].Party2[0]": "DONALD ERNEST GILLSON, Defendant",
            "CaseNumber[0].CaseNumber[0]": CASE_NO,
            "People[0].FillText1[0]": f"{w['name']}, {w['affil']}\nAddress: ____________________________ (to be completed by Defendant)",
            "Lia[0].HearingDate_dt[0]": "11/02/2026", "Lia[0].HearingTime_dt[0]": "9:00 a.m.", "Lia[0].Checkbox1[0]": True, "Lia[0].HearingDept_ft[0]": "606",
            "Lib[0].HearingDept_ft[0]": "400 McAllister Street, San Francisco, CA 94102",
            "List2[0].Lia[0].FillText108[0]": NAME, "List2[0].Lib[0].FillText109[0]": PHONE,
            "Sign[0].SigDate[0]": SUBDATE, "Sign[0].SigName[0]": ESIGN, "Sign[0].FillText108[0]": "Defendant in pro per"}
    return BB.fill_form(os.path.join(BB.FORMS, "subp001.pdf"), vals, path)


def pos020_pdf(path):
    vals = {"AttyPartyInfo[0].TextField1[0]": f"{NAME}, Defendant in pro per\n{ADDR1}, {ADDR2}", "AttyPartyInfo[0].Phone[0]": PHONE, "AttyPartyInfo[0].Email[0]": EMAIL,
            "CourtInfo[0].nameofcrt[0]": "SUPERIOR COURT OF CALIFORNIA, COUNTY OF SAN FRANCISCO", "CourtInfo[0].CrtStreet[0]": "400 McAllister Street",
            "CourtInfo[0].CrtCityZip[0]": "San Francisco, CA 94102", "TitlePartyName[0].Party1[0]": "SWORDS TO PLOWSHARES, Plaintiff", "TitlePartyName[0].Party2[0]": "DONALD ERNEST GILLSON, Defendant",
            "CaseNumber[0].CaseNumber[0]": CASE_NO}
    return BB.fill_form(os.path.join(BB.FORMS, "pos020.pdf"), vals, path)


def role_sheet(w, path):
    f = [P(f"WITNESS PACKET \u2013 {esc(w['name'].upper())}", h1), P(f"Case No. {CASE_NO} \u2013 {DEPT} \u2013 Trial Nov. 2, 2026, 9:00 a.m.", small), Spacer(1, 6),
         tbl([["Item", "Detail"], ["Witness", esc(w["name"])], ["Affiliation", esc(w["affil"])], ["Role", esc(w["role"])], ["Why the record identifies this witness", esc(w["why"])],
              ["Offer of proof (summary)", esc(w["offer"])], ["Documents (SUBP-002)", "Yes \u2013 Attachment 3 lists the categories. " + esc(w["basis"])],
              ["Address for service", "BLANK \u2013 no address for this witness appears in the sources. Defendant to complete on SUBP-001, SUBP-002 and the tracking sheet."],
              ["Packet contents", "1. This sheet  2. SUBP-001 (personal appearance)  3. SUBP-002 with Attachment 3 (records)  4. Blank proof of service (POS-020; SUBP-001 p. 2)  5. Service-tracking sheet"]],
             [1.7 * inch, 4.8 * inch], 8)]
    return rl(f, path, "Packet sheet")


def tracking_sheet(w, path):
    rows = [["Field", "Entry (complete by hand)"]] + [[x, ""] for x in ["Date subpoenas issued / clerk issuance or seal (if required)", "Address where witness will be served",
            "Process server (name, registration no.)", "Method (personal delivery, CCP \u00a7 1987)", "Date and time served", "Person served / description", "Witness fee and mileage tendered (Gov. Code \u00a7 68093)",
            "Proof of service signed and filed (date)", "Witness response / appearance confirmed", "Notes"]]
    f = [P(f"SERVICE-TRACKING SHEET \u2013 {esc(w['name'].upper())}", h1), P(f"Trial call November 2, 2026, 9:00 a.m., {DEPT}. Personal service on the witness is required for a personal-appearance subpoena; complete service before the trial call or apply to the Court for relief.", small),
         Spacer(1, 6), tbl(rows, [2.6 * inch, 3.9 * inch], 8)]
    return rl(f, path, "Tracking")


def witness_packet(w):
    t = w["tag"]; items = []
    items.append((f"{w['name']} \u2013 role and offer-of-proof sheet", role_sheet(w, os.path.join(TMP, f"s5_role_{t}.pdf"))))
    items.append((f"{w['name']} \u2013 SUBP-001 civil subpoena for personal appearance at trial", subp001_pdf(w, os.path.join(TMP, f"s5_s1_{t}.pdf"))))
    s2 = BB.make_subpoena(make_subp5(w)); att = att3_pdf(w, os.path.join(TMP, f"s5_att3_{t}.pdf"))
    s2m = A.merge([s2] if isinstance(s2, str) else s2, os.path.join(TMP, f"s5_s2_{t}.pdf"))
    items.append((f"{w['name']} \u2013 SUBP-002 civil subpoena (duces tecum) with Attachment 3", T.trim_subpoena(s2m, os.path.join(TMP, f"s5_s2t_{t}.pdf"))))
    items.append((f"{w['name']} \u2013 blank proof of service (POS-020)", pos020_pdf(os.path.join(TMP, f"s5_pos_{t}.pdf"))))
    items.append((f"{w['name']} \u2013 service-tracking sheet", tracking_sheet(w, os.path.join(TMP, f"s5_trk_{t}.pdf"))))
    BLANKS.append(f"Binder II, Tab 2.2 \u2013 {w['name']}: service address (SUBP-001, SUBP-002/Attachment 3, tracking sheet); signed proof of service; witness fee; clerk issuance if the court requires it")
    return items


# ------------------------------------------------------------------ Binder II generated documents
def addendum_pdf(path):
    rows = [["Witness", "Affiliation", "Role / subject (on information and belief)", "Compelled by"]]
    for w in W4:
        rows.append([w["name"], w["affil"], w["role"], "SUBP-001 + SUBP-002"])
    rows.append(["Swords to Plowshares staff (Tab 2.3 list)", "Plaintiff", "Officers, managing agents and employees; property management, notices, case management and clinical contacts", "CCP \u00a7 1987(b) notice (and SUBP-001 where not a managing agent)"])
    f = [P("ADDENDUM TO MASTER WITNESS LIST \u2013 ADDITIONAL TRIAL WITNESSES AND SUMMARY OF ANTICIPATED TESTIMONY", h1),
         P("The Master Witness List (preceding pages, including the Section VIII amendment as last revised) is unchanged. This addendum identifies the four additional witnesses for whom full subpoena packets are prepared in Tab 2.2, and Plaintiff's staff noticed in Tab 2.3. "
           "Descriptions are stated on information and belief and are drawn from the witness roster and docket.", small), Spacer(1, 6), tbl(rows, [1.3 * inch, 1.4 * inch, 2.7 * inch, 1.1 * inch], 7.5), Spacer(1, 10)]
    for w in W4:
        f += [P(f"<b>{esc(w['name'])}</b> \u2013 {esc(w['offer'])}", small), Spacer(1, 4)]
    return rl(f, path, "Addendum")


def notice_produce_pdf(path):
    hd = ParagraphStyle("nh", parent=h1, fontSize=12, leading=15)
    f = [P(f"{NAME}<br/>{ADDR1}, {ADDR2}<br/>{PHONE} | {EMAIL}<br/>Defendant in propria persona", small), Spacer(1, 8)] + [P(c, cen) for c in CAP]
    f += [Spacer(1, 4), tbl([["", ""], [f"SWORDS TO PLOWSHARES, Plaintiff,<br/>v.<br/>DONALD ERNEST GILLSON, Defendant.", f"Case No. {CASE_NO}<br/>{DEPT}<br/>Trial: November 2, 2026, 9:00 a.m."]], [3.4 * inch, 3.1 * inch], 8.5), Spacer(1, 8),
          P("DEFENDANT'S NOTICE TO ATTEND TRIAL AND PRODUCE OFFICERS, DIRECTORS, MANAGING AGENTS AND EMPLOYEES OF PLAINTIFF (CODE CIV. PROC., \u00a7 1987, subd. (b)); DEMAND FOR PRODUCTION OF DOCUMENTS AT TRIAL (\u00a7 1987, subd. (c))", hd), Spacer(1, 6),
          P("TO PLAINTIFF SWORDS TO PLOWSHARES AND ITS ATTORNEYS OF RECORD, John P. Zanghi, Francisco G. Torres, Zanghi Torres Adams LLP, 625 Market Street, 4th Floor, San Francisco, CA 94105:", small), Spacer(1, 4),
          P("PLEASE TAKE NOTICE that, under Code of Civil Procedure section 1987, subdivision (b), Defendant requires Plaintiff Swords to Plowshares to produce at trial, on <b>November 2, 2026 at 9:00 a.m., in Department 606</b>, Superior Court of California, County of San Francisco, 400 McAllister Street, San Francisco, California 94102, and to remain until excused, each of the following persons who is an officer, director or managing agent of Plaintiff, together with all other officers, agents and in-house staff of Plaintiff who have knowledge of the matters in issue. "
            "As to any listed person who is an employee but not an officer, director or managing agent, Defendant asks that Plaintiff produce the person voluntarily or by stipulation; Defendant reserves the right to serve a subpoena under section 1987, subdivision (a), on any such person.", small), Spacer(1, 6),
          tbl([["No.", "Person", "Basis in the record"]] + [[str(i), f"{n} {s}".strip(), b] for i, (n, s, b) in enumerate(STP, 1)] +
              [[str(len(STP) + 1), "All other Swords to Plowshares in-house staff named in the record", "Defendant will identify further names on the record at trial"]], [0.4 * inch, 2.1 * inch, 4.0 * inch], 8), Spacer(1, 6),
          P("<b>Demand for documents (\u00a7 1987, subd. (c)).</b> Plaintiff is further required to bring to trial the following documents and things in its possession, custody or control: (1) the complete tenancy file for Donald Ernest Gillson, 1030 Girard Road; (2) the rent ledger and all assistance-credit, subsidy and account entries; (3) the original Notices to Quit (Feb. 24 and Apr. 8, 2026), proofs of service, and the posting and mailing records; (4) all grievances, maintenance and pest-treatment records; (5) all communications with Defendant, the San Francisco Housing Authority, Adult Protective Services, the VA, and the U.S. Park Police concerning Defendant; (6) all case-management and clinical notes concerning Defendant in Plaintiff's possession; (7) all documents Plaintiff intends to use at trial.", small), Spacer(1, 4),
          P("<b>Timing.</b> Section 1987, subdivision (b) calls for service at least 10 days before the time required for attendance (and subdivision (c) at least 20 days for documents) unless the Court prescribes a shorter time. Trial call is November 2, 2026; this notice is served as soon as the trial date and department were fixed. Defendant requests that the Court prescribe the shorter time and order compliance, and that any non-compliance be addressed under \u00a7 1987, subdivision (b) (witness's statements, and where applicable the party's pleading, may be stricken or the party precluded).", small)]
    f += A.signature()
    BLANKS.append("Binder II, Tab 2.3: full surnames for Izzy, Cedric, Dwayne and Rochelle; confirm spelling Reyes vs. \u201cRates\u201d; confirm the role of each listed person; proof of service of this notice on Zanghi Torres Adams LLP (method, date, server)")
    return rl(f, path, "Notice to produce")


def pos_notice_pdf(path):
    f = [P("PROOF OF SERVICE \u2013 DEFENDANT'S \u00a7 1987(b) NOTICE (BLANK \u2013 TO BE COMPLETED BY SERVER)", h1), P(f"Case No. {CASE_NO}. I am over 18 and not a party. On ____________, 2026, I served the foregoing Notice to Attend Trial and Produce (CCP \u00a7 1987(b), (c)) on John P. Zanghi and Francisco G. Torres, Zanghi Torres Adams LLP, 625 Market Street, 4th Floor, San Francisco, CA 94105 by:  \u2610 personal delivery   \u2610 e-mail (CCP \u00a7 1010.6)   \u2610 first-class mail   \u2610 overnight delivery. I declare under penalty of perjury under the laws of California that the foregoing is true and correct.", small),
         Spacer(1, 16), P("Date: ____________    Name of server: ______________________    Signature: ______________________", small)]
    BLANKS.append("Binder II, Tab 2.3: blank proof of service for the \u00a7 1987(b) notice \u2013 server name, date, method, signature")
    return rl(f, path, "POS notice")


def summary_table_pdf(path):
    rows = [["Name", "Affiliation", "Role / relationship", "Subject of testimony", "Compelled by", "Service status"]]
    for w in W4:
        rows.append([w["name"], w["affil"], w["role"], w["offer"].split(": ", 1)[-1][:170] + "\u2026", "SUBP-001 + SUBP-002", "Prepared Nov. 1, 2026; address blank; not yet served"])
    for w in WITNESSES:
        rows.append([w["name"], w["role"], "Subpoenaed record custodian / witness (prepared Oct. 31, 2026)", w["why"][:150] + "\u2026", "SUBP-002", "Prepared Oct. 31, 2026; see service directory (Tab 2.2)"])
    for n, s, b in STP:
        rows.append([f"{n} {s}".strip(), "Swords to Plowshares (Plaintiff)", b, "Events, notices, management and case-management communications at issue", "\u00a7 1987(b) notice (Tab 2.3)", "Notice prepared Nov. 1, 2026; service on counsel to be completed"])
    return rl([P("WITNESS SUMMARY TABLE", h1), P("Name | Affiliation | Role/Relationship | Subject of testimony | Compelled by | Service status. The Master Witness List (Tab 2.1) remains the controlling list.", small), Spacer(1, 6),
               tbl(rows, [1.0 * inch, 1.0 * inch, 1.3 * inch, 1.7 * inch, 0.7 * inch, 0.8 * inch], 6.5)], path, "Witness summary")


def preservation_xref(path):
    rows = [["Preservation demand and notice to Francisco G. Torres, Esq. (Oct. 31, 2026)", "Tab 2.5 (this binder)", look(2, "Notice to Francisco Torres")],
            ["Hard-copy service / lodgment notice and Failure-to-Serve notice (Nov. 1, 2026)", "Binder I, Tab 1.3", look(1, "Notice of Lodgment")],
            ["Transmission log \u2013 e-mail service record; declaration of service", "Binder I, Tab 1.3", look(1, "Transmission Log")],
            ["Electronic service log declaration, Oct. 29 \u2013 Nov. 1, 2026", "Binder I, Tab 1.3", look(1, "Electronic Service Log")],
            ["Proofs of service on the SUBP-002 subpoenas (back of each form)", "Tab 2.2, previously prepared subpoenas", look(2, "Civil Subpoena (Duces Tecum) \u2013 William")],
            ["Existing proof of service in the court record (R05, key pages)", "Binder I, Tab 1.1 (record references)", look(1, "R05")]]
    return xref_table(path, "EXISTING PROOFS OF SERVICE AND PRESERVATION MATERIALS \u2013 CROSS-REFERENCE", "Existing proofs of service are cross-referenced to where they sit; they are not moved. The preservation demand is reproduced in this tab.", rows)


# ------------------------------------------------------------------ Binder I generated
def vesco_xref(path, cand):
    rows = []
    for lab, tab, p in cand:
        rows.append([esc(lab), f"Binder I, Tab {tab}", look(1, lab[:40])])
    rows += [["Court-facing Solano OST application / MC-410 (mentions \u201cVesco\u201d in routing)", "Binder V, Tab 5.1", look(5, "Application, Memorandum")]]
    return xref_table(path, "\u201cVESCO\u201d \u2013 DOCUMENT FINDER", "The defendant used the term \u201cVesco\u201d in these records. Every document in this set bearing that name or acronym is listed below with its Bates range.", rows)


def solano_xref(path):
    rows = [["Ex parte application for OST / Rule 1.100 request / memorandum / declaration / proposed order (court-facing)", "Binder V, Tab 5.1 (Solano Tab A)", look(5, "Application, Memorandum")],
            ["MC-410 (Solano) with attachment", "Binder V, Tab 5.1 (Solano Tab B)", look(5, "MC-410 with Attachment")],
            ["Complete Solano MC-410 binder (cover, Tabs A-I)", "Binder V, Tab 5.1", look(5, "Application, Memorandum")]]
    return xref_table(path, "SOLANO COURT FILINGS \u2013 CROSS-REFERENCE TO BINDER V", "The Solano court-facing documents are copied into this tab (next pages). The complete Solano binder remains in Binder V and is not moved.", rows)


# ------------------------------------------------------------------ main
def main():
    os.makedirs(ART, exist_ok=True)
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
    lead_memo = LM.build(os.path.join(TMP, "lead_memo.pdf")); med_ex = medical_exhibit(os.path.join(TMP, "two_medical_exhibit.pdf"))
    ada_items, seen = [], set()
    for fn, lab in ADA_EXHIBITS:
        path = os.path.join(HERE, "ada", fn); h = hashlib.md5(open(path, "rb").read()).hexdigest()
        if h in seen:
            continue
        seen.add(h); k = len(ada_items) + 1
        trimmed = T.trim_ada(path, os.path.join(TMP, f"two_ada_{k:02d}.pdf"))
        snipped = snip.snippet_pdf(trimmed, os.path.join(TMP, f"two_ada_{k:02d}_snip.pdf"), f"Binder I, Tab 1.4, Ex. {k} - {lab}", f"Ex. {k}")
        ada_items.append((f"ADA Ex. {k}. {lab} \u2013 operative language only (highlighted excerpts)", snipped))
    mc_sf = A.merge(make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} \u2014 {DEPT}",
        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall."],
        "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further proceedings in this case.", "Defendant", "Unlawful detainer",
        "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings."), os.path.join(TMP, "two_mc_sf.pdf"))
    mc_sol = A.merge(make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)", "Superior Court of California, County of Solano \u2013 Civil Harassment (Code Civ. Proc., \u00a7 527.6)",
        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall."],
        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings."), os.path.join(TMP, "two_mc_sol.pdf"))
    solano_ost = os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf")
    torres_notice = os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")
    # prior deliverables and incoming compilations
    keep = os.path.join(TMP, "s5_keep"); os.makedirs(keep, exist_ok=True)
    def stash(src, name):
        dst = os.path.join(keep, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
        return dst
    opening_art = stash(os.path.join(ART, "Gillson_Lead_Opening_Statement_CUD-26-682107.pdf"), "lead_opening.pdf")
    suppl_art = stash(os.path.join(ART, "Gillson_Supplemental_Trial_Record_CUD-26-682107_2026-11-01.pdf"), "supplemental.pdf")
    judge_stmt = os.path.join(INC, "judge_facing_statement.pdf"); roster = os.path.join(INC, "witness_roster.pdf"); master_bind = os.path.join(INC, "master_binder.pdf")
    master_soc = docx_to_pdf(os.path.join(INC, "master_soc.docx"), os.path.join(TMP, "s5_master_soc.pdf"), "MASTER STATEMENT OF THE CASE AND PROCEDURAL CHRONOLOGY (Word source)") if os.path.exists(os.path.join(INC, "master_soc.docx")) else None
    filing_md5 = {hashlib.md5(open(f, "rb").read()).hexdigest() for f in glob.glob(os.path.join(FIL if False else HERE, "filings", "*.pdf"))}
    extra_inc = [f for f in sorted(glob.glob(os.path.join(INC, "*.pdf"))) if os.path.basename(f) not in ("judge_facing_statement.pdf", "witness_roster.pdf", "master_binder.pdf")
                 and hashlib.md5(open(f, "rb").read()).hexdigest() not in filing_md5]
    print("extra incoming docs:", [os.path.basename(x) for x in extra_inc])
    va_full = os.path.join(HERE, "docs", "VA_Blue_Button_Report_2026-11-01.pdf"); excerpts = os.path.join(HERE, "docs", "VA_Blue_Button_Report_EXCERPTS.pdf")
    old = fitz.open(os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))
    def part(a, b, name):
        d = fitz.open(); d.insert_pdf(old, from_page=a - 1, to_page=b - 1); p = os.path.join(TMP, name); d.save(p); d.close(); return p
    decl = part(1, 3, "set_old_decl.pdf"); notices_old = part(45, 79, "set_old_notices.pdf"); va_old = part(80, 114, "set_old_va.pdf")
    CASEF = f"Gillson \u2013 {CASE_NO} \u2013 "

    # ---------------- Binder V (built first: Binder I cross-references it)
    xr5_rows = lambda: [["Lead Memorandum (statutory bars; mandatory federal exhaustion)", "Binder I, Tab 1.1", look(1, "Lead Memorandum")],
                        ["Notice to Francisco G. Torres, Esq. and preservation demand (Oct. 31, 2026)", "Binder II, Tab 2.5", look(2, "Notice to Francisco Torres")]]
    xr_sol = xref_table(os.path.join(TMP, "s5_xr_sol.pdf"), "CROSS-REFERENCE \u2013 MATERIALS HELD IN OTHER BINDERS",
                        "This binder is filed in a different court, so Tabs C-H repeat the San Francisco materials that the Solano application relies on. The full evidence set is not repeated; it is held as follows.",
                        [["Photographs and videos (Exs. 1-71, V1/V2)", "Binder III", "B3 Master Exhibit Directory"], ["VA and private medical records, correlation index", "Binder IV (confidential)", "B4 Tabs 4.1-4.3"],
                         ["Witness list and subpoenas", "Binder II", "B2 Tabs 2.1-2.5"], ["Emergency / Vesco papers and motions", "Binder I", "B1 Tabs 1.2-1.4"]])
    sol_tabs = [("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order", [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", solano_ost)]),
                ("B", "Request for Accommodations \u2013 MC-410 (Solano County) \u2013 CONFIDENTIAL IN PART", [("MC-410 with Attachment", mc_sol), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
                ("C", "Course of Conduct \u2013 Opening Notice and Integrated Statement of the Case (San Francisco, CUD-26-682107)", [("Transmission Log", translog), ("Master Integrated Statement of the Case", brief), ("Emergency Motion in Limine No. 1", mil)]),
                ("D", "Index of Record Irregularities (San Francisco record)", [("Line-by-line index", tabB)]),
                ("E", "Video Evidence \u2013 Audio-Visual Exhibit List, Foundation, Publication Plan", [("Audio-visual exhibit list", tabE)]),
                ("F", "Points and Authorities \u2013 Table of Authorities with Case Summaries", [("Memorandum", tabF)]),
                ("G", "Record References \u2013 San Francisco Court Record (R01\u2013R10), Key Pages Only", record_items),
                ("H", "San Francisco Superior Court Rule 1.100 Orders and Responses (July\u2013October 2026)", ada_items),
                ("I", "Cross-Reference to Evidence and Medical Binders", [("Materials held in Binders I-IV", xr_sol)])]
    items51 = [("Solano MC-410 binder cover", cover_sol(os.path.join(TMP, "s5_solcover.pdf")))]
    for L, ttl, its in sol_tabs:
        items51.append((f"Solano Tab {L} \u2013 {ttl}", A.tab_page(os.path.join(TMP, f"s5_soltab_{L}.pdf"), f"5.1-{L}", ttl)))
        items51 += [(f"Solano {L}: {lab}", pth) for lab, pth in its]
    rel52 = lambda: [["Solano ex parte application / OST / Rule 1.100 request (CCP \u00a7 527.6 petition papers)", "Binder V, Tab 5.1 (Solano Tab A)", look(5, "Application, Memorandum")],
                     ["Notice to Francisco G. Torres, Esq. and preservation demand", "Binder II, Tab 2.5", look(2, "Notice to Francisco Torres")],
                     ["Emergency Motion in Limine No. 1 (disqualification of counsel)", "Binder I, Tab 1.2", look(1, "Emergency Motion in Limine")]]
    rel53 = lambda: [["Lead Memorandum \u2013 statutory bars; federal-grant audit demand", "Binder I, Tab 1.1", look(1, "Lead Memorandum")],
                     ["Index of Record Irregularities and Indicia of Fraud", "Binder I, Tab 1.1", look(1, "Line-by-line index of record")],
                     ["Notice of Government Claims; RJN; Verified Statement of Disqualification", "Binder I, Tab 1.3", look(1, "Notice of Government Claims")]]
    b5 = [("5.1", "Solano County Superior Court \u2013 Full MC-410 Binder (Tabs A\u2013I)", items51, ""),
          ("5.2", "Restraining Order Framework \u2013 Connection to the Current Restraining Order Against Mr. Torres", [("Reserved \u2013 documents to be inserted", lambda: reserved(os.path.join(TMP, "s5_res52.pdf"), "Reserved \u2013 documents to be inserted.", "No document in the source set is specific to the current restraining order against Mr. Torres. Defendant to insert it when output is received. Related materials already in this set are listed below.", rel52()))], "Awaiting output"),
          ("5.3", "Malicious Prosecution Nexus", [("Reserved \u2013 documents to be inserted", lambda: reserved(os.path.join(TMP, "s5_res53.pdf"), "Reserved \u2013 documents to be inserted.", "No document in the source set is specific to a malicious-prosecution claim. Related materials already in this set are listed below.", rel53()))], "Reserved")]
    n5 = assemble5(5, cover5(5, os.path.join(TMP, "s5_cover5.pdf")), b5, CASEF + "Binder V \u2013 Solano County / MC-410", conf=True)
    print("B5", n5)

    # ---------------- Binder IV (confidential medical)
    corr, n_corr = correlation(os.path.join(TMP, "s5_corr.pdf"), excerpts, "")
    snips = snip.snippet_pdf(excerpts, os.path.join(TMP, "s5_va_snips.pdf"), "VA Blue Button report \u2013 findings correlated to case events", "VA excerpts", kw_re=KW)
    notice4 = rl([Spacer(1, 0.8 * inch), P("CONFIDENTIAL \u2013 MEDICAL INFORMATION", ORANGE), Spacer(1, 8), P("PROTECTED HEALTH INFORMATION \u2013 NOTICE OF CONFIDENTIALITY", h1),
                  P("This binder contains Defendant's private medical records and VA records. Authority: Cal. Rules of Court, rule 1.100(c)(4); Civ. Code, \u00a7 56 et seq. (CMIA); 38 U.S.C. \u00a7 7332; 45 C.F.R. \u00a7 164.512(e). "
                    "Do not file publicly. Lodge conditionally under seal (rule 2.551). Do not copy or disclose to anyone other than the Court and as authorized by Defendant. Defendant has designated these records as privileged and confidential.", small)], os.path.join(TMP, "s5_conf4.pdf"), "Confidential")
    b4 = [("4.1", "Confidentiality Notice \u2013 Protected Health Information", [("Notice of confidentiality and handling", notice4)], ""),
          ("4.2", "Medical & VA Records \u2013 Correlation Index, Private Records, VA Findings, VA Report, Agency Complaints",
           [("Correlation index (date | VA record | snippet | related event / exhibit)", corr), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex),
            ("Highlighted snippet pages from the VA Blue Button report", snips), ("VA Blue Button report \u2013 complete (215 pages)", va_full),
            ("VA excerpts as served Oct. 29-30, 2026 (Evidence Ex. 92)", va_old),
            ("BBS Complaint 2002026002097 \u2013 Kolby Losik", os.path.join(COMP, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
            ("BBS Complaint 2002026002098 \u2013 Mark Villalobos", os.path.join(COMP, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))], ""),
          ("4.3", "Solano APS & Care-Coordination Records", [("Reserved \u2013 documents to be inserted", reserved(os.path.join(TMP, "s5_res43.pdf"), "Reserved \u2013 documents to be inserted.", "No Solano County APS or care-coordination records are in the source set. San Francisco APS materials (Dec. 5, 2025 letter) appear in the Binder III photographic exhibits."))], "Reserved")]
    n4 = assemble5(4, cover5(4, os.path.join(TMP, "s5_cover4.pdf"), conf=True), b4, "CONFIDENTIAL \u2013 MEDICAL INFORMATION \u2013 " + CASEF + "Binder IV", conf=True)
    print("B4", n4)

    # ---------------- Binder III (master exhibit directory)
    photos = photo_exhibits(); vids = video_slips()
    photo_items = [(f"Ex. {p['n']} \u2013 {p['cat']}: {p['desc'][:90]}", p["pdf"]) for p in photos]
    vid_items = [(v["label"], v["pdf"]) for v in vids]
    notices_start = {}
    def exhibit_dir(path):
        import build as EBm
        rows = [[P(h, CELL8B) for h in ["Exhibit No.", "Description", "Date", "Type", "Evidence Code basis", "Bates"]]]
        def br(lab):
            for l2, (a, b) in BG.get(3, {}).items():
                if l2.startswith(lab):
                    return f"B3-{a:04d}\u2013{b:04d}"
            return "B3-0000\u20130000"
        for p in photos:
            rows.append([P(f"Ex. {p['n']}", CELL8), P(p["desc"][:200], CELL8), P(p["date"], CELL8), P(p["type"], CELL8), P(p["basis"].split(" (")[0], CELL8), P(br(f"Ex. {p['n']} \u2013 {p['cat']}:"), CELL8)])
        for v in vids:
            rows.append([P(f"Ex. {v['ex']}", CELL8), P(v["title"], CELL8), P(v["date"], CELL8), P(v["type"], CELL8), P(v["basis"], CELL8), P(br(v["label"]), CELL8)])
        rows.append([P("Exs. 72-91", CELL8), P("Evidentiary notices and video designations served Oct. 29-30, 2026 (as served)", CELL8), P("2026-10-29/30", CELL8), P("Notice", CELL8), P("Evid. Code \u00a7\u00a7 250, 1400-1401, 1410", CELL8), P(br("Evidentiary notices"), CELL8)])
        rows.append([P("Ex. 92", CELL8), P("VA records excerpts (served; confidential \u2013 held in Binder IV)", CELL8), P("2026-10-29/30", CELL8), P("Record", CELL8), P("Evid. Code \u00a7\u00a7 1271, 1280, 1560", CELL8), P(look(4, "VA excerpts as served").replace(" \u2013 ", "\u2013"), CELL8)])
        t = Table(rows, colWidths=[0.6 * inch, 2.55 * inch, 0.8 * inch, 0.8 * inch, 1.05 * inch, 0.7 * inch], repeatRows=1)
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#808080")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
        return rl([P("MASTER EXHIBIT INDEX \u2013 PHOTOGRAPHS, VIDEOS AND SERVED NOTICES", h1),
                   P("Exhibit No. | Description | Date | Type | Evidence Code basis | Bates. Videos are in the ZIP folder Binder3_Videos, named by exhibit number. Photographs are reproduced in full color.", small), Spacer(1, 6), t], path, "Exhibit index")
    b3 = [("3.1", "Master Exhibit Index and Foundation Declaration", [("Master exhibit index table (Exhibit | Description | Date | Type | Evidence Code basis | Bates)", lambda: exhibit_dir(os.path.join(TMP, "s5_exdir.pdf"))),
                                                               ("Declaration of Donald Ernest Gillson authenticating Exhibits 1-92 (as originally served)", decl)], ""),
          ("3.2", "Video / Audio-Visual Exhibits \u2013 Slip Sheets (files in ZIP folder Binder3_Videos)", [("Audio-visual exhibit list and publication plan", tabE)] + vid_items + [("Summary of exhibits", tabD)], ""),
          ("3.3", "Photographic Exhibits \u2013 Exhibits 1-71 (full color)", photo_items, ""),
          ("3.4", "Evidentiary Notices Served on Opposing Counsel, Oct. 29-30, 2026 (Exhibits 72-91, as served)", [("Evidentiary notices and video designations as served (Exs. 72-91)", notices_old)], "")]
    n3 = assemble5(3, cover5(3, os.path.join(TMP, "s5_cover3.pdf")), b3, CASEF + "Binder III \u2013 Master Exhibit Directory")
    print("B3", n3)

    # ---------------- Binder I
    vesco_cand = []
    def add_c(lab, tab, p):
        if mentions(p, r"vesco"):
            vesco_cand.append((lab, tab, p))
    t11 = [("Master Integrated Statement of the Case and Trial Brief (with Index of Record Irregularities and Summary of Exhibits)", brief),
           ("Lead Memorandum of Points and Authorities in Support of Emergency Dismissal, Mandatory Audit of Federal Grant Funds, and Injunctive Relief", lead_memo),
           ("Index of Record Irregularities and Indicia of Fraud (line-by-line)", tabB), ("Summary of Exhibits (exhibit and evidence list)", tabD),
           ("Streamlined Statement of the Case \u2013 four independent statutory bars and concise chronology", streamlined), ("Closing argument outline", tabG),
           ("Points and Authorities \u2013 memorandum with table of authorities", tabF)]
    for p in (opening_art, suppl_art):
        pass
    if os.path.exists(opening_art):
        t11.append(("Lead Opening Statement and Systemic Dossier (Nov. 1, 2026)", opening_art))
    if os.path.exists(suppl_art):
        t11.append(("Supplemental Trial Management Record (Nov. 1, 2026)", suppl_art))
    t11 += [("Court-review compilation \u2013 Master All-in-One Statement, Procedural Chronology and Register of Actions", judge_stmt), ("Master Trial Binder & Evidentiary Appendix (compiled Statement, witness and exhibit lists)", master_bind)]
    if master_soc:
        t11.append(("Master Statement of the Case and Procedural Chronology (Word source, rendered)", master_soc))
    t11 += [lab_p for lab_p in [(l, p) for (l, p) in [(x[0], x[1]) for x in record_items] if not re.match(r"^R(08|09|10)\b", x[0] if False else l)]]
    rec_early = [(x[0], x[1]) for x in record_items if not re.match(r"R(08|09|10)\b", x[0])]; rec_exparte = [(x[0], x[1]) for x in record_items if re.match(r"R(08|09|10)\b", x[0])]
    t11 = [x for x in t11 if x not in rec_early] + rec_early
    t11 += [(f"Additional court record document ({os.path.basename(f)})", f) for f in extra_inc]
    t12 = [("Emergency Motion in Limine No. 1 \u2013 Disqualify Zanghi Torres Adams LLP; Exclude VA-Derived Evidence; Rule 1.100 Accommodation; Declaration; [Proposed] Order", mil)] + rec_exparte
    t13 = [("Notice of Government Claims; Request for Judicial Notice; Verified Statement of Disqualification; Notice of Federal Rights; Points and Authorities", notice),
           ("Notice of Lodgment of Digital Case Repository and IP Protections; Notice of Hard-Copy Service (Nov. 1, 2026)", lodgment),
           ("Supplemental Notice of Active Monitoring, Digital Telemetry, and ESI Logs (Nov. 1, 2026)", telemetry),
           ("Notice of Plaintiff's Failure to Serve Statement of the Case and Pretrial Trial Materials; Objection (Nov. 1, 2026)", svc_notice),
           ("Declaration re Electronic Service Log, Oct. 29 - Nov. 1, 2026", svclog), ("Transmission Log \u2013 E-mail Service Record; Declaration of Service", translog)]
    t14 = [("Opening Statement; Application for Reasonable Accommodation and Emergency Judicial Access (Vesco) (Nov. 1, 2026)", opening),
           ("Request for Accommodations \u2013 MC-410 (San Francisco) with Attachment", mc_sf)] + ada_items
    t15 = [("Solano County court filings \u2013 cross-reference to Binder V", lambda: xref_table(os.path.join(TMP, "s5_x15.pdf"), "SOLANO COURT FILINGS \u2013 CROSS-REFERENCE TO BINDER V",
               "The Solano court-facing documents are copied into this tab (next pages). The complete Solano binder remains in Binder V and is not moved.",
               [["Ex parte application / OST / Rule 1.100 request / memorandum / declaration / proposed order", "Binder V, Tab 5.1 (Solano Tab A)", look(5, "Application, Memorandum")],
                ["MC-410 (Solano) with attachment", "Binder V, Tab 5.1 (Solano Tab B)", look(5, "MC-410 with Attachment")]])),
           ("Solano ex parte application for Order Shortening Time; Rule 1.100 request; memorandum; declaration; [proposed] order (court-facing copy)", solano_ost),
           ("Solano Request for Accommodations \u2013 MC-410 with attachment (court-facing copy)", mc_sol)]
    for lab, p in t11 + t12 + t13 + t14 + t15:
        if not callable(p):
            add_c(lab, "?", p)
    tabs_of = {id(x): "1.1" for x in t11}
    vesco_rows = []
    for tab, lst in (("1.1", t11), ("1.2", t12), ("1.3", t13), ("1.4", t14), ("1.5", t15)):
        for lab, p in lst:
            if not callable(p) and mentions(p, r"vesco"):
                vesco_rows.append((lab, tab, p))
    print("Vesco documents:", len(vesco_rows), [(r[0][:40], r[1]) for r in vesco_rows])
    def vesco_item():
        rows = [[esc(lab), f"Binder I, Tab {tab}", look(1, lab)] for lab, tab, p in vesco_rows]
        rows.append(["Solano OST / MC-410 routing papers (court-facing)", "Binder V, Tab 5.1", look(5, "Application, Memorandum")])
        return xref_table(os.path.join(TMP, "s5_vesco.pdf"), "\u201cVESCO\u201d \u2013 DOCUMENT FINDER", "The defendant used the term \u201cVesco\u201d. Every document in this set that bears that name or acronym is listed with its Bates range.", rows)
    t14 = t14 + [("\u201cVesco\u201d document finder", vesco_item)]
    t16 = [("Upcoming appointments and hearing calendar", calendar_pdf(os.path.join(TMP, "s5_calendar.pdf")))]
    b1 = [("1.1", "Master Statement of the Case", t11, ""), ("1.2", "Motions \u2013 Emergency, In Limine, Ex Parte and Emergency Hearing Papers, Proposed Orders", t12, ""),
          ("1.3", "Disqualification / Judicial Integrity / RJN / Government Claims / E-Service Log", t13, ""), ("1.4", "All ADA Materials \u2013 MC-410 Requests and Responses, Emergency ADA Requests, \u201cVesco\u201d", t14, ""),
          ("1.5", "Solano County Superior Court Filings and Orders (copies; full set in Binder V)", t15, ""), ("1.6", "Upcoming Appointments & Hearing Calendar", t16, "")]
    n1 = assemble5(1, cover5(1, os.path.join(TMP, "s5_cover1.pdf")), b1, CASEF + "Binder I \u2013 Statement of the Case", conf=False)
    print("B1", n1)

    # ---------------- Binder II
    t21 = [("Master Witness List, Offers of Proof, Section VIII Amendment and Preservation Request (as last revised)", tabC),
           ("Addendum \u2013 additional trial witnesses and summary of anticipated testimony", addendum_pdf(os.path.join(TMP, "s5_addendum.pdf"))),
           ("Consolidated witness roster (court-review compilation, incl. register of witnesses)", roster)]
    t22 = []
    for w in W4:
        t22 += witness_packet(w)
    sub_items = [(f"Civil Subpoena (Duces Tecum) \u2013 {w['name']} (prepared Oct. 31, 2026)",
                  T.trim_subpoena(A.merge(make_subpoena(w), os.path.join(TMP, f"s5_old_{w['tag']}.pdf")), os.path.join(TMP, f"s5_old_{w['tag']}_trim.pdf"))) for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY (PREVIOUSLY PREPARED SUBPOENAS)", h1), grid([["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES], [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "s5_svc.pdf"))
    t22 += [("Service directory \u2013 previously prepared SUBP-002 subpoenas", svc)] + sub_items
    t23 = [("Notice to Attend Trial and Produce (CCP \u00a7 1987(b)); Demand for Documents (\u00a7 1987(c))", notice_produce_pdf(os.path.join(TMP, "s5_n1987.pdf"))),
           ("Blank proof of service \u2013 \u00a7 1987(b) notice", pos_notice_pdf(os.path.join(TMP, "s5_n1987_pos.pdf")))]
    t24 = [("Witness summary table", summary_table_pdf(os.path.join(TMP, "s5_wsum.pdf")))]
    t25 = [("Notice to Francisco Torres, Esq., October 31, 2026 (preservation demand)", torres_notice), ("Existing proofs of service and preservation materials \u2013 cross-reference", lambda: preservation_xref(os.path.join(TMP, "s5_pres.pdf")))]
    b2 = [("2.1", "Master Witness List (incl. Section VIII Amendment)", t21, ""), ("2.2", "Fully Prepared Subpoenas \u2013 Wallingford, Whittaker, Timms, Gibson; Previously Prepared Subpoenas", t22, ""),
          ("2.3", "Swords to Plowshares Staff \u2013 Notice to Produce at Trial (CCP \u00a7 1987(b), (c))", t23, ""), ("2.4", "Witness Summary Table", t24, ""), ("2.5", "Preservation Demands and Existing Proofs of Service", t25, "")]
    n2 = assemble5(2, cover5(2, os.path.join(TMP, "s5_cover2.pdf")), b2, CASEF + "Binder II \u2013 Witness List & Subpoenas")
    print("B2", n2)
    # second pass so cross-binder references resolve to final Bates
    n1 = assemble5(1, cover5(1, os.path.join(TMP, "s5_cover1.pdf")), b1, CASEF + "Binder I \u2013 Statement of the Case")
    n2 = assemble5(2, cover5(2, os.path.join(TMP, "s5_cover2.pdf")), b2, CASEF + "Binder II \u2013 Witness List & Subpoenas")
    n5 = assemble5(5, cover5(5, os.path.join(TMP, "s5_cover5.pdf")), b5, CASEF + "Binder V \u2013 Solano County / MC-410", conf=True)
    n1 = assemble5(1, cover5(1, os.path.join(TMP, "s5_cover1.pdf")), b1, CASEF + "Binder I \u2013 Statement of the Case")
    n3 = assemble5(3, cover5(3, os.path.join(TMP, "s5_cover3.pdf")), b3, CASEF + "Binder III \u2013 Master Exhibit Directory")
    for n in (1, 2, 5):
        compress_scans(OUT5[n])
    json.dump({str(k): {l: list(v) for l, v in d.items()} for k, d in BG.items()}, open(os.path.join(TMP, "s5_bates.json"), "w"))
    json.dump(BLANKS, open(os.path.join(TMP, "s5_blanks.json"), "w"), indent=1)
    print("done", {1: n1, 2: n2, 3: n3, 4: n4, 5: n5})


if __name__ == "__main__":
    main()
