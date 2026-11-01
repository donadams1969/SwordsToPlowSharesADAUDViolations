"""All-in-one trial binder for Swords to Plowshares v. Gillson, CUD-26-682107.

Layout rules (per client instruction): 12-pt Times body, true double spacing (24-pt leading),
uniform 1-inch margins, every table cell wrapped in a Paragraph so nothing bleeds or overlaps,
break-anywhere wrapping for URLs, and no fixed-width spacing hacks.
The Solano MC-410 binder is intentionally NOT included; it stays a separate binder.
"""
import os, io, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors

import build_binders as bb
from build_binders import (NAME, ADDR1, ADDR2, PHONE, EMAIL, WITNESSES, ADA_EXHIBITS,
                           make_mc410, make_subpoena, medical_exhibit, compress_scans)
from build import CATEGORIES
from notices import NOTICES

HERE = os.path.dirname(os.path.abspath(__file__))
ART = "/vercel/share/artifacts"
COMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components")
TMP = os.path.join(HERE, "tmp"); os.makedirs(TMP, exist_ok=True)
FIL = os.path.join(HERE, "filings")
OUT = os.path.join(ART, "Gillson_All_In_One_Trial_Binder_CUD-26-682107.pdf")
PREFIX = "AIO"
FRONT = []  # (bookmark label, pdf path) pages placed between the cover and the exhibit index

CASE = "Swords to Plowshares v. Donald Ernest Gillson, Ed.D."
CASE_NO = "CUD-26-682107"
COURT = "Superior Court of California, County of San Francisco"
DEPT = "Department 606 (Hon. Stephen M. Murphy)"
TRIAL = "Trial call November 2, 2026, 9:00 a.m."
DATED = "November 1, 2026"

# ------------------------------------------------------------------ styles: double-spaced, 1" margins
MARGIN = inch
TEXT_W = letter[0] - 2 * MARGIN  # 6.5 inches

body = ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=24, alignment=TA_LEFT, spaceAfter=0, splitLongWords=True, firstLineIndent=36)
quote = ParagraphStyle("quote", parent=body, leftIndent=36, rightIndent=36, fontSize=11.5, leading=23, firstLineIndent=0)
h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=16, leading=24, alignment=TA_CENTER, spaceAfter=12)
h2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=13, leading=24, spaceBefore=12, spaceAfter=0, keepWithNext=True)
h3 = ParagraphStyle("h3", fontName="Times-BoldItalic", fontSize=12, leading=24, spaceBefore=6, keepWithNext=True)
cen = ParagraphStyle("cen", parent=body, alignment=TA_CENTER, firstLineIndent=0)
num = ParagraphStyle("num", parent=body, leftIndent=36, firstLineIndent=-24)
cell = ParagraphStyle("cell", fontName="Times-Roman", fontSize=10, leading=14, splitLongWords=True)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Times-Bold")
cellurl = ParagraphStyle("cellurl", parent=cell, fontSize=8.5, leading=12, wordWrap="CJK")
small = ParagraphStyle("small", parent=body, fontSize=10, leading=15, firstLineIndent=0)
tabttl = ParagraphStyle("tabttl", fontName="Times-Bold", fontSize=18, leading=26, alignment=TA_CENTER)


def P(t, s=body):
    return Paragraph(t, s)


def rl(flow, path, title=""):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN + 0.15 * inch, title=title, author=NAME)
    doc.build(flow)
    return path


def caption(title):
    """Pleading-style caption used at the top of every drafted section."""
    left = [P(f"{NAME}", small), P(f"{ADDR1}", small), P(f"{ADDR2}", small), P(f"{PHONE} | {EMAIL}", small), P("Defendant, in propria persona", small)]
    t = Table([[left, ""]], colWidths=[3.6 * inch, 2.9 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    cap = Table([
        [P("SWORDS TO PLOWSHARES,", cell), P(f"Case No. {CASE_NO}", cellb)],
        [P("Plaintiff,", cell), P(DEPT, cell)],
        [P("v.", cell), P(TRIAL, cell)],
        [P("DONALD ERNEST GILLSON, Ed.D. (Dr. Donny Gillson), and all unnamed occupants,", cell), P(title, cellb)],
        [P("Defendant.", cell), ""],
    ], colWidths=[3.4 * inch, 3.1 * inch])
    cap.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, -1), (0, -1), 0.75, colors.black),
        ("LINEAFTER", (0, 0), (0, -1), 0.75, colors.black), ("LEFTPADDING", (1, 0), (1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [t, Spacer(1, 10), P(COURT.upper(), cen), Spacer(1, 8), cap, Spacer(1, 18)]


def grid(rows, widths, header=True):
    """Every cell is a Paragraph so long text wraps inside the column; widths sum to TEXT_W."""
    assert abs(sum(widths) - TEXT_W) < 0.01, sum(widths)
    data = [[c if not isinstance(c, str) else P(c, cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")))
    t.setStyle(TableStyle(st))
    return t


ORCID = "0009-0007-0768-5486"
SIGN_TIME = "November 1, 2026"
ESIGN_NOTE = ("Electronically signed by the declarant through his ADA cognitive assistive digital-communications application "
              "(the accommodated written channel of record), which records the signer's identity, date and time. "
              "A conformed /s/ signature is used pursuant to Cal. Rules of Court, rule 2.257(b); the signer's ORCID iD is a "
              "persistent, publicly verifiable identifier of the signer.")


def esign_lines():
    """Full electronic signature block used on every paper in both binders."""
    legal = NAME if "Donald" in NAME else f"{NAME} (Donald Ernest Gillson)"
    return (f"<b>/s/ Dr. Donny Gillson, Ed.D.</b><br/>"
            f"{legal}<br/>"
            f"Defendant, in propria persona<br/>"
            f"ORCID iD: <font face='Courier'>https://orcid.org/{ORCID}</font><br/>"
            f"dgillson9175@gmail.com | donny@18fu.ai<br/>"
            f"1030 Girard Road, Unit 301A, San Francisco, CA 94129<br/>"
            f"E-signed: {SIGN_TIME}, San Francisco, California")


def signature():
    return [Spacer(1, 18), P(f"Dated: {DATED}"),
            Table([[P("", cell), P(esign_lines(), cell)]],
                  colWidths=[3.25 * inch, 3.25 * inch], style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")])),
            Spacer(1, 6), P(ESIGN_NOTE, ParagraphStyle("esn", parent=cell, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#444444")))]


# One color per tab, used on the master index, tab pages, exhibit sheets and the fore-edge index block
# printed on every page (so the colored tabs are visible on the edge of the printed binder).
TAB_COLORS = {
    "A": "#1F4E79", "B": "#C00000", "C": "#2E7D32", "D": "#B8860B", "E": "#6A1B9A", "F": "#00838F", "G": "#E65100",
    "H": "#37474F", "I": "#AD1457", "J": "#4E342E", "K": "#283593", "L": "#558B2F", "M": "#8E24AA", "N": "#00695C",
}


def tab_rgb(letter_):
    c = colors.HexColor(TAB_COLORS.get(letter_, "#444444"))
    return (c.red, c.green, c.blue)


def _banner(text, letter_, style, pad=14):
    col = colors.HexColor(TAB_COLORS.get(letter_, "#444444"))
    st = ParagraphStyle("bn", parent=style, textColor=colors.white)
    t = Table([[P(text, st)]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), col), ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def tab_page(path, letter_, title, sub=""):
    flow = [Spacer(1, 2.6 * inch), _banner(f"TAB {letter_}", letter_, bb.tab, 18), Spacer(1, 14), P(title, tabttl)]
    if sub:
        flow += [Spacer(1, 10), P(sub, ParagraphStyle("ts", parent=cen, fontSize=13, leading=20))]
    return rl(flow, path)


# ------------------------------------------------------------------ record: the ten filed documents
FILINGS = [
    ("R01", "May 5, 2026", "Summons (SUM-130) and Complaint for Unlawful Detainer (UD-100) with attachments, verification page, lease exhibits, and notice to quit", "R01_2026-05-05_Summons_SUM-130_and_Complaint_UD-100_with_Attachments.pdf"),
    ("R02", "May 19, 2026", "Plaintiff's Ex Parte Application for Order for Service by Posting (Code Civ. Proc., § 415.45) with Falanga and Martinez declarations", "R02_2026-05-19_Plaintiff_ExParte_Application_Order_Service_by_Posting_415.45.pdf"),
    ("R03", "June 30, 2026", "Request for Entry of Default (CIV-100), stamped DEFAULT ENTERED AS REQUESTED", "R03_2026-06-30_Request_for_Entry_of_Default_Entered.pdf"),
    ("R04", "June 30, 2026", "Judgment – Unlawful Detainer (UD-110), clerk's judgment by default, possession only, $0.00", "R04_2026-06-30_Default_Judgment_Entered.pdf"),
    ("R05", "June 30, 2026", "Proof of Service of Summons (POS-010) by posting and mailing, Falanga, party served: All Unnamed Occupants", "R05_2026-06-30_POS-010_Falanga_Posting_415.45.pdf"),
    ("R06", "July 1, 2026", "Plaintiff filing B – Notice of Entry of Judgment and related papers", "R06_2026-07-01_Plaintiff_Filing_B.pdf"),
    ("R07", "July 1, 2026", "Plaintiff filing A – Writ of Possession request (MC-030) and related papers", "R07_2026-07-01_Plaintiff_Filing_A.pdf"),
    ("R08", "July 7, 2026", "Defendant's Emergency Ex Parte Application", "R08_2026-07-07_Defendant_Emergency_ExParte_Application.pdf"),
    ("R09", "July 7, 2026", "Defendant's Ex Parte Packet – Points and Authorities, Answer dated May 17, 2026, and exhibits", "R09_2026-07-07_Defendant_ExParte_Packet_PA_Answer_Exhibits.pdf"),
    ("R10", "July 8, 2026", "Order re Ex Parte Application, and Points and Authorities signed by John Zanghi, Zanghi Torres Adams LLP, as \"Attorneys for Defendant\"", "R10_2026-07-08_Order_re_ExParte_and_ZTA_PA_signed_Attorneys_for_Defendant.pdf"),
]


# ------------------------------------------------------------------ TAB A: Statement of the Case
def statement_of_case(path):
    f = caption("DEFENDANT'S STATEMENT OF THE CASE")
    f.append(P("I. Nature of the Action", h2))
    f.append(P(
        "This is an unlawful detainer action brought by Swords to Plowshares, the operator of the Veterans Academy supportive-housing "
        "program at 1030 Girard Road in the Presidio of San Francisco, against Dr. Donald Ernest Gillson, Ed.D., a 90-percent service-connected "
        "disabled veteran who holds Unit 301A under a federally assisted tenancy. Plaintiff is represented by Zanghi Torres Adams LLP. "
        "The complaint was signed by John Zanghi. Francisco Torres has since appeared for plaintiff."))
    f.append(P(
        "Defendant contends that the action rests on a notice that is defective on its face, a complaint whose verification page names the "
        "defendant rather than the plaintiff, a declaration of diligence that was signed before the event it describes, a proof of service that "
        "names the wrong party, and a default that was requested and entered while an Answer bearing a May 17, 2026 date existed. Defendant further "
        "contends that the action was filed in retaliation for protected habitability complaints and disability-accommodation requests made between "
        "November 2025 and April 2026, and that plaintiff's counsel has since filed a paper in this very case identifying itself as "
        "\"Attorneys for Defendant.\" Each contention below is tied to a page in the record reproduced at Tab H."))

    f.append(P("II. The Tenancy and the Protected Activity That Preceded the Notice", h2))
    for t in [
        "Dr. Gillson occupies Unit 301A under a HUD-assisted supportive-housing lease. Plaintiff's own complaint attachment admits that the "
        "HUD-50059 and the Accessible Unit Lease Addendum \"cannot be located\" and that the lease exhibit bears a \"typographic error\" in its dates (Tab H, R01).",
        "Beginning November 16, 2025, Dr. Gillson submitted written grievances and maintenance requests describing a cockroach-infested refrigerator "
        "placed in his unit and an infestation that spread to his living space (Tab L, Category A). Photographs taken November 16, 2025 through "
        "January 5, 2026 document live cockroaches, loaded glue traps, droppings, and continued activity after the December 17, 2025 Pestec treatment (Tab L, Category B).",
        "On November 19, 2025, Dr. Gillson opened San Francisco 311 Case No. 101003004371, which was transferred to the Department of Public Health, "
        "Environmental Health Branch, Healthy Housing Program (Tab L, Category F). Adult Protective Services wrote to him on December 5, 2025 (same).",
        "Dr. Gillson's service dog, Jaxx, sustained bite lesions requiring veterinary treatment on December 11, 2025 (Tab L, Category C). Dr. Gillson "
        "himself was seen at UCSF Urgent Care on November 22, 2025 and in an emergency department on December 9, 2025 with concussion and cervical-sprain "
        "discharge instructions (Tab L, Category D).",
        "On November 24, 2025, Assistant Property Manager William Landrum wrote confirming continued pest treatment and monthly follow-up (Tab L, Category E). "
        "On January 2, 2026, plaintiff's property-management team sent a building-wide letter warning that \"formal notices may be issued\" for rent issues (same).",
        "On January 2, 2026, Dr. Gillson filed complaints with the California Board of Behavioral Sciences against two Swords to Plowshares clinicians, "
        "Nos. 2002026002097 and 2002026002098 (Tab L, Evidence Exhibit Binder, Category K).",
        "On December 25, 2025, Dr. Gillson's vehicle was broken into in plaintiff's parking lot; United States Park Police Case No. 251250105 was opened (Tab L, Category I).",
    ]:
        f.append(P(t))

    f.append(P("III. The Notice to Quit", h2))
    for t in [
        "The notice on which the complaint rests was, according to plaintiff's own proof of service, served April 8, 2026 and expired April 16, 2026 (Tab H, R01). "
        "The proof of service checks two mutually exclusive boxes: that a copy was given to a person residing at the premises, and that no person of suitable age "
        "or discretion could be found there. Both cannot be true.",
        "The eight-day span between service and expiration does not match a three-day notice under Code of Civil Procedure section 1161, and the complaint does not "
        "identify the notice as a HUD ten-day or thirty-day notice. The complaint's item 7 is itself marked in a way that states no proper notice was served.",
        "The notice does not state, with the specificity that 24 Code of Federal Regulations part 247.4 requires, the grounds for termination, nor does it advise the "
        "tenant of the ten-day right to meet with management to discuss the proposed termination. No proof of the dual service (first-class mail and hand delivery "
        "or posting) that part 247.4(b) requires appears in the record.",
        "Defendant's position, supported by on-site staff statements preserved on video (Tab E, second suite, V-03 and V-05), is that the notice and its proof of service "
        "name Jerome Bradford as the person who served it and William Landrum as the witness, that Mr. Bradford was not present at the stated date and time, and that "
        "a resident advisor has described legal papers at the building being delivered \"by accident.\"",
    ]:
        f.append(P(t))

    f.append(P("IV. The Complaint (May 5, 2026)", h2))
    for t in [
        "The UD-100 was filed May 5, 2026 by John Zanghi. Item 22 states \"See Attached Verification.\" The verification page that follows identifies the declarant as "
        "\"Donald Gillison\" – a misspelling of the defendant's name – rather than any officer or agent of plaintiff. A verification by the party being sued is no "
        "verification at all (Code Civ. Proc., § 1166, subd. (a)(1); § 446).",
        "The complaint carries over an attorney-and-date block referencing Andrew Wong and January 19, 2025 – a stale block from an unrelated 2025 matter – "
        "which indicates the pleading was assembled from a prior form rather than drafted for this tenancy.",
        "The complaint alleges rent of $1,500.00 per month, yet states fair rental value of $37.53 per day. One-thirtieth of $1,500 is $50.00. The two figures cannot both be correct.",
        "The complaint elects forfeiture of the lease. The default judgment entered June 30, 2026 (Tab H, R04) leaves the forfeiture box (item 6c) unchecked and awards $0.00.",
    ]:
        f.append(P(t))

    f.append(P("V. The Application for Service by Posting (May 19, 2026)", h2))
    for t in [
        "Plaintiff's application was supported by a declaration of diligence by process server Falanga and a declaration by Martinez of plaintiff's counsel's office (Tab H, R02).",
        "The Falanga declaration is dated May 11, 2026. It attests, under penalty of perjury, to a fourth attempt at service on May 12, 2026 at 6:06 p.m. – the day "
        "after the declaration was signed. A declarant cannot truthfully attest to an event that has not yet occurred. The copies of the declaration for Dr. Gillson and for "
        "\"All Unnamed Occupants\" recite identical attempt times.",
        "The Martinez declaration asserts that defendant never answered the door and that his place of employment was unknown. Plaintiff's own complaint attachment "
        "identifies plaintiff as the on-site property manager with staff present at the building. Plaintiff's counsel had Dr. Gillson's e-mail address and telephone "
        "number and had seen him in person at the March 19, 2026 restraining-order hearing. The declarations disclose no attempt to serve by mail, e-mail, telephone, "
        "or through the on-site staff who see the tenant daily. That is not the reasonable diligence section 415.45 requires.",
        "No signed order authorizing service by posting appears in the record provided to defendant. The record contains the application and its declarations only.",
    ]:
        f.append(P(t))

    f.append(P("VI. Posting, Mailing, Default, and Judgment (June 4 – July 1, 2026)", h2))
    for t in [
        "Plaintiff's photograph shows the summons posted on June 4, 2026 beside a Notice of Entry dated June 1, 2026 – demonstrating that the door was accessible and that "
        "management was in routine contact with the unit (Tab H, R05).",
        "Under section 415.45, subdivision (c), service by posting is complete on the tenth day after posting and mailing: June 14, 2026. The tenant then had ten court days "
        "to respond (Code Civ. Proc., § 1167, as amended effective January 1, 2025). Counting court days and excluding the June 19, 2026 Juneteenth holiday, the response "
        "period ran through approximately June 29, 2026. Plaintiff requested default on June 30, 2026 – the first possible day – and the clerk entered it the same day.",
        "The only POS-010 in the record (Tab H, R05) names \"All Unnamed Occupants\" as the party served. No proof of service of summons naming Donald Gillson appears. "
        "A clerk's default judgment for possession under section 1169 requires a valid proof of service on the defendant against whom judgment is entered.",
        "An Answer bearing the date May 17, 2026 appears in the record (Tab H, R09). Whether the clerk accepted it for filing on that date must be confirmed from the register "
        "of actions. If it was on file, the default entered June 30, 2026 was void on its face. If it was rejected, the rejection and its reason must be disclosed.",
        "On July 1, 2026, plaintiff served a Notice of Entry of Judgment reciting a 90-day period to seek relief and requested a writ of possession (Tab H, R06, R07). "
        "Relief from a default judgment under section 473, subdivision (b), may be sought within six months, and a void judgment may be set aside at any time under subdivision (d).",
    ]:
        f.append(P(t))

    f.append(P("VII. Defendant's Emergency Application and the July 8, 2026 Order", h2))
    for t in [
        "On July 7, 2026, Dr. Gillson filed an emergency ex parte application with points and authorities, the May 17, 2026 Answer, and exhibits (Tab H, R08, R09).",
        "The Court's July 8, 2026 order is accompanied in the file by a points-and-authorities document signed by John Zanghi of Zanghi Torres Adams LLP as "
        "\"Attorneys for Defendant,\" requesting relief for the defendant (Tab H, R10). Zanghi Torres Adams LLP is plaintiff's counsel. Either the firm filed a paper "
        "on behalf of the adverse party – a conflict under rule 1.7 of the Rules of Professional Conduct and a misrepresentation to the Court under rule 3.3 – or the "
        "firm's filing was mislabeled in a way that misstates who is asking the Court for what. Either way, the paper cannot be relied upon as a plaintiff's filing.",
        "The default has since been addressed, the matter has been assigned to Department 606, and trial call is set for November 2, 2026. Between July 20 and "
        "October 14, 2026, the Court issued twenty written responses and orders on Dr. Gillson's rule 1.100 accommodation requests (Tab K).",
    ]:
        f.append(P(t))

    f.append(P("VIII. Relief Defendant Will Request", h2))
    for i, t in enumerate([
        "Judgment for defendant, or dismissal, because the notice is defective on its face and a defective notice cannot be cured by amendment.",
        "Alternatively, an order striking the complaint as unverified under sections 446 and 1166 until plaintiff files a verification by a competent agent.",
        "A finding that the June 30, 2026 default and judgment were void for want of valid service and, if the Answer was on file, for entry in the face of a responsive pleading.",
        "An order requiring plaintiff's counsel to explain, under oath, the May 11, 2026 declaration describing a May 12, 2026 event, and the July 8, 2026 paper signed as \"Attorneys for Defendant.\"",
        "Sanctions under Code of Civil Procedure sections 128.5 and 128.7, and referral of the service declarations to the District Attorney under Penal Code section 118, as the Court deems appropriate.",
        "Attorney fees and costs to the prevailing party as the lease and Civil Code section 1717 provide, and such further relief as is just.",
    ], 1):
        f.append(P(f"{i}.&nbsp;&nbsp;{t}", num))
    f += signature()
    return rl(f, path, "Statement of the Case")


# ------------------------------------------------------------------ TAB B: Record irregularities, line by line
IRREG = [
    ("1", "R01 – Notice to quit, proof of service", "Both \"copy given to person residing at premises\" and \"no person of suitable age or discretion found\" are checked.", "Internally contradictory; one of the two statements is false. Code Civ. Proc., § 1162; Pen. Code, § 118."),
    ("2", "R01 – Notice dates", "Served April 8, 2026; expired April 16, 2026 (eight days).", "Does not match a three-day notice (§ 1161) and is not identified as a HUD notice under 24 C.F.R. § 247.4."),
    ("3", "R01 – Notice content", "No specific statement of grounds; no advice of the ten-day right to discuss; no proof of dual service.", "24 C.F.R. § 247.4(a)–(b); Gersten Companies v. Deloney (1989) 212 Cal.App.3d 1119 (HUD notice rules are a condition precedent)."),
    ("4", "R01 – UD-100 item 7", "Marked so as to state that no proper notice was served.", "Judicial admission inconsistent with the cause of action."),
    ("5", "R01 – Verification page", "Declarant named as \"Donald Gillison\" – the defendant, misspelled – not an officer or agent of plaintiff.", "Code Civ. Proc., §§ 446, 1166(a)(1). An unverified UD complaint is subject to a motion to strike."),
    ("6", "R01 – Attorney/date block", "References Andrew Wong and January 19, 2025 – a stale block from an unrelated matter.", "Indicates recycled pleading; relevant to candor and to the reliability of the verification."),
    ("7", "R01 – Rent figures", "Rent $1,500 per month; fair rental value $37.53 per day ($50.00 would be correct).", "Internal inconsistency in a verified pleading."),
    ("8", "R01 – Lease exhibits", "Lease dates admitted to contain a \"typographic error\"; HUD-50059 and Accessible Unit Lease Addendum \"cannot be located.\"", "Plaintiff cannot prove the terms it seeks to enforce; HUD lease documents are required for a HUD-assisted unit."),
    ("9", "R02 – Falanga declaration of diligence", "Signed May 11, 2026; attests to a fourth attempt on May 12, 2026 at 6:06 p.m.", "Impossible chronology; false declaration under penalty of perjury. Pen. Code, § 118; Code Civ. Proc., § 2015.5."),
    ("10", "R02 – Falanga declarations (two copies)", "Copies for Gillson and for All Unnamed Occupants recite identical attempt times.", "Template reuse rather than a record of actual attempts."),
    ("11", "R02 – Martinez declaration", "States defendant never answered and employment unknown; no mail, e-mail, phone, or on-site-staff attempt disclosed despite counsel's known contact with defendant.", "Fails reasonable diligence. Code Civ. Proc., § 415.45(a); Evartt v. Superior Court (1979) 89 Cal.App.3d 795."),
    ("12", "R02 – Order", "No signed order authorizing posting appears in the record.", "Posting without an order is not service. § 415.45(a)."),
    ("13", "R05 – Posting photograph", "Summons posted June 4, 2026 next to a Notice of Entry dated June 1, 2026.", "Door accessible; management in routine contact; undercuts claimed inability to serve."),
    ("14", "R05 – POS-010 party served", "Names \"All Unnamed Occupants\" only. No POS naming Donald Gillson in the record.", "No valid proof of service on the named defendant. §§ 417.10, 1169."),
    ("15", "R03 – Timing of default", "Service complete June 14, 2026; ten court days (Juneteenth excluded) ran to about June 29; default requested and entered June 30.", "Requested on the earliest arguable day; any miscount renders the default premature and void. § 1167; § 473(d)."),
    ("16", "R03 / R09 – Answer dated May 17, 2026", "An Answer bearing a May 17, 2026 date exists in the record; default nonetheless entered June 30.", "If on file, default void on its face. If rejected, plaintiff must disclose the rejection. § 585; § 1169."),
    ("17", "R04 – UD-110", "Clerk's judgment, possession only, $0.00; forfeiture box 6c unchecked though complaint elects forfeiture.", "Judgment does not conform to the pleading; § 1174."),
    ("18", "R06 – Notice of Entry of Judgment", "Recites a 90-day period for relief.", "Misstates the six-month period under § 473(b) and the no-time-limit rule for void judgments under § 473(d)."),
    ("19", "R07 – Writ request (MC-030)", "Requested the day after judgment on a $0.00 possession-only judgment resting on the defects above.", "Enforcement sought on a void judgment."),
    ("20", "R10 – Points and authorities, July 8, 2026", "Signed by John Zanghi, Zanghi Torres Adams LLP, \"Attorneys for Defendant,\" requesting relief for defendant.", "Rules Prof. Conduct, rules 1.7, 3.3; Bus. & Prof. Code, § 6068(d). A plaintiff's firm cannot appear for the defendant."),
    ("21", "Pattern – Retaliation chronology", "Notice issued April 8, 2026, after habitability complaints (Nov. 2025), 311/DPH referral (Nov. 19, 2025), APS contact (Dec. 5, 2025), BBS complaints (Jan. 2, 2026), and accommodation requests.", "Civ. Code, § 1942.5(a), (d); Barela v. Superior Court (1981) 30 Cal.3d 244. Retaliation is a complete defense."),
    ("22", "Pattern – Service by on-site staff", "On-site resident advisor describes legal papers delivered \"by accident\" (Tab E, second suite, V-05) and management instructions and selective enforcement (V-03).", "Contradicts a proof of service reciting personal delivery at a stated time by Mr. Bradford."),
]


def irregularities(path):
    f = caption("INDEX OF RECORD IRREGULARITIES AND INDICIA OF FRAUD (LINE-BY-LINE)")
    f.append(P(
        "Each entry below identifies the document (by Tab H record number), quotes or describes the specific line or box at issue, "
        "and states the rule it offends. Defendant asks that the Court take judicial notice of each cited court record under Evidence "
        "Code sections 452, subdivision (d), and 453."))
    f.append(Spacer(1, 10))
    rows = [["No.", "Document / Line", "What the record shows", "Why it matters / authority"]] + [list(r) for r in IRREG]
    f.append(grid(rows, [0.45 * inch, 1.55 * inch, 2.35 * inch, 2.15 * inch]))
    f.append(Spacer(1, 12))
    f.append(P("Reservation", h2))
    f.append(P(
        "Several of the filed documents in Tab H are image scans. Defendant has read each page and describes the record in good faith. "
        "Where a quoted figure or date is taken from a scanned image, the Court is asked to rely on the filed original in the register of actions, "
        "which defendant requests be lodged by plaintiff for trial."))
    f += signature()
    return rl(f, path, "Record Irregularities")


# ------------------------------------------------------------------ TAB C: Witness list
WITNESS_ROWS = [
    ("1", "Dr. Donald Ernest Gillson, Ed.D.", "Defendant; tenant of Unit 301A", "Tenancy history; condition of the unit; each grievance, 311 report, and accommodation request; absence of any personal service; medical effects; the courthouse and property confrontations shown in Exhibits V-01 to V-07."),
    ("2", "William Landrum", "Assistant Property Manager, Swords to Plowshares (subpoenaed, Tab I)", "Witness or declarant on the notice's proof of service; author of the November 24, 2025 pest letter; the person with whom the underlying dispute occurred; what staff complaints existed before the notice issued; who decided to serve and when."),
    ("3", "Jerome Bradford", "Property / operations staff, Swords to Plowshares (subpoenaed, Tab I)", "Identified as the person who executed and/or served the notice. Whether he was at the premises on the date and time stated; who told him to serve; what he actually did with the papers."),
    ("4", "\"Dwayne\" (surname to be confirmed)", "Resident advisor, 1030 Girard Road", "On video describes legal papers being delivered by accident and management's service practices (second suite V-05) and management instructions and selective enforcement (V-03). Direct contradiction of the proof of service."),
    ("5", "Process server Falanga", "Registered process server retained by plaintiff's counsel", "The May 11, 2026 declaration attesting to a May 12, 2026 attempt; the identical attempt times on both declarations; the June 4, 2026 posting; whether anyone instructed the contents of the declarations."),
    ("6", "Martinez (declarant)", "Staff, Zanghi Torres Adams LLP", "The May 19, 2026 diligence declaration; what contact information counsel had for defendant; why no mail, e-mail, telephone, or staff service was attempted; the July 1, 2026 Notice of Entry of Judgment."),
    ("7", "John P. Zanghi, Esq.", "Partner, Zanghi Torres Adams LLP; signed the complaint (subpoenaed, Tab I)", "Preparation of the UD-100; who signed the verification and why it names the defendant; the recycled January 2025 attorney block; the July 8, 2026 paper signed as \"Attorneys for Defendant\"; receipt of the Court's rule 1.100 orders."),
    ("8", "Francisco G. Torres, Esq.", "Partner, Zanghi Torres Adams LLP; present counsel for plaintiff (subpoenaed, Tab I)", "Handling of the file after Mr. Zanghi; knowledge of the service defects after receipt of defendant's October 31, 2026 notice (Tab I); the delivery of a box of documents to defendant in Department 505; handling of accommodation requests."),
    ("9", "Custodian of Records, Swords to Plowshares (attn: Michael Blecker, Executive Director)", "Plaintiff (subpoenaed, Tab I)", "Tenant ledger; HUD-50059 and lease addenda plaintiff says cannot be located; maintenance, pest-control, and contractor records; access-control and camera records for the claimed service date; staff communications about the notice."),
    ("10", "Tramecia Garner, LPCC", "Executive Director, Swords to Plowshares (November 2025)", "Receipt of the November 2025 grievances; the organization's knowledge of the infestation and of defendant's protected complaints before the notice issued."),
    ("11", "Kolby Losik and Mark Villalobos", "Clinicians, Swords to Plowshares; subjects of BBS complaints Nos. 2002026002097 and 2002026002098 (Tab L, Evidence Exhibit Binder, Category K)", "Knowledge within plaintiff's organization of the January 2, 2026 licensing complaints – protected activity preceding the April 8, 2026 notice. Statement attributed to \"Mark\": \"I saw some bugs, I didn't think it was Level 5\" (Tab L, Category G)."),
    ("12", "Custodian of Records, SF Department of Public Health, Environmental Health Branch", "Non-party agency (subpoenaed, Tab I)", "The 311 / Healthy Housing file for Case No. 101003004371 opened November 19, 2025; inspection and closure records for 1030 Girard Road."),
    ("13", "Custodian of Records, SF Superior Court ADA Coordinator (Joy Guandique)", "Court administrative office (subpoenaed, Tab I)", "Dates and dispositions of each rule 1.100 request and the transmittal of the Court's orders to plaintiff's counsel – fixing the dates of protected activity and counsel's notice of it."),
    ("14", "Adult Protective Services worker (author of the December 5, 2025 letter)", "City and County of San Francisco, DAS/APS", "Independent corroboration that a protective-services referral concerning defendant's housing conditions existed in December 2025."),
    ("15", "Officer Stromberg", "United States Park Police, San Francisco Field Office", "Case No. 251250105 – vehicle break-in in plaintiff's lot on December 25, 2025; conditions and security at the premises."),
    ("16", "Custodians of Records, UCSF Health; John Muir Health; VA Northern California", "Medical providers", "Authentication of the November 22, 2025 urgent-care visit, the December 9, 2025 emergency visit, and the October 30, 2026 emergency visit and work-status note (Tab J, confidential)."),
]


def witness_list(path):
    f = caption("DEFENDANT'S WITNESS LIST AND OFFER OF PROOF")
    f.append(P(
        "Defendant identifies the following witnesses and, for each, the reason the witness is called. Witnesses 2, 3, 7, 8, 9, 12, and 13 have "
        "been served, or will be served, with civil subpoenas duces tecum (Tab I). Defendant reserves the right to call any witness identified by "
        "plaintiff and to call rebuttal witnesses."))
    f.append(Spacer(1, 10))
    rows = [["No.", "Witness", "Capacity", "Why the witness is called"]] + [list(r) for r in WITNESS_ROWS]
    f.append(grid(rows, [0.45 * inch, 1.7 * inch, 1.65 * inch, 2.7 * inch]))
    f.append(Spacer(1, 12))
    f.append(P("Estimated time", h2))
    f.append(P("Defendant estimates two court days for his case, exclusive of plaintiff's case and cross-examination. Dr. Gillson will testify "
               "with the accommodations ordered under rule 1.100 (Tab K), including rest breaks and remote appearance if his medical orders remain in effect."))
    f.append(P("V. Notice of Demand for In Camera Review and Reasonable Accommodation Testimony", h2))
    f.append(P("Please take further notice that formal application is hereby made for an in camera review and live video-feed reasonable accommodation for "
               "all veteran residents of 1030 and 1029 Girard Road who are members and participants of the Veterans Tenant Union."))
    f.append(P("<b>1. Scope and justification.</b> <b>Witness protection and retaliation prevention:</b> due to documented institutional retaliation, eviction "
               "threats, and aggressive administrative blowback by Swords to Plowshares (StP) management and associated actors, live open-court testimony poses "
               "severe safety and housing-security risks to vulnerable veteran witnesses. <b>Reasonable accommodation:</b> to ensure uncoerced, full, and fair "
               "testimony regarding habitability violations, systemic neglect, and concerted retaliation, an in camera proceeding conducted via secure live video "
               "feed on-site (or through protected remote channels) is requested under California Rules of Court, rule 1.100, Code of Civil Procedure section 367.75, "
               "Evidence Code section 765, Government Code section 68086, Title II of the Americans with Disabilities Act (42 U.S.C. \u00a7 12132; 28 C.F.R. \u00a7 35.130(b)(7)), "
               "and the anti-retaliation provisions of the Fair Housing Act (42 U.S.C. \u00a7 3617) and Civil Code section 1942.5. <b>Integration into proceedings:</b> "
               "this request encompasses all resident witnesses from 1030 and 1029 Girard Road participating in the Veterans Tenant Union, so that their sworn "
               "statements, evidentiary contributions, and accounts of institutional misconduct are preserved and integrated into the judicial record and the "
               "pending federal reviews."))
    f.append(P("VI. Formal Incorporation of Video Testimony, Signed Declarations, and Registrative Actions as Witness Testimony", h2))
    f.append(P("Please take further notice that all current video testimonies, signed declarations contained within formal pleadings, and ongoing registrative "
               "actions submitted by veteran residents, tenant union participants, and associated parties are offered, and defendant asks that they be received, "
               "as witness testimony in this action and are tendered to the investigative proceedings in which they are also lodged."))
    f.append(P("<b>1. Evidentiary weight and admissibility.</b> <b>Integration of pleadings and registrative filings:</b> all verified declarations, sworn statements, "
               "and evidentiary submissions embedded within active court pleadings, administrative dockets, and official registrative actions are offered under Code of "
               "Civil Procedure sections 2009 and 2015.5 and Evidence Code sections 1400\u20131401, 1220 and 1280 for their full evidentiary weight. <b>Audio-visual and video "
               "testimony:</b> live or recorded video testimonies provided by veteran residents and tenant union members, particularly those conducted via secure remote "
               "feeds or protected in camera protocols, are offered as contemporaneous witness accounts documenting habitability violations, retaliation, and institutional "
               "misconduct (Tab E; Evidence Exhibit Binder, Category L). <b>Consolidated record:</b> these testimonies and declarations are incorporated as a continuous, "
               "unified body of evidence presently before federal investigators, regional VA offices, and oversight authorities, so that every witness account is "
               "preserved, examined, and weighed in connection with the ongoing federal reviews. Defendant acknowledges that the Court will rule on hearsay and "
               "foundation objections as each item is offered and asks that any exclusion be stated on the record with its grounds."))
    f.append(P("VII. Notice of Complex Litigation Status and Warrant for Assignment to Department 606", h2))
    f.append(P("Please take further notice that the trial and evidentiary record lodged in this matter, comprising the two trial binders, the Evidence Exhibit Binder, "
               "and the native filings they excerpt (court orders, medical records, federal investigative notices, sworn declarations, and electronically stored "
               "information logs), exceeds 700 pages of verified documentation and is empirical proof that this matter is not a standard, summary unlawful detainer proceeding."))
    f.append(P("<b>1. Justification for complex-litigation designation (Cal. Rules of Court, rule 3.400).</b> <b>Systemic scope and multiple parties:</b> the litigation "
               "encompasses widespread systemic violations, institutional neglect, fiduciary abuse, coordinated retaliatory eviction tactics affecting multiple veteran "
               "residents, and active federal investigations across regional VA nodes and oversight bodies (rule 3.400(b)(1), (3), (5)). <b>Complex legal frameworks:</b> the "
               "proceedings involve intersecting federal statutes, constitutional protections, the Presidio Trust Act, disability-rights law, the Elder Abuse and Dependent "
               "Adult Civil Protection Act (Welf. &amp; Inst. Code, \u00a7 15600 et seq.), and intricate evidentiary chains (rule 3.400(b)(1), (2)). <b>Warrant for Department 606 "
               "assignment:</b> the volume, technical complexity, and scope of the record warrant that this action be designated and administered as complex litigation "
               "under rules 3.400\u20133.403, with a single assigned judicial officer for all purposes, case-management orders, and judicial oversight in Department 606 "
               "consistent with the Presiding Judge's assignment authority under rule 10.603(c)(1)(C). Defendant acknowledges that complex designation ordinarily removes "
               "the summary unlawful detainer calendar preferences of Code of Civil Procedure section 1179a and requests exactly that."))
    f.append(P("VIII. Amended Notice of Addition to Indexed Witness Register: Cooley LLP, Its Responsible Executives and Counsel, and the Board of Directors of Swords to Plowshares", h2))
    f.append(P("Please take notice that defendant amends this witness list to add the following adverse witnesses, each to be called through the person most "
               "qualified under Code of Civil Procedure section 2025.230 and Evidence Code section 776, with trial subpoenas to issue under Code of Civil Procedure "
               "section 1987 on the same terms as the subpoenas at Tab I:"))
    f.append(P("<b>Cooley LLP; its responsible executives and attorneys of record for Swords to Plowshares.</b> <i>Designation:</i> adverse witness; institutional "
               "counsel and corporate-governance representatives. <i>Offer of proof:</i> institutional representation of Swords to Plowshares; corporate directives "
               "and management-compliance oversight; civil-rights and housing-practice policies; and participation in litigation coordination and procedural "
               "strategy bearing on the habitability, tenancy, and retaliatory displacement of defendant. Defendant acknowledges the attorney-client privilege "
               "(Evid. Code, \u00a7 954) and will confine examination to non-privileged facts, business policies, and communications made to third parties or in "
               "furtherance of the crime-fraud exception (Evid. Code, \u00a7 956), with the Court to rule on each objection as it is made. Estimated time: 0.5 hour."))
    f.append(P("<b>Board of Directors of Swords to Plowshares (chair, or the director(s) designated as most qualified).</b> <i>Designation:</i> adverse witness; "
               "governing board and fiduciary supervisory body. <i>Offer of proof:</i> corporate oversight; fiduciary duties owed to tenants and program participants; "
               "knowledge and ratification of management practices, including the acts of Bradley White, Kolby Losik, and William Landrum; failure to accommodate "
               "disability under state and federal law (Gov. Code, \u00a7 12927, subd. (c)(1); 42 U.S.C. \u00a7 3604(f)(3)(B)); and institutional accountability for "
               "constructive displacement and retaliation under Civil Code section 1942.5, including ratification for purposes of Civil Code section 3294, "
               "subdivision (b). Estimated time: 0.75 hour."))
    f.append(P("<b>Basis for the addition; information and belief regarding access to defendant's intellectual property.</b> Defendant states, <i>on information "
               "and belief only</i>, and based on the IP-address and device telemetry for the digital case repository (Supplemental Notice of Active Monitoring, "
               "Tab A; ESI logs, Tab L), that persons or systems associated with the Board of Directors of Swords to Plowshares and Cooley LLP may have accessed, "
               "copied, or retained on their servers defendant's proprietary case materials and intellectual property published at calindex.vercel.app, and may "
               "have done so in coordination with plaintiff's counsel Zanghi Torres Adams LLP (John Zanghi and Francisco G. Torres). Defendant does not allege "
               "this as an established fact. IP addresses and device signatures show only that a network location or device requested the repository; they do not "
               "by themselves identify the individual or organization responsible, and defendant has not yet matched any address to a named person. The "
               "telemetry is preserved in the native logs and will be produced on request. Defendant calls these witnesses to examine them on whether, and "
               "by whom, the materials were received, routed, or used, and on retaliation, litigation coordination, and the protective-order and copyright "
               "issues raised in the Notice of Lodgment (Tab A). Defendant asks the Court to order preservation of the recipients' server and e-mail access "
               "logs under Code of Civil Procedure section 2031.010 pending trial, so that the belief stated here can be confirmed or dispelled."))
    f.append(P("This addition is integrated into the digital case repository at https://calindex.vercel.app/ and is included in the hard-copy set being served "
               "through Rapid Legal under Code of Civil Procedure section 1011 et seq. and California Rules of Court, rule 2.251, as stated in the Notice of "
               "Lodgment at Tab A."))
    f += signature()
    return rl(f, path, "Witness List")


# ------------------------------------------------------------------ TAB D: Evidence list
def evidence_list(path, photo_counts):
    f = caption("DEFENDANT'S EXHIBIT AND EVIDENCE LIST")
    f.append(P("Part 1. Court records (Tab H). Judicial notice requested under Evidence Code sections 452(d) and 453.", h2))
    rows = [["No.", "Filed", "Document", "Purpose"]]
    purposes = {
        "R01": "Notice defects; defective verification; recycled form; inconsistent rent figures; missing HUD documents.",
        "R02": "Impossible chronology in the diligence declaration; absence of reasonable diligence; no order in record.",
        "R03": "Default requested on the earliest arguable day despite the May 17, 2026 Answer.",
        "R04": "Judgment does not conform to the pleading; $0.00; forfeiture unchecked.",
        "R05": "Proof of service names only All Unnamed Occupants; door was accessible on June 4, 2026.",
        "R06": "Misstatement of the period for relief from default.",
        "R07": "Enforcement sought on a void judgment.",
        "R08": "Defendant's prompt emergency application.",
        "R09": "Answer dated May 17, 2026; defendant's defenses pleaded.",
        "R10": "Plaintiff's firm signing as \"Attorneys for Defendant.\"",
    }
    for code, dt, desc, _ in FILINGS:
        rows.append([code, dt, desc, purposes[code]])
    f.append(grid(rows, [0.5 * inch, 0.95 * inch, 2.75 * inch, 2.3 * inch]))

    f.append(P("Part 2. Photographic and documentary exhibits (Tab L, Gillson Evidence Exhibit Binder, Bates GILLSON-).", h2))
    rows = [["Cat.", "Category", "Items", "Relevance"]]
    rel = {
        "A": "Protected activity: written grievances and maintenance requests, November 16, 2025.",
        "B": "Habitability: infestation inside the unit, November 2025 – January 2026, before and after treatment.",
        "C": "Harm: injuries to the service animal; disability nexus.",
        "D": "Harm: injuries to defendant; urgent-care and emergency records.",
        "E": "Plaintiff's knowledge and admissions: Landrum letter; entry notices; January 2, 2026 rent letter.",
        "F": "Protected activity and corroboration: 311 / DPH Case 101003004371; APS letter.",
        "G": "Contemporaneous notes, including statement attributed to \"Mark.\"",
        "H": "Common-area conditions and repair activity.",
        "I": "Security at the premises: vehicle break-in; U.S. Park Police Case 251250105.",
    }
    for letter_, title, items in CATEGORIES:
        rows.append([letter_, title, str(len(items)), rel.get(letter_, "")])
    rows.append(["J", "Evidentiary notices served on opposing counsel and forwarded to the Court, October 29–30, 2026", "4", "Notice to plaintiff of the video exhibits and preservation demand."])
    rows.append(["K", "Complaints filed with the California Board of Behavioral Sciences, January 2, 2026", "2", "Protected activity preceding the notice."])
    f.append(grid(rows, [0.5 * inch, 2.6 * inch, 0.6 * inch, 2.8 * inch]))

    f.append(P("Part 3. Court orders, accommodation record, and defendant's trial papers.", h2))
    rows = [["Tab", "Exhibit", "Relevance"]]
    rows.append(["I", "Notice to Francisco Torres, Esq. re fraudulent service, retaliation, hearsay, and medical chronology (Oct. 31, 2026); seven civil subpoenas duces tecum with Attachment 3; service directory and log", "Notice to counsel; compulsory process for the witnesses and records above."])
    rows.append(["J", "Request for Accommodations (MC-410) for Department 606 with Attachment; CONFIDENTIAL medical exhibit (John Muir Health ED, Oct. 30, 2026)", "Rule 1.100 request for trial; medical basis for remote appearance (confidential)."])
    rows.append(["K", f"Twenty rule 1.100 responses and orders of this Court, July 20 – October 14, 2026 (Exhibits 1–{len(ADA_EXHIBITS)})", "Dates of protected activity; plaintiff's counsel's notice of the Court's orders."])
    rows.append(["M", "Board of Behavioral Sciences complaints Nos. 2002026002097 and 2002026002098", "Protected activity, January 2, 2026."])
    f.append(grid(rows, [0.5 * inch, 3.6 * inch, 2.4 * inch]))

    f.append(P("Part 4. Audio-visual exhibits.", h2))
    f.append(P("See Tab E for the two designated video suites (V-01 through V-07 and second-suite V-01 through V-06), served on plaintiff's counsel October 29, 2026 with preservation demands."))
    f += signature()
    return rl(f, path, "Evidence List")


# ------------------------------------------------------------------ TAB E: Video list
def video_list(path):
    f = caption("DEFENDANT'S AUDIO-VISUAL EXHIBIT LIST (VIDEO LIST)")
    f.append(P(
        "The recordings below were designated as trial exhibits by formal evidentiary notice e-mailed to plaintiff's counsel on October 29, 2026 "
        "at 11:00 p.m. and 11:21 p.m. (Tab L, Category J). Each recording is maintained in a Google Drive repository at the link shown; native files "
        "with metadata will be lodged on a USB drive at trial call. Defendant will authenticate each recording by his own testimony as the person who "
        "made it (Evid. Code, §§ 1400, 1401) and offers the staff statements within them as party admissions (Evid. Code, § 1222) or, alternatively, "
        "for their effect on the listener and as prior inconsistent statements (Evid. Code, § 1235)."))
    for suite_idx, heading in [(0, "Suite 1 – Exhibits V-01 through V-07 (notice sent 11:00:17 p.m. PDT)"), (1, "Suite 2 – Newly added Exhibits V-01 through V-06 (notice sent 11:21:32 p.m. PDT)")]:
        f.append(P(heading, h2))
        rows = [["Ex.", "Title and description", "Repository link"]]
        for code, title, url, desc in NOTICES[suite_idx]["videos"]:
            rows.append([P(code, cellb), P(f"<b>{title}</b><br/>{desc}", cell), P(url, cellurl)])
        f.append(grid(rows, [0.55 * inch, 3.6 * inch, 2.35 * inch]))
    f.append(P("Publication plan", h2))
    f.append(P(
        "Defendant will publish second-suite V-03 (Dwayne – management admissions) and V-05 (Dwayne – accidental legal service) during the testimony of "
        "Mr. Landrum and Mr. Bradford on the service question; second-suite V-01 and V-04 (Landrum confrontation; verbal assault) on retaliation and motive; "
        "first-suite V-02 (habitability) with the photographs at Tab L; and first-suite V-04 (courthouse confrontation and process-server conduct) on the "
        "credibility of the service declarations. Running time for all designated clips is estimated at under ninety minutes."))
    f += signature()
    return rl(f, path, "Video List")


# ------------------------------------------------------------------ TAB F: Points and authorities – new notice, new action
def points_authorities(path):
    f = caption("MEMORANDUM OF POINTS AND AUTHORITIES: WHY PLAINTIFF MUST SERVE A NEW NOTICE AND FILE A NEW ACTION, AND WHY SUBSTITUTION OF COUNSEL DOES NOT CURE THE RECORD")
    f.append(P("I. Introduction", h2))
    f.append(P(
        "Plaintiff's complaint was prepared and signed by John Zanghi. Francisco Torres now handles the matter. Defendant anticipates plaintiff will argue that "
        "new counsel may simply carry the existing case to trial. The law is otherwise. The defects in this record are not drafting errors that a new lawyer can "
        "re-paper. They go to the notice, the verification, the service, and the default – each a jurisdictional or quasi-jurisdictional prerequisite in a summary "
        "unlawful detainer proceeding. If plaintiff wishes to proceed, it must serve a lawful notice and file a new, properly verified action."))

    f.append(P("II. A Defective Notice Cannot Be Cured by Amendment; the Action Must Be Dismissed", h2))
    f.append(P(
        "Unlawful detainer is a summary statutory remedy, and the landlord must strictly comply with the notice requirements of Code of Civil Procedure section 1161. "
        "A notice that fails those requirements will not support the action. (<i>Kwok v. Bergren</i> (1982) 130 Cal.App.3d 596, 599–600; <i>Liebovich v. Shahrokhkhany</i> "
        "(1997) 56 Cal.App.4th 511, 513; <i>Bevill v. Zoura</i> (1994) 27 Cal.App.4th 694, 697.) Because a valid notice is an element of the cause of action and must "
        "precede the filing of the complaint, the defect cannot be cured by amending the complaint. (<i>Delta Imports, Inc. v. Municipal Court</i> (1983) 146 Cal.App.3d "
        "1033, 1036 [complaint failing to allege a proper notice does not state a cause of action for unlawful detainer].) The only remedy is a new notice followed by a new action."))
    f.append(P(
        "Here the notice's own proof of service recites two incompatible modes of service, the notice period does not correspond to any notice the statute recognizes, and the "
        "complaint's item 7 states that no proper notice was served. Statutory extensions for mailing under Civil Code section 1013 do not apply to unlawful detainer notices and "
        "cannot explain the eight-day period. (<i>Losornio v. Motta</i> (1998) 67 Cal.App.4th 110, 115–116.)"))

    f.append(P("III. The HUD Notice Requirements Are a Condition Precedent That Was Not Met", h2))
    f.append(P(
        "Unit 301A is a HUD-assisted unit; plaintiff admits the HUD-50059 exists but \"cannot be located.\" For such tenancies, 24 Code of Federal Regulations part 247 governs. "
        "The landlord may terminate only for the good-cause grounds listed in section 247.3, and the notice must state the reasons for termination \"with enough specificity so as "
        "to enable the tenant to prepare a defense,\" advise the tenant of the right to meet with the landlord within ten days to discuss the proposed termination, and be served "
        "both by first-class mail and by hand delivery or posting. (24 C.F.R. § 247.4(a)–(b).) California courts treat compliance with these federal notice requirements as a "
        "condition precedent to an unlawful detainer action. (<i>Gersten Companies v. Deloney</i> (1989) 212 Cal.App.3d 1119, 1127–1129.) No compliant notice appears in this record."))

    f.append(P("IV. The Complaint Is Not Verified by Plaintiff and Cannot Support Judgment", h2))
    f.append(P(
        "An unlawful detainer complaint \"shall be verified.\" (Code Civ. Proc., § 1166, subd. (a)(1).) Verification must be by the party or, for a corporation, by an officer or "
        "agent with knowledge. (Code Civ. Proc., § 446, subd. (a).) The verification page attached to this complaint names the defendant. A verification by the adverse party is "
        "a nullity; the complaint stands unverified and is subject to a motion to strike. The defect also infects the default: a clerk may enter judgment for possession under "
        "section 1169 only on a verified complaint whose allegations are deemed admitted by the default. There was no competent verification to be admitted."))

    f.append(P("V. Service by Posting Was Not Authorized by Diligence, and the Proof of Service Does Not Name the Defendant", h2))
    f.append(P(
        "Service by posting under section 415.45 is available only on a court order supported by an affidavit showing that the defendant \"cannot with reasonable diligence be "
        "served in any manner specified\" in sections 415.10 through 415.40. (Code Civ. Proc., § 415.45, subd. (a).) Reasonable diligence means a thorough, systematic inquiry "
        "using the means reasonably available – including the means the plaintiff already has in hand. (<i>Evartt v. Superior Court</i> (1979) 89 Cal.App.3d 795, 801–802; "
        "<i>Board of Trustees of Leland Stanford Junior University v. Ham</i> (2013) 216 Cal.App.4th 330, 337–339 [affidavit insufficient where obvious avenues were not tried].) "
        "Plaintiff's counsel had defendant's e-mail address and telephone number, had seen him in court on March 19, 2026, and operated the building where he lives. None of that was used."))
    f.append(P(
        "More fundamentally, the declaration of diligence was signed May 11, 2026 and describes an attempt on May 12, 2026. A declaration that attests to a future event is false "
        "when made. (Code Civ. Proc., § 2015.5; Pen. Code, § 118.) A judgment obtained on a false return of service is void for extrinsic fraud and may be set aside at any time. "
        "(<i>County of San Diego v. Gorham</i> (2010) 186 Cal.App.4th 1215, 1228–1231; Code Civ. Proc., �� 473, subd. (d).) And the only proof of service of summons in the record "
        "names \"All Unnamed Occupants,\" not Donald Gillson. Without a return of service on the named defendant, the clerk had no authority to enter his default. (Code Civ. Proc., §§ 417.10, 585, 1169.)"))

    f.append(P("VI. The Default Was Void if an Answer Was on File, and Premature if the Response Period Was Miscounted", h2))
    f.append(P(
        "A clerk may not enter default while a responsive pleading is on file; a default so entered is void and must be set aside. (Code Civ. Proc., §§ 585, 473, subd. (d); "
        "<i>Wilson v. Goldman</i> (1969) 274 Cal.App.2d 573, 576–577.) The record contains an Answer dated May 17, 2026. If it was filed, the June 30, 2026 default is void. "
        "Independently, service by posting is complete on the tenth day after posting and mailing (§ 415.45, subd. (c)), and the tenant then has ten court days to respond "
        "(§ 1167, as amended by Assembly Bill 2347, effective January 1, 2025). Plaintiff requested default on the earliest arguable day; any error in counting – including the "
        "June 19 court holiday – made the request premature and the default void."))

    f.append(P("VII. Substitution of Counsel Does Not Cure Any of This", h2))
    f.append(P(
        "A party may change attorneys by consent or court order (Code Civ. Proc., §§ 284, 285), and the change does not itself require a new action. But substitution does not "
        "re-verify a complaint, re-serve a notice, or re-date a declaration. New counsel inherits the record as it stands and the duty of candor about it. (Rules Prof. Conduct, "
        "rule 3.3(a)(1), (a)(3) [duty to correct false statements of fact previously made to the tribunal]; Bus. & Prof. Code, § 6068, subd. (d).) Mr. Torres is therefore "
        "obliged either to withdraw the defective papers and begin again with a lawful notice and a verified complaint, or to defend them as they are. He cannot do both, "
        "and he cannot amend his way around a notice that was defective before the case began."))
    f.append(P(
        "The July 8, 2026 points and authorities signed by Mr. Zanghi as \"Attorneys for Defendant\" (Tab H, R10) compounds the problem. A lawyer may not represent adverse "
        "parties in the same matter (Rules Prof. Conduct, rule 1.7(a)), and a paper that misidentifies whom counsel represents is a misstatement to the Court. If the firm "
        "contends the caption was an error, the error is itself evidence of the care with which these papers were prepared."))

    f.append(P("VIII. Retaliation Is a Complete Defense", h2))
    f.append(P(
        "A landlord may not seek to recover possession in retaliation for a tenant's complaint to a public agency about habitability, or for the tenant's lawful exercise of rights, "
        "within 180 days of the protected act. (Civ. Code, § 1942.5, subds. (a), (d).) Retaliatory eviction is an affirmative defense in unlawful detainer. (<i>Barela v. Superior "
        "Court</i> (1981) 30 Cal.3d 244, 249–253; <i>Schweiger v. Superior Court</i> (1970) 3 Cal.3d 507, 513–517.) The notice issued April 8, 2026 – within 180 days of the "
        "November 19, 2025 DPH referral, the December 5, 2025 APS contact, and the January 2, 2026 licensing complaints. Retaliation against a tenant for requesting disability "
        "accommodation is independently unlawful. (Gov. Code, § 12955, subd. (f); 42 U.S.C. § 3617; Civ. Code, §§ 54.1, 54.2 [service animal].) A landlord who violates section "
        "1942.5 is liable for actual damages, punitive damages of $100 to $2,000 per retaliatory act, and attorney fees. (Civ. Code, § 1942.5, subds. (h), (i).)"))

    f.append(P("IX. Sanctions and Referral", h2))
    f.append(P(
        "The Court may impose sanctions for filings presented for an improper purpose or without evidentiary support (Code Civ. Proc., § 128.7, subds. (b), (c)) and for bad-faith "
        "tactics (§ 128.5). A false declaration of service is perjury (Pen. Code, § 118) and may be referred to the District Attorney. Defendant requests that the Court exercise "
        "these powers as it deems appropriate after hearing from the declarants under oath."))

    f.append(P("X. Conclusion", h2))
    f.append(P(
        "The notice is defective and cannot be amended. The complaint is unverified. The service declarations are impossible on their face, and the proof of service does not name "
        "the defendant. The default was entered over an existing Answer or on a miscounted deadline. Plaintiff's counsel has filed in this case as counsel for the defendant. "
        "Judgment should be entered for defendant. If plaintiff believes it has good cause to terminate a HUD-assisted tenancy, the law gives it one route: a compliant notice, "
        "properly served, followed by a new and properly verified complaint."))
    f.append(P("Table of Authorities", h2))
    auth = [
        ("Cases", ["Barela v. Superior Court (1981) 30 Cal.3d 244", "Bevill v. Zoura (1994) 27 Cal.App.4th 694", "Board of Trustees of Leland Stanford Junior University v. Ham (2013) 216 Cal.App.4th 330",
                   "County of San Diego v. Gorham (2010) 186 Cal.App.4th 1215", "Delta Imports, Inc. v. Municipal Court (1983) 146 Cal.App.3d 1033", "Evartt v. Superior Court (1979) 89 Cal.App.3d 795",
                   "Gersten Companies v. Deloney (1989) 212 Cal.App.3d 1119", "Kwok v. Bergren (1982) 130 Cal.App.3d 596", "Liebovich v. Shahrokhkhany (1997) 56 Cal.App.4th 511",
                   "Losornio v. Motta (1998) 67 Cal.App.4th 110", "Schweiger v. Superior Court (1970) 3 Cal.3d 507", "Wilson v. Goldman (1969) 274 Cal.App.2d 573"]),
        ("Statutes and rules", ["Code Civ. Proc., §§ 128.5, 128.7, 284, 285, 415.10–415.50, 417.10, 446, 473(b), 473(d), 585, 1013, 1161, 1162, 1166, 1167, 1169, 1174, 2015.5",
                                "Civ. Code, §§ 54.1, 54.2, 1717, 1942.5", "Gov. Code, § 12955(f)", "Pen. Code, § 118", "Evid. Code, §§ 452(d), 453, 1222, 1235, 1400, 1401",
                                "Bus. & Prof. Code, § 6068(d)", "Rules Prof. Conduct, rules 1.7, 3.3", "Cal. Rules of Court, rule 1.100", "24 C.F.R. §§ 247.3, 247.4; 42 U.S.C. § 3617"]),
    ]
    rows = [["Category", "Authority"]]
    for cat, items in auth:
        rows.append([cat, P("<br/>".join(items), cell)])
    f.append(grid(rows, [1.4 * inch, 5.1 * inch]))
    f += signature()
    return rl(f, path, "Points and Authorities")


# ------------------------------------------------------------------ TAB G: Closing argument
def closing(path):
    f = caption("DEFENDANT'S CLOSING ARGUMENT (OUTLINE FOR DELIVERY)")
    f.append(P(
        "Your Honor, this case asks a simple question: did Swords to Plowshares do what the law requires before it asked this Court to put a disabled veteran out of his home? "
        "The record answers no – not once, but at every step."))
    f.append(P("1. The notice", h2))
    f.append(P(
        "Begin where plaintiff had to begin: the notice. Its own proof of service says two things that cannot both be true – that a copy was handed to someone living at the unit, "
        "and that nobody could be found there. It ran eight days, which is not a three-day notice and is not a HUD notice. It does not tell Dr. Gillson why he is being evicted "
        "or that he had ten days to sit down with management. And the complaint's own item 7 says no proper notice was served. The courts of this State have said for forty "
        "years that a landlord who gets the notice wrong loses the case. (<i>Kwok</i>; <i>Liebovich</i>; <i>Bevill</i>.) That is the end of plaintiff's case. Everything that "
        "follows explains why it should also be the beginning of an inquiry."))
    f.append(P("2. The complaint", h2))
    f.append(P(
        "Turn to the verification page. The person swearing to the truth of plaintiff's complaint is \"Donald Gillison.\" That is the defendant, misspelled. Look at the attorney "
        "block: Andrew Wong, January 19, 2025 – a different lawyer, a different year, a different case. Look at the rent: $1,500 a month, and $37.53 a day. This is not a pleading "
        "that was drafted. It is a form that was recycled, and nobody read it before signing it."))
    f.append(P("3. The service", h2))
    f.append(P(
        "Mr. Falanga signed his declaration of diligence on May 11, 2026. In it he swears he tried to serve Dr. Gillson on May 12, 2026 at 6:06 in the evening. He swore to "
        "something that had not happened yet. The firm then told this Court that Dr. Gillson could not be found – while it had his e-mail, had his phone number, had stood "
        "across a courtroom from him on March 19, and ran the building he lives in. The photograph of the posting shows the summons taped beside a management notice dated three days earlier. "
        "They could reach his door whenever they liked. They just did not want to hand him the papers."))
    f.append(P("4. The default", h2))
    f.append(P(
        "The proof of service they filed names \"All Unnamed Occupants.\" There is none for Donald Gillson. An Answer dated May 17 sits in this file. And on June 30 – the first "
        "day anyone could even argue the clock had run – plaintiff asked the clerk for a default and got it, for $0.00, with the forfeiture box left blank. A writ was requested "
        "the next morning. This was not a landlord trying to resolve a tenancy. It was a race to a judgment before the tenant could be heard."))
    f.append(P("5. \"Attorneys for Defendant\"", h2))
    f.append(P(
        "On July 8, plaintiff's own firm filed a paper in this case signed \"Attorneys for Defendant.\" Plaintiff will call it a typo. Accept that for a moment. Then every "
        "document in this file was prepared by a firm whose typos include who it represents, when its process server was at the door, and who swore to its complaint. The Court "
        "does not have to find intent to find that nothing from this firm can be taken at face value."))
    f.append(P("6. Why this happened", h2))
    f.append(P(
        "Look at the calendar. November 2025: Dr. Gillson photographs cockroaches in his refrigerator, his sink, his toilet, and on his service dog. He files grievances. He calls 311, "
        "and the Department of Public Health opens a case. Adult Protective Services writes to him. He is treated at UCSF and at an emergency room. January 2026: he files licensing "
        "complaints against two of plaintiff's clinicians, and plaintiff's management sends a letter warning that \"formal notices may be issued.\" April 8, 2026: the notice. "
        "Civil Code section 1942.5 says that sequence – protected complaints followed within 180 days by a notice to quit – is retaliation, and retaliation is a complete defense. "
        "The staff member on video who describes papers delivered \"by accident\" and instructions from management tells the Court what the paperwork was trying to hide."))
    f.append(P("7. What the Court should do", h2))
    for i, t in enumerate([
        "Enter judgment for Dr. Gillson, because the notice is defective and cannot be amended.",
        "Find that the June 30, 2026 default and judgment were void, so that no part of them can be revived or relied upon.",
        "Require Mr. Falanga, the Martinez declarant, and Mr. Zanghi to explain their declarations and filings under oath, and refer the service declarations as the Court sees fit.",
        "Award Dr. Gillson his costs and fees, and leave plaintiff to the only lawful path it ever had: a proper notice, properly served, and a new case if it can honestly bring one.",
    ], 1):
        f.append(P(f"{i}.&nbsp;&nbsp;{t}", num))
    f.append(P(
        "Dr. Gillson served this country. He asked for a refrigerator without cockroaches in it and for the accommodations this Court has already ordered. "
        "He asks now only that the law be applied to his landlord the way it would be applied to him. Thank you."))
    f += signature()
    return rl(f, path, "Closing Argument")


# ------------------------------------------------------------------ cover and TOC
def cover(path):
    f = [Spacer(1, 1.3 * inch), P("ALL-IN-ONE TRIAL BINDER", ParagraphStyle("big", parent=h1, fontSize=24, leading=32)),
         P("Defendant's Trial Materials and the Filed Record", ParagraphStyle("sub", parent=cen, fontSize=14, leading=22)), Spacer(1, 24),
         P(f"<i>{CASE}</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P(f"Case No. {CASE_NO} (related: CCH-26-589086, CCH-26-589728)", cen), P(COURT, cen), P(f"{DEPT}", cen), P(TRIAL, cen), Spacer(1, 30),
         P(f"Submitted by {NAME}", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 30),
         P("Tabs A through G are defendant's trial papers. Tab H reproduces the filed court record (R01–R10). "
           "Tab I contains the notice to counsel and subpoenas. Tab J (MC-410 and medical exhibit) is for the ADA Coordinator and is confidential "
           "under rule 1.100(c)(4). Tabs K through M are the accommodation record, the photographic evidence binder, and related administrative complaints. "
           "The Solano County accommodation binder is maintained separately.", small),
         Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


def toc(path, rows, case_label=""):
    f = [P("NOTICE OF LODGMENT AND MASTER INDEX OF EXHIBITS", h1), Spacer(1, 6),
         P("Defendant lodges the exhibits indexed below, in the tabbed and Bates-numbered order shown. Each exhibit is separated by its own exhibit sheet bearing its "
           "number and title; the Bates range after each entry is the range of the exhibit itself. Confidential medical exhibits (rule 1.100(c)(4)) are so marked on their sheets. "
           + (case_label or ""), small), Spacer(1, 8)]
    # Color key: one swatch per tab, in binder order.
    letters = [r[0] for r in rows if len(r[0]) == 1]
    if letters:
        key = Table([[P("Color key", cellb)] + [P(f"<b>{l}</b>", ParagraphStyle("kc", parent=cellb, textColor=colors.white, alignment=TA_CENTER)) for l in letters]],
                    colWidths=[0.75 * inch] + [(5.95 * inch) / len(letters)] * len(letters))
        kst = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
        for j, l in enumerate(letters, 1):
            kst.append(("BACKGROUND", (j, 0), (j, 0), colors.HexColor(TAB_COLORS.get(l, "#444444"))))
        key.setStyle(TableStyle(kst)); f += [key, Spacer(1, 8)]
    white_b = ParagraphStyle("wb", parent=cellb, textColor=colors.white)
    data = [["Exhibit", "Document", "Pages", "Bates range"]] + [[r[0], r[1], r[3] if len(r) > 3 else "", r[2]] for r in rows]
    body_rows = []
    for i, r in enumerate(data):
        is_tab = i > 0 and len(r[0]) == 1
        body_rows.append([P(c, white_b if is_tab else (cellb if i == 0 else cell)) for c in r])
    t = Table(body_rows, colWidths=[0.75 * inch, 3.9 * inch, 0.55 * inch, 1.5 * inch], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black), ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.grey),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    current = None
    for i, r in enumerate(data):
        if i == 0:
            continue
        if len(r[0]) == 1:
            current = r[0]
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(TAB_COLORS.get(current, "#444444"))))
        elif current:
            c = colors.HexColor(TAB_COLORS.get(current, "#444444"))
            st.append(("BACKGROUND", (0, i), (0, i), colors.Color(c.red, c.green, c.blue, alpha=0.18)))
            st.append(("LINEBEFORE", (0, i), (0, i), 3, c))
    t.setStyle(TableStyle(st))
    f.append(t)
    f.append(Spacer(1, 14)); f.extend(signature())
    return rl(f, path, "Notice of Lodgment and Master Index of Exhibits")


def exhibit_sheet(path, number, title, pages, confidential=False):
    flow = [Spacer(1, 2.4 * inch), _banner(f"EXHIBIT {number}", str(number)[0], bb.tab, 18), Spacer(1, 14), P(title, tabttl), Spacer(1, 12),
            P(f"{pages} page{'s' if pages != 1 else ''}", ParagraphStyle("es", parent=cen, fontSize=12, leading=18))]
    if confidential:
        flow += [Spacer(1, 10), P("CONFIDENTIAL \u2013 Cal. Rules of Court, rule 1.100(c)(4)", ParagraphStyle("ec", parent=cen, fontSize=12, leading=18, textColor=colors.HexColor("#8B0000")))]
    return rl(flow, path)


def merge(paths, out):
    m = fitz.open()
    for p in paths:
        m.insert_pdf(fitz.open(p))
    m.save(out); m.close()
    return out


def assemble(out_path, cover_pdf, sections, footer_note):
    def build(toc_pdf):
        doc = fitz.open(); bookmarks = []; rows = []; bates = 1
        def add(path, bookmark=None, level=1):
            nonlocal bates
            src = fitz.open(path); start = len(doc); doc.insert_pdf(src)
            if bookmark:
                bookmarks.append([level, bookmark, start + 1])
            first = bates; bates += len(src); src.close()
            return first, bates - 1
        page_tab = {}  # page index -> tab letter, for the fore-edge color index
        add(cover_pdf, "Cover")
        for front_label, front_path in FRONT:
            add(front_path, front_label)
        if toc_pdf:
            add(toc_pdf, "Notice of Lodgment and Master Index of Exhibits")
        n_tabs = len(sections)
        for ti, (letter_, title, items) in enumerate(sections):
            tp = tab_page(os.path.join(TMP, f"aio_tab_{letter_}.pdf"), letter_, title)
            tab_start = len(doc)
            add(tp, f"Tab {letter_} \u2013 {title}")
            rows.append([letter_, f"<b>{title}</b>", "", ""])
            for k, (label, path) in enumerate(items, 1):
                num = f"{letter_}-{k}"; npages = len(fitz.open(path))
                conf = ("MC-410" in title or "Confidential" in title or "Medical" in title or "medical" in label.lower())
                if "highlighted excerpts" in label:
                    # excerpt exhibits carry their own title band on every page; a separate cover slip would only add pages
                    a, b = add(path, f"Exhibit {num} \u2013 {label}", 2)
                    first_pg = doc[len(doc) - npages]
                    first_pg.insert_textbox(fitz.Rect(54, 8, 558, 26), f"EXHIBIT {num}", fontsize=11, fontname="hebo", color=(0.16, 0.2, 0.55), align=1)
                else:
                    sheet = exhibit_sheet(os.path.join(TMP, f"aio_ex_{letter_}_{k}.pdf"), num, label, npages, conf)
                    add(sheet, f"Exhibit {num} \u2013 {label}", 2)
                    a, b = add(path)
                rows.append([num, label, f"{PREFIX}-{a:04d} \u2013 {PREFIX}-{b:04d}", str(npages)])
            for pi in range(tab_start, len(doc)):
                page_tab[pi] = (letter_, ti)
        for i, page in enumerate(doc):
            if page.rect.width > page.rect.height:  # every page reads in portrait
                page.set_rotation((page.rotation + 90) % 360)
            r = page.rect; dm = page.derotation_matrix; rot = page.rotation
            if i in page_tab:
                # Fore-edge index: a colored block stepped down the right margin by tab, with the tab letter.
                letter_, ti = page_tab[i]
                usable = r.height - 2.0 * inch; step = usable / max(n_tabs, 1); bh = min(step, 0.6 * inch)
                y0 = 1.0 * inch + ti * step
                blk = fitz.Rect(r.width - 0.32 * inch, y0, r.width, y0 + bh) * dm
                shape = page.new_shape()
                shape.draw_rect(blk); shape.finish(color=None, fill=tab_rgb(letter_))
                shape.commit()
                page.insert_text(fitz.Point(r.width - 0.25 * inch, y0 + bh / 2 + 4) * dm, letter_, fontsize=11, fontname="hebo", color=(1, 1, 1), rotate=rot)
            page.insert_text(fitz.Point(r.width - 1.9 * inch, r.height - 0.35 * inch) * dm, f"{PREFIX}-{i+1:04d}", fontsize=8, fontname="helv", rotate=rot)
            page.insert_text(fitz.Point(0.75 * inch, r.height - 0.35 * inch) * dm, footer_note, fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3), rotate=rot)
        doc.set_toc(bookmarks)
        return doc, rows
    d, rows = build(None); d.close()
    tocp = toc(os.path.join(TMP, "aio_toc.pdf"), rows, footer_note)
    for _ in range(3):  # stabilize index page count
        d, rows = build(tocp); n_toc = len(fitz.open(tocp)); d.close()
        tocp = toc(os.path.join(TMP, "aio_toc.pdf"), rows, footer_note)
        if len(fitz.open(tocp)) == n_toc:
            break
    d, _ = build(tocp)
    d.save(out_path, garbage=3, deflate=True); n = len(d); d.close()
    return n


if __name__ == "__main__":
    photo_counts = {l: len(items) for l, _, items in CATEGORIES}
    print("drafting sections")
    tabA = statement_of_case(os.path.join(TMP, "aio_A.pdf"))
    tabB = irregularities(os.path.join(TMP, "aio_B.pdf"))
    tabC = witness_list(os.path.join(TMP, "aio_C.pdf"))
    tabD = evidence_list(os.path.join(TMP, "aio_D.pdf"), photo_counts)
    tabE = video_list(os.path.join(TMP, "aio_E.pdf"))
    tabF = points_authorities(os.path.join(TMP, "aio_F.pdf"))
    tabG = closing(os.path.join(TMP, "aio_G.pdf"))

    print("MC-410 (SF) and medical exhibit")
    med_ex = medical_exhibit(os.path.join(TMP, "medical_exhibit.pdf"))
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO,
                       f"{COURT} – {DEPT}",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further hearings in this case.", "Defendant", "Unlawful detainer",
                       "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    mc_sf_merged = merge(mc_sf, os.path.join(TMP, "aio_mc_sf.pdf"))

    print("subpoenas")
    sub_items = []
    for w in WITNESSES:
        parts = make_subpoena(w)
        sub_items.append((f"Civil Subpoena (Duces Tecum) – {w['name']}", merge(parts, os.path.join(TMP, f"aio_subp_{w['tag']}.pdf"))))
    svc_rows = [["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES]
    log_rows = [["Witness", "Date / time served", "Served by", "Fees tendered", "Proof filed"]] + [[w["name"].split(",")[0], "", "", "", ""] for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY AND SERVICE LOG", h1),
              P("Subpoenas must be issued by the clerk before service and personally served, with witness fees tendered on demand (Code Civ. Proc., §§ 1985, 1987; Gov. Code, § 68093). "
                "Serve each subpoena with its Attachment 3. Complete the proof of service on page 3 of each SUBP-002 and file it with Department 606.", small),
              Spacer(1, 10), grid(svc_rows, [2.1 * inch, 2.2 * inch, 2.2 * inch]), Spacer(1, 14), P("Service log", h2),
              grid(log_rows, [2.1 * inch, 1.2 * inch, 1.2 * inch, 1.0 * inch, 1.0 * inch])], os.path.join(TMP, "aio_svc.pdf"))

    ada_items = [(f"Ex. {i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]
    filing_items = [(f"{code} – {dt} – {desc}", os.path.join(FIL, fn)) for code, dt, desc, fn in FILINGS]

    sections = [
        ("A", "Statement of the Case", [("Defendant's Statement of the Case", tabA)]),
        ("B", "Index of Record Irregularities and Indicia of Fraud", [("Line-by-line index, 22 entries", tabB)]),
        ("C", "Witness List", [("Witness list and offer of proof, 16 witnesses", tabC)]),
        ("D", "Evidence List", [("Exhibit and evidence list, Parts 1–4", tabD)]),
        ("E", "Video List", [("Audio-visual exhibit list, two suites, publication plan", tabE)]),
        ("F", "Points and Authorities – New Notice and New Action Required", [("Memorandum with table of authorities", tabF)]),
        ("G", "Closing Argument", [("Closing argument outline", tabG)]),
        ("H", "The Filed Court Record (R01–R10)", filing_items),
        ("I", "Notice to Counsel and Civil Subpoenas (SUBP-002 with Attachment 3)",
         [("Notice to Francisco Torres, Esq., October 31, 2026", os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")),
          ("Service directory and service log", svc)] + sub_items),
        ("J", "Request for Accommodations – MC-410 (Dept. 606) – CONFIDENTIAL IN PART",
         [("MC-410 with Attachment (Items 3–5)", mc_sf_merged),
          ("CONFIDENTIAL Exhibit – John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)]),
        ("K", "Rule 1.100 Orders and Responses of this Court (July–October 2026)", ada_items),
        ("L", "Evidence Exhibit Binder – Photographs, Notices, and Agency Records (Categories A–K)",
         [("Gillson Evidence Exhibit Binder (Bates GILLSON-)", os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
        ("M", "Related Administrative Complaints",
         [("BBS Complaint 2002026002097 – Kolby Losik", os.path.join(COMP, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
          ("BBS Complaint 2002026002098 – Mark Villalobos", os.path.join(COMP, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))]),
    ]
    cov = cover(os.path.join(TMP, "aio_cover.pdf"))
    n = assemble(OUT, cov, sections, "Gillson – All-in-One Trial Binder – CUD-26-682107 – Tab J confidential in part (CRC 1.100(c)(4))")
    print("pages", n)
    compress_scans(OUT)
