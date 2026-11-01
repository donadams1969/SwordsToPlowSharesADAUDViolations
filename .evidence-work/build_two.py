"""
Builds exactly two deliverables:
  Gillson_FINAL_All_In_One_Trial_Binder_SAN_FRANCISCO_CUD-26-682107.pdf
  Gillson_FINAL_All_In_One_Binder_SOLANO_COUNTY.pdf
Each opens with the Notice (government claims / disqualification / federal rights) and the
Integrated Statement of the Case, then its own tabs. Removes every other PDF in the artifacts dir.
"""
import os, sys, glob, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_allinone as A
from build_allinone import P, rl, grid, h1, cen, small, TMP, ART, COMP, HERE, FIL, FILINGS, CASE_NO, COURT, DEPT, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer
import build_integrated as I
import build_notice as N
import build_brief as B
import build_record_refs as RR
import trim as T
import build_mil as M
import build_notice_service as NS
import build_opening as OP
import build_notice_lodgment as NL
import build_notice_telemetry as NT
import build_service_log as SL
import build_translog as TL
import snip
import hashlib
from build import CATEGORIES
from build_binders import WITNESSES, ADA_EXHIBITS, make_mc410, make_subpoena, medical_exhibit, compress_scans
from build_final import excerpt_items, cover_sol

OUT_SF = os.path.join(ART, "Gillson_FINAL_All_In_One_Trial_Binder_SAN_FRANCISCO_CUD-26-682107.pdf")
OUT_SOL = os.path.join(ART, "Gillson_FINAL_All_In_One_Binder_SOLANO_COUNTY.pdf")
WEB = os.path.join(os.path.dirname(HERE), "public", "binders")


def cover_sf(path):
    f = [Spacer(1, 1.2 * inch), P("ALL-IN-ONE TRIAL BINDER", ParagraphStyle("big", parent=h1, fontSize=24, leading=32)),
         P("San Francisco \u2014 Final Edition", ParagraphStyle("sub", parent=cen, fontSize=14, leading=22)), Spacer(1, 24),
         P("<i>Swords to Plowshares v. Gillson</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P(f"{COURT} \u2014 {DEPT}", cen), P(f"Case No. {CASE_NO} \u2014 Trial call November 2, 2026, 9:00 a.m.", cen), Spacer(1, 30),
         P(f"Submitted by {NAME}, Defendant in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 30),
         P("Tab A opens with the Master Trial Brief (lead document) with the line-by-line index of record irregularities; then the Notice of Government Claims, Verified Statement of Disqualification and Notice of Federal Rights; then Emergency Motion in Limine No. 1 (disqualification of plaintiff's counsel); then the "
           "Streamlined Statement of the Case (four independent statutory bars and a concise chronology). Tab H carries key pages only of the filed record (R01\u2013R10); "
           "Tab K carries only this Court's rule 1.100 orders and responses. Tab J is confidential in part under California Rules of Court, rule 1.100(c)(4). "
           "Every page is Bates-numbered; every assertion in Tab A is pinned to a Bates page or a Tab.", small),
         Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


if __name__ == "__main__":
    figs = I.render_figs()
    print("statement"); I.build_pdf(figs, I.OUT_PDF); I.build_docx(figs, I.OUT_DOCX)
    notice = N.build_notice(os.path.join(TMP, "notice_opening.pdf")); print("notice")
    mil = M.build_mil(os.path.join(TMP, "mil_1.pdf")); print("mil")
    svc_notice = NS.build(os.path.join(TMP, "notice_failure_to_serve.pdf")); print("service notice")
    opening = OP.build(os.path.join(TMP, "opening_statement.pdf")); print("opening")
    lodgment = NL.build(os.path.join(TMP, "notice_lodgment.pdf")); print("lodgment")
    telemetry = NT.build(os.path.join(TMP, "notice_telemetry.pdf")); print("telemetry")
    svclog = SL.build(os.path.join(TMP, "service_log.pdf")); print("service log")
    translog = TL.build(os.path.join(TMP, "translog.pdf")); print("translog")
    photo_counts = {l: len(items) for l, _, items in CATEGORIES}
    record_items = RR.record_items(); print("record refs")
    brief = B.build_brief(os.path.join(TMP, "trial_brief.pdf")); print("brief")
    tabA_items = [("Opening Statement; Application for Reasonable Accommodation and Emergency Judicial Access (Vesco) (Nov. 1, 2026)", opening),
                  ("Notice of Lodgment of Digital Case Repository (calindex.vercel.app) and IP Protections; Notice of Hard-Copy Service via Rapid Legal (Nov. 1, 2026)", lodgment),
                  ("Supplemental Notice of Active Monitoring, Digital Telemetry, and ESI Logs - External Access to calindex.vercel.app (Nov. 1, 2026)", telemetry),
                  ("Declaration re Electronic Service Log, Oct. 29 - Nov. 1, 2026 (transmissions to Dept. 606, ADA Coordinator, counsel)", svclog),
                  ("Notice of Plaintiff's Failure to Serve Statement of the Case and Pretrial Trial Materials; Objection (Nov. 1, 2026)", svc_notice),
                  ("Transmission Log - E-mail Service Record of Opening Papers and Notices, Oct. 29 - Nov. 1, 2026; Declaration of Service", translog),
                  ("Master Integrated Statement of the Case and Trial Brief; Index of Record Irregularities; Summary of Exhibits (LEAD DOCUMENT)", brief),
                  ("Notice of Government Claims; Request for Judicial Notice; Verified Statement of Disqualification; Notice of Federal Rights; Points and Authorities", notice),
                  ("Emergency Motion in Limine No. 1 \u2013 Disqualify Zanghi Torres Adams LLP; Exclude VA-Derived Evidence; Rule 1.100 Accommodation; Declaration; [Proposed] Order", mil),
                  ("Streamlined Statement of the Case \u2013 Four Independent Statutory Bars and Concise Chronology", T.streamlined_statement(os.path.join(TMP, "streamlined_statement.pdf")))]
    tabB = A.irregularities(os.path.join(TMP, "two_B.pdf")); tabC = A.witness_list(os.path.join(TMP, "two_C.pdf"))
    tabD = A.evidence_list(os.path.join(TMP, "two_D.pdf"), photo_counts); tabE = A.video_list(os.path.join(TMP, "two_E.pdf"))
    tabF = A.points_authorities(os.path.join(TMP, "two_F.pdf")); tabG = A.closing(os.path.join(TMP, "two_G.pdf"))
    med_ex = medical_exhibit(os.path.join(TMP, "two_medical_exhibit.pdf"))
    # Drop byte-identical court responses (the court issued several twice); renumber so the exhibit run stays continuous.
    ada_items, seen_hashes = [], set()
    for fn, lab in ADA_EXHIBITS:
        path = os.path.join(HERE, "ada", fn); h = hashlib.md5(open(path, "rb").read()).hexdigest()
        if h in seen_hashes: print("dedupe ADA:", lab); continue
        seen_hashes.add(h)
        trimmed = T.trim_ada(path, os.path.join(TMP, f"two_ada_{len(ada_items)+1:02d}.pdf"))
        snipped = snip.snippet_pdf(trimmed, os.path.join(TMP, f"two_ada_{len(ada_items)+1:02d}_snip.pdf"), f"Tab K, Ex. {len(ada_items)+1} - {lab}", f"Ex. {len(ada_items)+1}")
        ada_items.append((f"Ex. {len(ada_items)+1}. {lab} \u2013 operative language only (highlighted excerpts)", snipped))
    filing_items = [(f"{code} \u2013 {dt} \u2013 {desc}", os.path.join(FIL, fn)) for code, dt, desc, fn in FILINGS]

    # ---------------- San Francisco
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} \u2014 {DEPT}",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further proceedings in this case.", "Defendant", "Unlawful detainer",
                       "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    mc_sf_merged = A.merge(mc_sf, os.path.join(TMP, "two_mc_sf.pdf"))
    sub_items = [(f"Civil Subpoena (Duces Tecum) \u2013 {w['name']}",
                  T.trim_subpoena(A.merge(make_subpoena(w), os.path.join(TMP, f"two_subp_{w['tag']}.pdf")), os.path.join(TMP, f"two_subp_{w['tag']}_trim.pdf")))
                 for w in WITNESSES]
    svc_rows = [["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY", h1), grid(svc_rows, [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "two_svc.pdf"))
    sections_sf = [
        ("A", "Opening Papers: Opening Statement, Notices, Motion in Limine No. 1, and Statements of the Case", tabA_items),
        ("B", "Index of Record Irregularities and Indicia of Fraud", [("Line-by-line index", tabB)]),
        ("C", "Witness List", [("Witness list and offer of proof", tabC)]),
        ("D", "Evidence List", [("Exhibit and evidence list", tabD)]),
        ("E", "Video List", [("Audio-visual exhibit list", tabE)]),
        ("F", "Points and Authorities", [("Memorandum with table of authorities", tabF)]),
        ("G", "Closing Argument", [("Closing argument outline", tabG)]),
        ("H", "Record References \u2013 Chronology of the Filed Court Record (R01\u2013R10), Key Pages Only", record_items),
        ("I", "Notice to Counsel and Civil Subpoenas",
         [("Notice to Francisco Torres, Esq., October 31, 2026", os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")), ("Service directory", svc)] + sub_items),
        ("J", "Request for Accommodations \u2013 MC-410 \u2013 CONFIDENTIAL IN PART",
         [("MC-410 with Attachment", mc_sf_merged), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
        ("K", "Rule 1.100 Orders and Responses of this Court", ada_items),
        ("L", "Evidence Exhibit Binder \u2013 Photographs, Notices, Agency Records, Video Links, VA Medical Excerpts", [("Gillson Evidence Exhibit Binder", os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
    ]
    A.PREFIX = "SF"
    if not os.environ.get("SKIP_SF"):
      n = A.assemble(OUT_SF, cover_sf(os.path.join(TMP, "two_cover_sf.pdf")), sections_sf, "Gillson \u2013 FINAL All-in-One Trial Binder \u2013 San Francisco \u2013 CUD-26-682107 \u2013 Tab J confidential in part (CRC 1.100(c)(4))")
      print("SF pages", n); compress_scans(OUT_SF)

    # ---------------- Solano
    mc_sol = make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)",
                        "Superior Court of California, County of Solano \u2013 Civil Harassment (Code Civ. Proc., \u00a7 527.6)",
                        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026. I ask to appear by Zoom at every hearing in this matter until those orders are lifted. The emergency department record is attached as a confidential exhibit."],
                        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings.")
    mcsp = A.merge(mc_sol, os.path.join(TMP, "two_mc_sol.pdf"))
    sections_sol = [
        ("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order",
         [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
        ("B", "Request for Accommodations \u2013 MC-410 (Solano County) \u2013 CONFIDENTIAL IN PART",
         [("MC-410 with Attachment", mcsp), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
        ("C", "Course of Conduct \u2013 Opening Notice and Integrated Statement of the Case (San Francisco, CUD-26-682107)", [tabA_items[5], tabA_items[6], tabA_items[8]]),
        ("D", "Index of Record Irregularities (San Francisco record)", [("Line-by-line index", tabB)]),
        ("E", "Video Evidence \u2013 Audio-Visual Exhibits, Foundation, Publication Plan", [("Audio-visual exhibit list", tabE)]),
        ("F", "Points and Authorities \u2013 Table of Authorities with Case Summaries", [("Memorandum", tabF)]),
        ("G", "Record References \u2013 Chronology of the San Francisco Court Record (R01\u2013R10), Key Pages Only", record_items),
        ("H", "San Francisco Superior Court Rule 1.100 Orders and Responses (July\u2013October 2026)", ada_items),
        ("I", "Evidence Exhibit Binder \u2013 Photographs, Notices, Agency Records, Video Links, VA Medical Excerpts", [("Gillson Evidence Exhibit Binder", os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
    ]
    A.PREFIX = "SOL"
    n = A.assemble(OUT_SOL, cover_sol(os.path.join(TMP, "two_cover_sol.pdf")), sections_sol, "Gillson \u2013 FINAL All-in-One Binder \u2013 Solano County \u2013 Confidential in part (CRC 1.100(c)(4))")
    print("Solano pages", n); compress_scans(OUT_SOL)

    # exactly two downloads
    for p in glob.glob(os.path.join(ART, "*")):
        if os.path.abspath(p) not in (os.path.abspath(OUT_SF), os.path.abspath(OUT_SOL)):
            os.remove(p)
    # copies for the website
    os.makedirs(WEB, exist_ok=True)
    import shutil
    # Versioned file names so browsers / the CDN never serve a stale cached binder at the old URL.
    shutil.copy(OUT_SF, os.path.join(WEB, "san-francisco-final-355pp.pdf")); shutil.copy(OUT_SOL, os.path.join(WEB, "solano-final-306pp.pdf"))
    shutil.copy(notice, os.path.join(WEB, "notice.pdf")); shutil.copy(mil, os.path.join(WEB, "motion-in-limine-1.pdf"))
    print("done")
