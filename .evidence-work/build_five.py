"""
Builds exactly five deliverables from the same components as build_two.py:
  1  Statement of the Case - Full Judicial Binder
  2  Witness List and Subpoena Paperwork
  3  Evidence Binder - photographs, videos, master index
  4  Private Medical Records and Vesco Correlation (CONFIDENTIAL) - opens with the Vesco application, motions, and statements
  5  Solano County - Full MC-410
Every binder opens with a cover, the Master Index of the five-binder set (with a former-tab cross-reference), and its own exhibit index.
"""
import os, sys, glob, hashlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz
import build_two as B2
import build_allinone as A
from build_allinone import P, rl, grid, h1, h2, cen, small, TMP, ART, COMP, HERE, FIL, FILINGS, CASE_NO, COURT, DEPT, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer
import build_integrated as I
import build_notice as N
import build_brief as B
import build_record_refs as RR
import build_correlation as CO
import trim as T
import build_mil as M
import build_notice_service as NS
import build_opening as OP
import build_lead_memo as LM
import build_notice_lodgment as NL
import build_notice_telemetry as NT
import build_service_log as SL
import build_translog as TL
import snip
from build import CATEGORIES
from build_binders import WITNESSES, ADA_EXHIBITS, make_mc410, make_subpoena, medical_exhibit, compress_scans
from build_final import cover_sol

EB = sys.modules["build"]  # the evidence-binder module (exhibits, PAGE_OF)

OUT = {
    1: os.path.join(ART, "Binder_1_Statement_of_the_Case_Full_Judicial_Binder.pdf"),
    2: os.path.join(ART, "Binder_2_Witness_List_and_Subpoena_Paperwork.pdf"),
    3: os.path.join(ART, "Binder_3_Evidence_Binder_Photographs_and_Videos.pdf"),
    4: os.path.join(ART, "Binder_4_Private_Medical_Records_and_Vesco_Correlation_CONFIDENTIAL.pdf"),
    5: os.path.join(ART, "Binder_5_Solano_County_Full_MC-410.pdf"),
}
PREFIXES = {1: "SOC", 2: "WIT", 3: "EVD", 4: "MED", 5: "SOL"}
NAMES = {
    1: "Statement of the Case \u2013 Full Judicial Binder",
    2: "Witness List and Subpoena Paperwork",
    3: "Evidence Binder \u2013 Photographs, Videos, and Master Index",
    4: "Private Medical Records and Vesco Correlation (CONFIDENTIAL)",
    5: "Solano County \u2013 Full MC-410",
}
CONTENTS = {
    1: "Opening papers: Vesco application, lead memorandum (fiduciary duty, federal funding records, retaliation), notices, Motion in Limine No. 1, Master Integrated Statement and Streamlined Statement of the Case; index of record irregularities; points and authorities; closing argument; record references R01\u2013R10; Court's Rule 1.100 orders.",
    2: "Witness list with offer of proof and Section VIII amendment; notice to counsel; service directory; civil subpoenas (SUBP-002 with Attachment 3).",
    3: "Evidence list; video list (two suites, links, publication plan); color photograph index (every exhibit); Evidence Exhibit Binder (photographs, notices, agency records, video links).",
    4: "Front: Vesco application, Motion in Limine No. 1, Statement of the Case. Then: medical-record-to-Vesco correlation; MC-410 and ED record; VA Blue Button excerpts and full report; Court's Rule 1.100 responses.",
    5: "Solano County: ex parte application for order shortening time; MC-410 with attachment; confidential ED record; Vesco application; San Francisco Rule 1.100 orders.",
}
FORMER_TABS = [
    ("A", "Opening papers; statements of the case", "Binder 1, Tab A (Vesco application, Motion in Limine No. 1 and statements also at Binder 4, Tab A)"),
    ("B", "Index of record irregularities", "Binder 1, Tab B"),
    ("C", "Witness list", "Binder 2, Tab A"),
    ("D", "Evidence list", "Binder 3, Tab A"),
    ("E", "Video list", "Binder 3, Tab B"),
    ("F", "Points and authorities", "Binder 1, Tab C"),
    ("G", "Closing argument", "Binder 1, Tab D"),
    ("H", "Record references R01\u2013R10", "Binder 1, Tab E"),
    ("I", "Notice to counsel; subpoenas", "Binder 2, Tabs B\u2013C"),
    ("J", "MC-410 and confidential medical exhibit", "Binder 4, Tab C (San Francisco); Binder 5, Tabs B\u2013C (Solano)"),
    ("K", "Rule 1.100 orders and responses", "Binder 1, Tab F; also Binder 4, Tab E and Binder 5, Tab E"),
    ("L", "Evidence Exhibit Binder", "Binder 3, Tab D"),
]


def set_index(path, current):
    f = [P("MASTER INDEX OF THE FIVE-BINDER SET", h1),
         P(f"<i>Swords to Plowshares v. Gillson</i>, {COURT}, Case No. {CASE_NO}, {DEPT}. You are reading <b>Binder {current} of 5</b>. "
           "Each binder is a single bookmarked, tabbed, Bates-numbered PDF with its own exhibit index, consistent with Cal. Rules of Court, rule 3.1110(f) "
           "(identification of exhibits and bookmarks for electronic exhibits). Confidential medical material is marked under rule 1.100(c)(4).", small), Spacer(1, 8)]
    rows = [["Binder", "Title", "Contents", "Bates prefix"]]
    for n in range(1, 6):
        mark = "  (this binder)" if n == current else ""
        rows.append([str(n), f"<b>{NAMES[n]}</b>{mark}", CONTENTS[n], f"{PREFIXES[n]}-0001"])
    f.append(grid(rows, [0.55 * inch, 1.6 * inch, 3.5 * inch, 0.85 * inch]))
    f += [Spacer(1, 10), P("Cross-reference: former tab to new location", h2),
          P("Papers drafted for the earlier single binder cite its Tabs A\u2013L. The key below shows where each former tab now sits.", small)]
    rows = [["Former tab", "Subject", "Now at"]] + [[t, s, w] for t, s, w in FORMER_TABS]
    f.append(grid(rows, [0.8 * inch, 2.4 * inch, 3.3 * inch]))
    return rl(f, path, "Master Index of the Five-Binder Set")


def cover(path, n, lines):
    f = [Spacer(1, 1.1 * inch), P(f"BINDER {n} OF 5", ParagraphStyle("b5", parent=cen, fontSize=13, leading=20)),
         P(NAMES[n].upper(), ParagraphStyle("big", parent=h1, fontSize=22, leading=30)), Spacer(1, 18),
         P("<i>Swords to Plowshares v. Donald Ernest Gillson, Ed.D.</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P(f"{COURT} \u2014 {DEPT}", cen), P(f"Case No. {CASE_NO} \u2014 Trial call November 2, 2026, 9:00 a.m.", cen), Spacer(1, 24),
         P(f"Submitted by {NAME}, Defendant in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 24)]
    f += [P(t, small) for t in lines]
    f += [Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, f"Cover - Binder {n}")


def photo_index(path, binder_start):
    """Index of every numbered exhibit in the Evidence Exhibit Binder with both its own page and its page in this binder."""
    rows = [["Ex.", "Cat.", "Captured", "Description", "GILLSON page", "Binder page"]]
    for e in EB.exhibits:
        short = e["desc"].split(". ")[0].strip()
        short = short if len(short) <= 135 else short[:132] + "..."
        gp = EB.PAGE_OF.get(e["no"], 0)
        bp = f"{binder_start + gp - 1}" if binder_start and gp else "-"
        rows.append([str(e["no"]), e["cat"], e["dt"].strftime("%m/%d/%Y %-I:%M %p"), short, str(gp), bp])
    f = [P("COLOR PHOTOGRAPH AND EXHIBIT INDEX", h1),
         P(f"Every numbered exhibit in the Evidence Exhibit Binder ({len(EB.exhibits)} exhibits; {EB.N_PHOTO} are color photographs and screenshots taken on the declarant's own device; "
           "the rest are e-mailed notices, agency records, video links, and VA excerpts). \"GILLSON page\" is the page number stamped at the foot of the exhibit itself "
           "(Bates GILLSON-); \"Binder page\" is the page in this binder.", small), Spacer(1, 6),
         grid(rows, [0.4 * inch, 0.4 * inch, 1.1 * inch, 3.0 * inch, 0.8 * inch, 0.8 * inch])]
    return rl(f, path, "Color Photograph and Exhibit Index")


def assemble(n, front_cover_lines, sections, footer):
    A.PREFIX = PREFIXES[n]
    A.FRONT = [("Master Index of the Five-Binder Set", set_index(os.path.join(TMP, f"five_set_{n}.pdf"), n))]
    cov = cover(os.path.join(TMP, f"five_cover_{n}.pdf"), n, front_cover_lines)
    pages = A.assemble(OUT[n], cov, sections, footer)
    compress_scans(OUT[n])
    print(f"Binder {n}: {pages} pages"); return pages


if __name__ == "__main__":
    only = {int(x) for x in os.environ.get("ONLY", "1,2,3,4,5").split(",")}
    figs = I.render_figs()
    I.build_pdf(figs, I.OUT_PDF); I.build_docx(figs, I.OUT_DOCX)
    notice = N.build_notice(os.path.join(TMP, "notice_opening.pdf"))
    mil = M.build_mil(os.path.join(TMP, "mil_1.pdf"))
    svc_notice = NS.build(os.path.join(TMP, "notice_failure_to_serve.pdf"))
    opening = OP.build(os.path.join(TMP, "opening_statement.pdf"))
    lead_memo = LM.build(os.path.join(TMP, "lead_memo.pdf"))
    lodgment = NL.build(os.path.join(TMP, "notice_lodgment.pdf"))
    telemetry = NT.build(os.path.join(TMP, "notice_telemetry.pdf"))
    svclog = SL.build(os.path.join(TMP, "service_log.pdf"))
    translog = TL.build(os.path.join(TMP, "translog.pdf"))
    photo_counts = {l: len(items) for l, _, items in CATEGORIES}
    record_items = RR.record_items()
    brief = B.build_brief(os.path.join(TMP, "trial_brief.pdf"))
    streamlined = T.streamlined_statement(os.path.join(TMP, "streamlined_statement.pdf"))
    print("drafted papers")

    OP_LBL = "Opening Statement; Application for Reasonable Accommodation and Emergency Judicial Access (Vesco) (Nov. 1, 2026)"
    MIL_LBL = "Emergency Motion in Limine No. 1 \u2013 Disqualify Zanghi Torres Adams LLP; Exclude VA-Derived Evidence; Rule 1.100 Accommodation; Declaration; [Proposed] Order"
    STREAM_LBL = "Streamlined Statement of the Case \u2013 Four Independent Statutory Bars and Concise Chronology"
    BRIEF_LBL = "Master Integrated Statement of the Case and Trial Brief; Index of Record Irregularities; Summary of Exhibits (LEAD DOCUMENT)"
    tabA_items = [
        (OP_LBL, opening),
        ("Lead Memorandum of Points and Authorities \u2013 Fiduciary Duty, Conflict of Interest, Federal Funding Records, and Retaliatory Prosecution (Nov. 1, 2026)", lead_memo),
        ("Notice of Lodgment of Digital Case Repository (calindex.vercel.app) and IP Protections; Notice of Hard-Copy Service via Rapid Legal (Nov. 1, 2026)", lodgment),
        ("Supplemental Notice of Active Monitoring, Digital Telemetry, and ESI Logs - External Access to calindex.vercel.app (Nov. 1, 2026)", telemetry),
        ("Declaration re Electronic Service Log, Oct. 29 - Nov. 1, 2026 (transmissions to Dept. 606, ADA Coordinator, counsel)", svclog),
        ("Notice of Plaintiff's Failure to Serve Statement of the Case and Pretrial Trial Materials; Objection (Nov. 1, 2026)", svc_notice),
        ("Transmission Log - E-mail Service Record of Opening Papers and Notices, Oct. 29 - Nov. 1, 2026; Declaration of Service", translog),
        (BRIEF_LBL, brief),
        ("Notice of Government Claims; Request for Judicial Notice; Verified Statement of Disqualification; Notice of Federal Rights; Points and Authorities", notice),
        (MIL_LBL, mil),
        (STREAM_LBL, streamlined),
    ]
    tabB = A.irregularities(os.path.join(TMP, "five_B.pdf")); tabC = A.witness_list(os.path.join(TMP, "five_C.pdf"))
    tabD = A.evidence_list(os.path.join(TMP, "five_D.pdf"), photo_counts); tabE = A.video_list(os.path.join(TMP, "five_E.pdf"))
    tabF = A.points_authorities(os.path.join(TMP, "five_F.pdf")); tabG = A.closing(os.path.join(TMP, "five_G.pdf"))
    med_ex = medical_exhibit(os.path.join(TMP, "five_medical_exhibit.pdf"))

    ada_items, seen, ada_no, ada_by_hash = [], set(), {}, {}
    for fn, lab in ADA_EXHIBITS:
        path = os.path.join(HERE, "ada", fn); h = hashlib.md5(open(path, "rb").read()).hexdigest()
        if h in seen:
            ada_no[fn] = ada_by_hash[h]; continue
        seen.add(h); k = len(ada_items) + 1; ada_by_hash[h] = k; ada_no[fn] = k
        trimmed = T.trim_ada(path, os.path.join(TMP, f"five_ada_{k:02d}.pdf"))
        snipped = snip.snippet_pdf(trimmed, os.path.join(TMP, f"five_ada_{k:02d}_snip.pdf"), f"Rule 1.100 Order, Ex. {k} - {lab}", f"Ex. {k}")
        ada_items.append((f"Ex. {k}. {lab} \u2013 operative language only (highlighted excerpts)", snipped))
    corr = CO.build(os.path.join(TMP, "five_correlation.pdf"), {key: ada_no[fn] for key, fn in CO.ADA_FILES.items()})

    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} \u2014 {DEPT}",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further proceedings in this case.", "Defendant", "Unlawful detainer",
                       "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    mc_sf_merged = A.merge(mc_sf, os.path.join(TMP, "five_mc_sf.pdf"))
    mc_sol = make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)",
                        "Superior Court of California, County of Solano \u2013 Civil Harassment (Code Civ. Proc., \u00a7 527.6)",
                        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026. I ask to appear by Zoom at every hearing in this matter until those orders are lifted. The emergency department record is attached as a confidential exhibit."],
                        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings.")
    mc_sol_merged = A.merge(mc_sol, os.path.join(TMP, "five_mc_sol.pdf"))

    sub_items = [(f"Civil Subpoena (Duces Tecum) \u2013 {w['name']}",
                  T.trim_subpoena(A.merge(make_subpoena(w), os.path.join(TMP, f"five_subp_{w['tag']}.pdf")), os.path.join(TMP, f"five_subp_{w['tag']}_trim.pdf")))
                 for w in WITNESSES]
    svc_rows = [["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY", h1), grid(svc_rows, [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "five_svc.pdf"))
    torres = os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")
    va_excerpts = os.path.join(HERE, "docs", "VA_Blue_Button_Report_EXCERPTS.pdf")
    va_full = os.path.join(COMP, "VA_Blue_Button_Report_2026-11-01.pdf")
    ev_binder = os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf")

    # ------------------------------------------------ Binder 1
    if 1 in only:
        assemble(1, ["This binder is the full judicial statement of the case. Tab A opens with the Vesco application and accommodation request, the lead memorandum of points and authorities on fiduciary duty, federal funding records, and retaliation, the notices, the service records, the Master Integrated "
                     "Statement of the Case and Trial Brief (lead document), Emergency Motion in Limine No. 1, and the Streamlined Statement. Tabs B through F carry the index of record irregularities, "
                     "the points and authorities, the closing argument, key pages of the filed record (R01\u2013R10), and this Court's Rule 1.100 orders. The witness list and subpoenas are Binder 2; the evidence "
                     "and videos are Binder 3; the confidential medical records are Binder 4; the Solano County MC-410 is Binder 5."],
                 [("A", "Opening Papers: Vesco Application, Notices, Motion in Limine No. 1, and Statements of the Case", tabA_items),
                  ("B", "Index of Record Irregularities and Indicia of Fraud", [("Line-by-line index", tabB)]),
                  ("C", "Points and Authorities", [("Memorandum with table of authorities", tabF)]),
                  ("D", "Closing Argument", [("Closing argument outline", tabG)]),
                  ("E", "Record References \u2013 Chronology of the Filed Court Record (R01\u2013R10), Key Pages Only", record_items),
                  ("F", "Rule 1.100 Orders and Responses of this Court", ada_items)],
                 "Gillson \u2013 Binder 1 of 5 \u2013 Statement of the Case \u2013 CUD-26-682107")

    # ------------------------------------------------ Binder 2
    if 2 in only:
        assemble(2, ["This binder holds the witness list with offer of proof (including the Section VIII amendment, stated on information and belief), the notice to counsel, the subpoena "
                     "service directory, and one civil subpoena (SUBP-002 with Attachment 3) for each witness. Subpoenas must be issued by the clerk and personally served, with witness fees tendered on demand "
                     "(Code Civ. Proc., \u00a7\u00a7 1985, 1987; Gov. Code, \u00a7 68093); the proof of service on each SUBP-002 is completed after service."],
                 [("A", "Witness List and Offer of Proof", [("Witness list, offer of proof, and Section VIII amendment", tabC)]),
                  ("B", "Notice to Counsel and Subpoena Service Directory",
                   [("Notice to Francisco Torres, Esq., October 31, 2026", torres), ("Service directory", svc)]),
                  ("C", "Civil Subpoenas (SUBP-002 with Attachment 3)", sub_items)],
                 "Gillson \u2013 Binder 2 of 5 \u2013 Witness List and Subpoena Paperwork \u2013 CUD-26-682107")

    # ------------------------------------------------ Binder 3 (two passes so the photo index shows true binder pages)
    if 3 in only:
        lines = ["This binder is the evidence binder. Tab A is the exhibit and evidence list; Tab B is the video list with links, foundation, and publication plan (the videos are hosted online and are "
                 "cited by link and QR code in Tab D; no video file is embedded in this PDF); Tab C indexes every exhibit, including each color photograph, by date, description, and page; Tab D is the Evidence "
                 "Exhibit Binder itself. Master index of exhibits with Bates ranges follows the cover.",
                 "Note: Tab D includes Category D (injuries and medical records) and Category M (VA excerpts) as already served; the full private medical record is in Binder 4 only."]
        def sections3(start):
            return [("A", "Evidence List", [("Exhibit and evidence list", tabD)]),
                    ("B", "Video List \u2013 Audio-Visual Exhibits, Foundation, Publication Plan", [("Audio-visual exhibit list", tabE)]),
                    ("C", "Color Photograph and Exhibit Index", [("Index of every exhibit with page references", photo_index(os.path.join(TMP, "five_photo_index.pdf"), start))]),
                    ("D", "Evidence Exhibit Binder \u2013 Photographs, Notices, Agency Records, Video Links", [("Gillson Evidence Exhibit Binder (Bates GILLSON-)", ev_binder)])]
        foot3 = "Gillson \u2013 Binder 3 of 5 \u2013 Evidence Binder \u2013 CUD-26-682107"
        assemble(3, lines, sections3(0), foot3)
        toc = fitz.open(OUT[3]).get_toc()
        sheet_pg = [pg for lvl, title, pg in toc if lvl == 2 and "Gillson Evidence Exhibit Binder" in title][0]
        assemble(3, lines, sections3(sheet_pg + 1), foot3)

    # ------------------------------------------------ Binder 4
    if 4 in only:
        assemble(4, ["CONFIDENTIAL IN PART \u2013 Cal. Rules of Court, rule 1.100(c)(4); Civ. Code, \u00a7 56 et seq. Tab A opens with the emergency Vesco application, Emergency Motion in Limine No. 1, and the "
                     "Statements of the Case. Tab B correlates each dated entry in defendant's medical record to the Vesco and Rule 1.100 proceedings. Tab C is the San Francisco MC-410 with the John Muir Health "
                     "emergency-department record and photographs; Tab D is the VA Blue Button excerpts relied on; Tab E is the full 215-page VA report, to be lodged conditionally under seal only; "
                     "Tab F is the Court's Rule 1.100 responses that the correlation cites."],
                 [("A", "Emergency Vesco Application, Motion in Limine No. 1, and Statements of the Case",
                   [(OP_LBL, opening), (MIL_LBL, mil), (STREAM_LBL, streamlined), (BRIEF_LBL, brief)]),
                  ("B", "Correlation of Medical Record to the Vesco Accommodation Proceedings \u2013 CONFIDENTIAL", [("Date-by-date correlation and condition-to-accommodation matrix", corr)]),
                  ("C", "Request for Accommodations \u2013 MC-410 (Dept. 606) \u2013 CONFIDENTIAL IN PART",
                   [("MC-410 with Attachment", mc_sf_merged), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)]),
                  ("D", "VA Medical Records \u2013 Excerpts Relied On \u2013 CONFIDENTIAL", [("VA Blue Button excerpts (34 of 215 pages), Aug. 1 \u2013 Nov. 1, 2026", va_excerpts)]),
                  ("E", "VA Medical Records \u2013 Full Blue Button Report (215 pages) \u2013 CONFIDENTIAL \u2013 LODGE UNDER SEAL ONLY", [("Full VA Blue Button report generated Nov. 1, 2026, 6:53 a.m.", va_full)]),
                  ("F", "Rule 1.100 Orders and Responses of this Court", ada_items)],
                 "Gillson \u2013 Binder 4 of 5 \u2013 Private Medical Records and Vesco Correlation \u2013 CONFIDENTIAL (CRC 1.100(c)(4))")

    # ------------------------------------------------ Binder 5
    if 5 in only:
        assemble(5, ["This binder is the complete Solano County accommodation filing: the ex parte application for an order shortening time with the Rule 1.100 request, memorandum, declaration, and "
                     "proposed order (Tab A); the Judicial Council form MC-410 with its attachment (Tab B); the confidential John Muir Health emergency-department record (Tab C); the Vesco "
                     "application filed in San Francisco (Tab D); and the San Francisco Court's Rule 1.100 orders (Tab E). Tabs B and C are confidential in part under rule 1.100(c)(4)."],
                 [("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order",
                   [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
                  ("B", "Request for Accommodations \u2013 MC-410 (Solano County) \u2013 CONFIDENTIAL IN PART", [("MC-410 with Attachment", mc_sol_merged)]),
                  ("C", "CONFIDENTIAL Medical Exhibit \u2013 John Muir Health ED Record", [("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)]),
                  ("D", "Supporting Application \u2013 Vesco Application and Opening Statement (San Francisco)", [(OP_LBL, opening)]),
                  ("E", "San Francisco Superior Court Rule 1.100 Orders and Responses (July\u2013October 2026)", ada_items)],
                 "Gillson \u2013 Binder 5 of 5 \u2013 Solano County \u2013 Full MC-410 \u2013 Confidential in part (CRC 1.100(c)(4))")

    keep = {os.path.abspath(p) for p in OUT.values()}
    for p in glob.glob(os.path.join(ART, "*")):
        if os.path.abspath(p) not in keep:
            os.remove(p)
    print("done")
