"""
Integrated Statement of the Case: the narrative with the record embedded in it.

Every factual paragraph is pinned to a record cite (R01–R10 = the filed court record,
Tab letters = this binder).  Key pages are cropped from the filed PDFs and placed
inline as numbered figures so the Court reads the assertion and sees the page.

Outputs (in /vercel/share/artifacts):
  Gillson_Integrated_Statement_of_the_Case_CUD-26-682107.pdf
  Gillson_Integrated_Statement_of_the_Case_CUD-26-682107.docx
  Gillson_Master_Trial_Binder_INTEGRATED_CUD-26-682107.pdf  (full binder, Tab A = this statement)
"""
import os, re, sys, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Image as RLImage, KeepTogether, Table, TableStyle, PageBreak
from reportlab.lib import colors
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_allinone as A
from build_allinone import (P, rl, caption, grid, signature, h1, h2, h3, body, cell, cellb, small, cen,
                            FILINGS, TEXT_W, TMP, FIL, HERE, COMP, ART, CASE, CASE_NO, COURT, DEPT, TRIAL, DATED, NAME)

FIG = os.path.join(HERE, "tmp", "fig"); os.makedirs(FIG, exist_ok=True)
INC = os.path.join(HERE, "incoming")
OUT_PDF = os.path.join(ART, "Gillson_Integrated_Statement_of_the_Case_CUD-26-682107.pdf")
OUT_DOCX = os.path.join(ART, "Gillson_Integrated_Statement_of_the_Case_CUD-26-682107.docx")
OUT_BINDER = os.path.join(ART, "Gillson_Master_Trial_Binder_INTEGRATED_CUD-26-682107.pdf")

# Type: 12.5 pt body (reduced from the earlier binders), 22.5 pt subject-matter headings, 15 pt sub-headings.
BODY_PT, H2_PT, H3_PT = 12.5, 22.5, 15
body = ParagraphStyle("ibody", parent=body, fontSize=BODY_PT, leading=BODY_PT * 1.45, spaceAfter=8)
h2 = ParagraphStyle("ih2", parent=h2, fontSize=H2_PT, leading=H2_PT * 1.2, spaceBefore=16, spaceAfter=8)
h3 = ParagraphStyle("ih3", parent=h3, fontSize=H3_PT, leading=H3_PT * 1.3, spaceBefore=12, spaceAfter=6)
phase = ParagraphStyle("phase", parent=small, fontSize=9.5, leading=12, textColor=colors.HexColor("#555555"), spaceBefore=14, spaceAfter=0)
capstyle = ParagraphStyle("cap", parent=small, fontSize=9.5, leading=13, spaceBefore=3, spaceAfter=10, textColor=colors.HexColor("#222222"))
chkstyle = ParagraphStyle("chk", parent=small, fontSize=10, leading=13.5)
chkbox = TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#888888")),
                     ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)])
figbox = TableStyle([("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#555555")), ("TOPPADDING", (0, 0), (-1, -1), 4),
                     ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)])


def rpath(code):
    return os.path.join(FIL, next(fn for c, _, _, fn in FILINGS if c == code))


# ------------------------------------------------------------------ figures: (key, source, page, crop-fraction box, caption)
# crop = (x0, y0, x1, y1) as fractions of the page
FIGS = [
    ("F1", rpath("R01"), 33, (0.08, 0.14, 0.92, 0.80),
     "R01 p. 33 — Notice to Quit dated April 8, 2026 (Complaint Exhibit 2), page 1 of 3. The stated grounds include defendant's "
     "February 25, 2026 petition for an Elder/Dependent Adult Abuse Restraining Order against the Assistant Property Manager, and "
     "\u201cover one thousand (1,000) lengthy emails\u201d to management \u2014 the written-communication channel that is defendant's disability accommodation."),
    ("F2", rpath("R01"), 35, (0.08, 0.05, 0.92, 0.78),
     "R01 p. 35 — Notice to Quit, page 3 of 3. States that the tenancy \u201cis exempt from the provisions of the San Francisco Residential Rent "
     "Stabilization and Arbitration Ordinance,\u201d is dated 4/8/2026, signed by Jerome Bradford \u201cFor Swords to Plowshares,\u201d and copied to the "
     "San Francisco Housing Authority and SF DHSH before any adjudication."),
    ("F3", rpath("R01"), 5, (0.06, 0.20, 0.94, 0.78),
     "R01 p. 5 — Complaint (UD-100) page 3, items 9\u201314. Plaintiff pleads that the notice expired 4/16/2026, that it was served by posting on "
     "4/8/2026 and mailing on 4/8/2026 \u201cbecause no person of suitable age or discretion can be found there,\u201d that proof of service of the notice "
     "is attached as Exhibit 3, and that fair rental value is $37.53 per day."),
    ("F4", rpath("R01"), 55, (0.08, 0.05, 0.92, 0.50),
     "R01 p. 55 — Verification of the Complaint, signed by Jerome Bradford on 5/4/2026 as an \u201cauthorized employee\u201d declaring the facts "
     "\u201cwithin my personal knowledge.\u201d Mr. Bradford also signed the notice; he is the person whose presence at the claimed posting is disputed."),
    ("F5", rpath("R01"), 56, (0.06, 0.04, 0.94, 0.42),
     "R01 p. 56 — Civil Case Cover Sheet (CM-010), FILED May 5, 2026, designating the case as a limited civil matter; counsel John P. Zanghi and "
     "Charity Martinez, Zanghi Torres Adams LLP."),
    ("F6", rpath("R02"), 1, (0.06, 0.04, 0.94, 0.62),
     "R02 p. 1 — Plaintiff's Ex Parte Application for an order permitting service of the summons by posting (Code Civ. Proc., \u00a7 415.45), filed May 19, 2026 "
     "\u2014 two days after defendant's Answer was dated and while defendant's address, email and telephone were known to counsel from the related restraining-order case."),
    ("F7", rpath("R05"), 1, (0.06, 0.30, 0.94, 0.62),
     "R05 p. 1 — Proof of Service of Summons (POS-010), items 2\u20134: documents served include the Prejudgment Claim of Right of Possession; "
     "the party served (item 3a) is \u201cAll Unnamed Occupants.\u201d No POS-010 naming Donald Gillson as the party served appears in the record."),
    ("F8", rpath("R05"), 2, (0.06, 0.18, 0.94, 0.80),
     "R05 p. 2 — POS-010 continued: service \u201cPer CCP 415.45 By posting the documents on the premises \u2026 on Thurs, June 4 2026 at 11:03 AM, and by causing copies "
     "to be mailed by certified mail on Thurs, June 4 2026\u201d; server Joseph Falanga, Spirit Courier, Reg. No. 1539; signed 6/12/2026; filed 06/30/2026 \u2014 the same day default was entered."),
    ("F9", rpath("R03"), 1, (0.06, 0.03, 0.94, 0.40),
     "R03 p. 1 — Request for Entry of Default (CIV-100), electronically filed 06/30/2026, stamped \u201cDEFAULT ENTERED AS REQUESTED\u201d by the clerk the same day."),
    ("F10", rpath("R04"), 1, (0.06, 0.03, 0.94, 0.45),
     "R04 p. 1 — Judgment \u2014 Unlawful Detainer (UD-110), clerk's judgment by default for possession only ($0.00), \u201cDEFAULT JUDGMENT ENTERED\u201d 06/30/2026."),
    ("F11", rpath("R06"), 1, (0.06, 0.03, 0.94, 0.45),
     "R06 p. 1 — Notice of Entry of Judgment, electronically filed 07/01/2026 by Zanghi Torres Adams LLP; the accompanying POS-030 (R06 p. 3) is signed by "
     "Itzayana Flores and states the notice was placed for mailing to 1030 Girard Road, Unit #301A on 07/01/2026."),
    ("F12", rpath("R08"), 1, (0.06, 0.03, 0.94, 0.55),
     "R08 p. 1 — Defendant's Emergency Ex Parte Application (stay of execution / recall of writ / set aside default), FILED July 7, 2026, seven days after the "
     "default judgment and six days after notice of entry was mailed."),
    ("F13", rpath("R10"), 1, (0.06, 0.03, 0.94, 0.60),
     "R10 p. 1 — Order re Defendant's Ex Parte Application, FILED July 8, 2026 (heard July 7, 2026); served by the clerk on both sides on July 8, 2026."),
    ("F14", rpath("R10"), 2, (0.06, 0.04, 0.94, 0.48),
     "R10 p. 2 — The July 8, 2026 order (Hon. Charles F. Haines): hearing on a Motion to Vacate Default and Default Judgment set for July 22, 2026; defendant's "
     "July 7 papers deemed the moving papers; plaintiff to oppose by July 14 and defendant to reply by July 17; \u201cThe writ issued on July 1, 2026 shall not be executed prior to July 22, 2026.\u201d"),
]


def render_figs():
    out = {}
    for key, src, pg, box, cap in FIGS:
        d = fitz.open(src); page = d[pg - 1]; r = page.rect
        clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
        pix = page.get_pixmap(dpi=150, clip=clip)
        p = os.path.join(FIG, f"{key}.png"); pix.save(p); out[key] = (p, pix.width, pix.height, cap)
        d.close()
    return out


def contact_sheet(figs, path):
    from PIL import Image, ImageDraw
    ims = []
    for key, *_ in FIGS:
        im = Image.open(figs[key][0]).convert("RGB"); w = 520; im = im.resize((w, int(w * im.height / im.width)))
        dr = ImageDraw.Draw(im); dr.rectangle([0, 0, 60, 18], fill="yellow"); dr.text((4, 3), key, fill="black"); ims.append(im)
    cols = 3; rows = (len(ims) + cols - 1) // cols; hmax = max(i.height for i in ims)
    S = Image.new("RGB", (cols * 520, rows * hmax), "white")
    for k, im in enumerate(ims):
        S.paste(im, ((k % cols) * 520, (k // cols) * hmax))
    S.save(path)


# ------------------------------------------------------------------ content model shared by PDF and DOCX
# ("h2", text) | ("h3", text) | ("p", text) | ("n", text)  numbered paragraph | ("fig", key) | ("table", rows, widths)
FIG_NO = {k: i + 1 for i, (k, *_) in enumerate(FIGS)}


def fr(key):
    return f"Figure {FIG_NO[key]}"


CONTENT = [
    ("phase", "STRUCTURE OF THIS STATEMENT"),
    ("h2", "Reader's Map"),
    ("p", "This statement is organized on the ADDIE model (Analyze, Design, Develop, Implement, Evaluate) so that a reader coming to the file cold can follow it in "
          "one pass, and on SAM (Successive Approximation) within each chronology section: the record is shown, then checked, then carried forward. Each phase is labeled "
          "where it begins. Each chronology section closes with a Checkpoint stating what the record shows, what it omits, and what is asked of the Court on that point."),
    ("table", [
        ["Phase", "Part", "Purpose for the Court"],
        ["Analyze", "I\u2013II", "What this case is, who the parties are, and what question is actually before the Court."],
        ["Design", "I \u00b6 2; VI", "How the record is cited (R01\u2013R10, Tabs A\u2013M), how figures map to Bates pages, and how to verify any sentence."],
        ["Develop", "III A\u2013J", "The chronology, built from plaintiff's own filings, with the relevant page reproduced at the point it is discussed."],
        ["Implement", "IV", "The contradictions applied: each representation set against the paper that contradicts it."],
        ["Evaluate", "V; Verification", "The issues for trial, the relief requested, and the declarant's verification under penalty of perjury."],
    ], [1.0 * inch, 1.0 * inch, 4.5 * inch]),
    ("phase", "PHASE 1 \u2014 ANALYZE"),
    ("h2", "I. Nature of the Action and How to Read This Statement"),
    ("n", "This is a residential unlawful detainer for possession only. Judgment was entered by clerk's default on June 30, 2026 for $0.00 (R04). "
          "Defendant, a service-connected disabled veteran proceeding in propria persona under the Court's rule 1.100 accommodation orders (Tab K), "
          "contends the action is retaliatory on the face of plaintiff's own notice, rests on a notice and a service record that do not withstand "
          "inspection, and was pushed to default while defendant's Answer and accommodation request were in the Court's hands."),
    ("n", "Every factual statement below carries a record cite. \u201cR01\u201d through \u201cR10\u201d are the ten filed court documents reproduced in full at Tab H, "
          "Bates-numbered; the same documents were separately downloaded from the Court's docket on October 31, 2026 under document numbers 10197292, 10224145, "
          "10294374, 10294375, 10294379, 10297112\u201310297114, 10303427, 10303428 and 10306382, and are identical. Where a page matters, it is reproduced "
          "inline as a numbered figure so the Court can read the assertion and the page together. The cropping is for legibility only; the full page is at the cited Bates location."),

    ("h2", "II. Parties and Premises"),
    ("n", "Plaintiff Swords to Plowshares, a California nonprofit, is the housing provider for the Jon W. Paulson Veterans Community at 1030 Girard Road, "
          "in the Presidio of San Francisco. It is also a veterans' advocacy organization. Its property management and clinical functions are performed by the "
          "same personnel who are the complaining witnesses here (R01 pp. 33\u201335; Tab C)."),
    ("n", "Defendant Donald Ernest Gillson, Ed.D., has occupied Unit 301A under a HUD-VASH / project-based subsidy tenancy. He has service-connected PTSD and "
          "traumatic brain injury, uses a psychiatric service dog, and since November 20, 2025 has had a written request for reasonable accommodation pending "
          "with plaintiff, the core of which is that management communicate with him in writing (R09, Answer, First and Second Affirmative Defenses; Tab K)."),

    ("phase", "PHASE 3 \u2014 DEVELOP (SAM: show the record, check it, carry it forward)"),
    ("h2", "III. Chronology, With the Record"),
    ("h3", "A. Protected activity preceding the notice (November 2025 \u2013 March 2026)"),
    ("n", "November 20, 2025: defendant's written Reasonable Accommodation Request (R09, Answer, First Aff. Def., citing evidence node GMAIL-02-RAR). "
          "December 23, 2025: accommodation consensus on written, email-based communication reached among defendant, Joel Champion and Kobe (Kolby) Losik (Tab D, Ex. A). "
          "January 2, 2026: Mr. Losik's recorded statement to defendant, \u201cstop with the fucking emails, or else\u201d (Tab D, Ex. B; Tab E). "
          "January 3, 2026: confrontation by property manager William Landrum (Tab C). "
          "February 25, 2026: defendant petitions this Court for an Elder/Dependent Adult Abuse Restraining Order against the Assistant Property Manager, "
          "case CCH-26-589086; hearing March 19, 2026 (R01 p. 33, plaintiff's own recital). Each of these is protected activity under Civil Code section 1942.5 and "
          "Government Code section 12955, subdivision (f). The January 2, 2026 statement and the January 3, 2026 confrontation, both directed at defendant's complaints and "
          "accommodation requests, fall within the 180 days preceding the April 8, 2026 notice; under section 1942.5, subdivision (a), a notice issued within that window "
          "after protected complaints is presumptively retaliatory and the burden shifts to plaintiff to prove a non-retaliatory purpose."),

    ("chk", "Protected activity Nov. 2025–Mar. 2026 recited in plaintiff's own notice (R01 p. 33).", 'Any warning, notice to cure, or incident report preceding the notice.', 'Treat the notice as issuing within the 180-day window of Civ. Code § 1942.5(a).'),

    ("h3", "B. The April 8, 2026 Notice to Quit (R01 pp. 33\u201335; Complaint Exhibit 2)"),
    ("n", f"The notice is a three-page nuisance notice under Code of Civil Procedure section 1161, subdivision (4), demanding possession by April 16, 2026. "
          f"Its first enumerated ground is defendant's February 25, 2026 restraining-order petition and his March 19, 2026 court appearance ({fr('F1')}). "
          f"Its second is that defendant sent management \u201cover one thousand (1,000) lengthy emails\u201d ({fr('F1')}). A notice to quit that names the tenant's "
          f"court petition and the tenant's accommodated communication channel as the nuisance is a retaliatory notice on its own face (Civ. Code, \u00a7 1942.5, subds. (a), (d))."),
    ("fig", "F1"),
    ("n", f"The notice is drafted in the third person and attributes the remaining conduct to unnamed \u201cstaff\u201d on January 23 and February 20, 2026, after the "
          f"accommodation consensus and after Mr. Losik's January 2 threat. No contemporaneous incident report, warning, or notice to cure preceded it (Tab I, Notice to Counsel \u00a7 III). "
          f"The complaining manager, Mr. Landrum, is the person who caused the notice to issue (Tab I \u00a7 III; Tab C)."),
    ("n", f"Page 3 states that the tenancy \u201cis exempt from the provisions of the San Francisco Residential Rent Stabilization and Arbitration Ordinance\u201d ({fr('F2')}). "
          f"Three weeks later plaintiff's complaint pleads in Attachment 18 that the tenancy is subject to, and that plaintiff has complied with, the just-cause requirements "
          f"applicable to a federally subsidized tenancy (R01 pp. 7\u20138). Plaintiff cannot be exempt for purposes of the notice and compliant for purposes of the complaint."),
    ("n", f"The notice is signed by Jerome Bradford \u201cFor Swords to Plowshares\u201d and is copied to the San Francisco Housing Authority and SF DHSH ({fr('F2')}) \u2014 "
          f"publication of accusatory allegations to the subsidy administrator before any adjudication, in a building where the eviction was also publicly posted (R09, P&A, \u201cPublic Posting\u201d)."),
    ("fig", "F2"),

    ("chk", 'Notice names the RO petition and accommodated emails as grounds; declares the tenancy exempt; copied to the Housing Authority (Figs. 1–2).', 'Particularized facts of nuisance; a named declarant with personal knowledge; the Exhibit 3 proof of service.', 'Find the notice retaliatory on its face and insufficient under § 1161(4).'),

    ("h3", "C. The Complaint (R01; filed May 5, 2026; verified May 4, 2026)"),
    ("n", f"The complaint pleads that the notice was served on April 8, 2026 by posting and mailing \u201cbecause no person of suitable age or discretion can be found there\u201d "
          f"({fr('F3')}, item 10a(3)\u2013(4)). Defendant, who was in residence and in continuous written contact with management, was never handed the notice. The "
          f"complaint says the proof of service of the notice is attached as Exhibit 3 (item 10d). On defendant's page-by-page review of the 58-page filed complaint, "
          f"no page labeled Exhibit 3 appears; pages 36\u201354 are the Mayor's Office eviction-prevention insert and HUD VAWA forms. The person who executed the notice, "
          f"Mr. Bradford, is the same person who verified the complaint on personal knowledge ({fr('F4')}), and is the person whose presence at the premises at the time of the "
          f"claimed service is disputed (Tab I \u00a7 II). Production of the original proof of service, access logs and camera footage for that hour has been demanded and the demand is unanswered."),
    ("fig", "F3"),
    ("fig", "F4"),
    ("n", f"The complaint seeks possession and holdover damages at $37.53 per day from April 17, 2026 ({fr('F3')}, item 14; R01 p. 6, item 20g) and is designated a limited civil "
          f"case ({fr('F5')}). It does not plead nonpayment; the only basis is the nuisance notice."),
    ("fig", "F5"),

    ("chk", 'Bradford verified the complaint on personal knowledge the day before filing (Fig. 4); service by posting pleaded (Fig. 3).', 'Exhibit 3; any explanation why personal delivery was impossible to a tenant in residence.', 'Require production of the original proof of service and access/camera records (Tab I § II).'),

    ("h3", "D. Defendant's Answer (dated May 17, 2026) and the Court's access channel"),
    ("n", "Defendant prepared and dated an Answer on May 17, 2026 asserting a general denial and thirteen affirmative defenses, including retaliation, failure to accommodate, "
          "habitability, waiver by acceptance of rent, unclean hands and witness tampering (R09 pp. 22\u201326 of the packet, Bates at Tab H). At the same time defendant was "
          "corresponding with the Court's ADA/access channel regarding his MC-410 request. On June 10, 2026 the Court's clerk advised that plaintiff's default paperwork "
          "could not be processed because it was incomplete, and defendant was told no further action was required while the accommodation request was reviewed (R08 \u00b6\u00b6 6, 10(c)). "
          "The Answer was not entered on the docket; the Court later recognized that the ADA/MC-410 record had been treated as confidential while the unlawful detainer docket proceeded to default (R09, P&A, p. 11)."),

    ("chk", "Answer dated May 17, 2026 (R09); clerk's June 10 letter; MC-410 pending (R08 ¶¶ 6, 10).", 'A docket entry for the Answer; any notice to defendant that default would be sought.', 'Treat the Answer as tendered before default for purposes of § 585 and § 473(d).'),

    ("h3", "E. Service of the summons by posting (R02, R05)"),
    ("n", f"On May 19, 2026 \u2014 two days after the Answer was dated \u2014 plaintiff applied ex parte for an order permitting service of the summons by posting under "
          f"Code of Civil Procedure section 415.45 ({fr('F6')}), supported by declarations of counsel Charity Martinez and process server Joseph Falanga (R02 pp. 2\u20135). "
          f"Section 415.45 is available only on a showing of reasonable diligence in attempting personal or substituted service. Plaintiff's counsel was at that moment "
          f"litigating against defendant in the related restraining-order matter in this courthouse and had his unit number, email and telephone number (R01 p. 1; Tab I)."),
    ("fig", "F6"),
    ("n", f"The only Proof of Service of Summons in the record names the party served as \u201cAll Unnamed Occupants\u201d and lists the Prejudgment Claim of Right of Possession "
          f"among the documents served ({fr('F7')}). It recites posting on Thursday, June 4, 2026 at 11:03 a.m. and certified mailing the same day, is signed June 12, 2026, "
          f"and was not filed until June 30, 2026 ({fr('F8')}). No proof of service of the summons on the named defendant, Donald Gillson, appears in the record. "
          f"A default cannot be entered against a defendant who has not been served (Code Civ. Proc., \u00a7\u00a7 415.45, subd. (c), 585, 1167)."),
    ("fig", "F7"),
    ("fig", "F8"),

    ("chk", 'Ex parte for posting two days after the Answer date (Fig. 6); POS-010 on “All Unnamed Occupants” only (Figs. 7–8).', 'Any proof of service of summons on Donald Gillson; any diligence addressed to his known email, phone or unit.', 'Find the summons unserved on the named defendant; the default void.'),

    ("h3", "F. Default and judgment entered the same day the proof of service was filed (R03, R04)"),
    ("n", f"On June 30, 2026 plaintiff filed the June 12 proof of service, a Request for Entry of Default, and a form of judgment; the clerk entered default \u201cas requested\u201d "
          f"and entered a clerk's judgment for possession, $0.00, that day ({fr('F9')}, {fr('F10')}). This followed the clerk's June 10 letter rejecting the default request as "
          f"incomplete (R08 \u00b6 6). The defect that made it incomplete on June 10 \u2014 the absence of a filed proof of service \u2014 was addressed by filing a proof of service on "
          f"the unnamed occupants, not on the defendant."),
    ("fig", "F9"),
    ("fig", "F10"),

    ("chk", 'Default, judgment and POS all entered June 30, 2026 (Figs. 8–10) after a June 10 rejection.', 'Cure of the June 10 defect as to the named defendant.', 'Set aside under § 473(d); alternatively § 473(b).'),

    ("h3", "G. Notice of entry, writ, and defendant's emergency application (R06\u2013R08)"),
    ("n", f"Plaintiff mailed Notice of Entry of Judgment on July 1, 2026 ({fr('F11')}; R06 p. 3) and the same day filed for a writ of possession (R07). Defendant, "
          f"receiving the notice by mail, filed an emergency ex parte application on July 7, 2026 to stay execution, recall the writ, set aside the default, and route the "
          f"MC-410 record for judicial review ({fr('F12')}; R08 pp. 1\u20133; R09)."),
    ("fig", "F11"),
    ("fig", "F12"),

    ("chk", 'Notice of entry mailed July 1 (Fig. 11); writ sought the same day (R07); emergency application July 7 (Fig. 12).', 'Any pause by plaintiff after receipt of the Answer or the rule 1.100 correspondence.', 'Weigh the race to the writ in the equities of forfeiture.'),

    ("h3", "H. The July 8, 2026 order (R10)"),
    ("n", f"The Court (Hon. Charles F. Haines) heard the application on July 7 and filed its order on July 8, 2026, served on both sides by the clerk ({fr('F13')}; R10 p. 3, Clerk's "
          f"Certificate of Mailing). The order treats defendant's July 7 papers as a Motion to Vacate Default and Default Judgment, sets the hearing for July 22, 2026, "
          f"fixes an opposition and reply schedule, and directs that the writ issued July 1, 2026 not be executed before July 22 ({fr('F14')}). The default was thereafter "
          f"set aside and the matter returned to the merits track; by order of August 27, 2026 the Court preserved defendant's affirmative defenses for trial (Tab K)."),
    ("fig", "F13"),
    ("fig", "F14"),
    ("n", "Defendant's index of irregularities (Tab B, item 20) identifies a July 2026 paper from plaintiff's firm bearing the signature block "
          "\u201cAttorneys for Defendant\u201d; the copy in defendant's possession is being conformed to the Court's file and will be lodged, and the item is not relied on in this statement until it is."),

    ("chk", 'Order of July 7/8: hearing set, writ stayed to July 22 (Figs. 13–14); defenses preserved Aug. 27 (Tab K).', "Nothing — this is the Court's own record.", 'Hold plaintiff to the orders already entered.'),

    ("h3", "I. October 2026: accommodation orders, medical status, and notice to counsel"),
    ("n", "The Court's rule 1.100 orders of July through October 2026 authorize defendant's remote appearance and written communication (Tab K). On October 30, 2026 defendant "
          "was treated in the John Muir Health Concord Emergency Department after a fall (CT head and cervical spine; acute cervical strain) and placed off work through "
          "November 3, 2026 with directed follow-up at David Grant USAF Medical Center on or about November 1, 2026; the record is lodged confidentially at Tab J under "
          "rule 1.100(c)(4). On October 31, 2026 defendant served plaintiff's counsel with a written notice identifying the service defects, the hearsay character of the "
          "\u201cstaff\u201d allegations, the retaliation sequence, and a preservation demand for the original notice, proof of service, access logs and camera footage (Tab I)."),

    ("chk", 'Rule 1.100 orders (Tab K); Oct. 30 ED record (Tab J); Oct. 31 notice and preservation demand (Tab I).', 'Any response from counsel to the preservation demand.', 'Continue accommodations; adverse inference if the demanded records are not produced.'),

    ("h3", "J. Addendum: threats of criminal referral, communication blocks, the service animal, and dependent-adult protections"),
    ("n", "Plaintiff's agents and counsel have threatened referral to the District Attorney over defendant's documentation of conditions and conduct in the building, "
          "characterizing it as unlawful recording (Tab I; Tab C, offer of proof). Every recording in this case was made in common areas or at defendant's own door, "
          "where no party had a reasonable expectation that the communication was confidential (Pen. Code, \u00a7 632, subd. (c)), and each is logged contemporaneously "
          "(Tab E). A threat of criminal process to deter a tenant from documenting habitability, retaliation and accommodation failures is itself retaliatory conduct "
          "(Civ. Code, \u00a7 1942.5, subd. (a)(5)) and bears on plaintiff's clean hands."),
    ("n", "Management blocked defendant's email channel \u2014 the accommodated channel \u2014 and declined delivery of his papers (Tab D, Ex. C; Tab I \u00a7 I). Counsel has since "
          "described defendant's filings as \u201cemails\u201d or a \u201cdata dump.\u201d The record distinguishes the two: informal correspondence went to management by email under the "
          "accommodation; every court paper was served through Rapid Legal, a registered third-party process server, with delivery manifests retained and cross-referenced "
          "to the Bates range of each document (Tab D, Ex. C), as Code of Civil Procedure section 1011 et seq. and rule 2.251 of the California Rules of Court permit. "
          "Blocking the agreed written channel and then relying on the volume of its use as grounds for eviction is a failure to accommodate (Gov. Code, \u00a7 12927, "
          "subd. (c)(1); 24 C.F.R. \u00a7 100.204) and a procedural default by the party that blocked it."),
    ("n", "Defendant's record-keeping is maintained through an external cognitive prosthetic: a Supabase-backed system that stores every communication, accommodation "
          "agreement and filing with a server-side timestamp, used to compensate for TBI- and PTSD-related memory impairment (Tab D, Ex. D). It is auxiliary aid and "
          "assistive technology within the meaning of the ADA (42 U.S.C. \u00a7 12103(1); 28 C.F.R. \u00a7\u00a7 35.104, 36.303) and is part of the accommodation the Court has "
          "recognized under rule 1.100 (Tab K). Plaintiff has characterized its output as \u201cAI hallucination.\u201d The Court is asked to rely on the source documents and "
          "timestamps, not on either side's characterization; each exhibit at Tab D and Tab L is paired with its source file and capture date so that any entry can be checked."),
    ("n", "Defendant's psychiatric service dog, Jaxx, is a medically prescribed assistance animal (Tab K; Tab J). Displacement of a tenant with TBI and PTSD from a fixed, "
          "accessible unit to a vessel moored in Vallejo, Solano County, where defendant has been forced to shelter during the pendency of this action, disrupts the "
          "animal's working environment and the tenant's care routine, and is part of the damages record (Tab D, Ex. E: mileage, fuel and transit logs between Vallejo "
          "and San Francisco since July 2026)."),
    ("n", "Defendant qualifies as a dependent adult within the meaning of Welfare and Institutions Code section 15610.23 and invokes the protections of the Elder Abuse and "
          "Dependent Adult Civil Protection Act against financial and psychological abuse by a housing provider that is also his clinical services provider "
          "(Welf. & Inst. Code, \u00a7\u00a7 15610.07, 15610.30, 15610.53). The same facts underlie the pending restraining-order matter CCH-26-589086 (R01 p. 33) and the "
          "BBS complaints at Tab M. These matters are placed in the Department 606 record so that the trial court has the complete context in which the April 8, 2026 notice issued."),

    ("chk", 'Threats of criminal referral; blocked communication channel; attacks on assistive technology; displacement to Vallejo (Tabs C, D, E, I).', 'Any lawful basis for the threatened referral; any individualized assessment of the service animal.', 'Treat the conduct as retaliation and as bearing on clean hands.'),

    ("phase", "PHASE 4 \u2014 IMPLEMENT"),
    ("h2", "IV. The Record Against Itself"),
    ("p", "The following representations in plaintiff's own papers are contradicted by other papers plaintiff filed, or by the absence of what plaintiff said it filed."),
    ("table", [
        ["Plaintiff's representation", "Where", "Contradicted by", "Where"],
        ["Tenancy is \u201cexempt\u201d from the SF Rent Ordinance", "Notice to Quit p. 3 (R01 p. 35; Fig. 2)", "Complaint pleads just-cause compliance for a subsidized tenancy", "Attachment 18 (R01 pp. 7\u20138)"],
        ["Nuisance consists of \u201cstaff harassment\u201d by unnamed staff", "Notice to Quit pp. 1\u20132 (R01 pp. 33\u201334)", "Grounds actually listed: the RO petition and the volume of accommodated emails", "R01 p. 33 (Fig. 1)"],
        ["Notice posted and mailed 4/8/2026 because no suitable person could be found", "UD-100 item 10 (R01 p. 5; Fig. 3)", "Defendant in residence and in daily written contact; executing employee's presence disputed; no Exhibit 3 in the filed complaint", "R01 pp. 36\u201358; Tab I \u00a7 II"],
        ["Proof of service of notice \u201cattached and labeled Exhibit 3\u201d", "UD-100 item 10d (R01 p. 5)", "No page labeled Exhibit 3 in R01", "R01, all 58 pages (Tab H)"],
        ["Reasonable diligence justified service by posting", "Ex parte application 5/19/2026 (R02; Fig. 6)", "Counsel simultaneously litigating against defendant in CCH-26-589086 with his address, email and phone", "R01 p. 1; Tab I; Tab K"],
        ["Summons served on defendant", "Request for Entry of Default (R03; Fig. 9)", "Only POS-010 names \u201cAll Unnamed Occupants\u201d", "R05 p. 1 (Fig. 7)"],
        ["Default properly entered 6/30/2026", "R03, R04 (Figs. 9\u201310)", "Clerk rejected default 6/10/2026 as incomplete; Answer dated 5/17/2026 tendered; MC-410 pending", "R08 \u00b6\u00b6 6, 10; R09"],
        ["Writ may be executed on the June 30 judgment", "Writ request 7/1/2026 (R07)", "Court: writ \u201cshall not be executed prior to July 22, 2026\u201d; default thereafter set aside", "R10 p. 2 (Fig. 14); Tab K"],
        ["Eviction is for \u201cthe way that staff was treated\u201d", "Counsel's statement (Tab I \u00a7 III)", "No incident report, warning or notice to cure; sole dispute was with Mr. Landrum, who caused the notice to issue", "Tab I \u00a7 III; Tab C"],
        ["Defendant's filings are \u201cemails\u201d or a \u201cdata dump\u201d", "Counsel's characterization (Tab I)", "Court papers served via Rapid Legal (CCP \u00a7 1011; CRC 2.251) with manifests cross-referenced to Bates ranges; email limited to the rule 1.100 channel", "Tab D Ex. C; Tab K"],
    ], [1.9 * inch, 1.35 * inch, 2.0 * inch, 1.25 * inch]),

    ("phase", "PHASE 5 \u2014 EVALUATE"),
    ("h2", "V. Issues for Trial and Relief Requested"),
    ("n", "(1) Whether the April 8, 2026 notice states a nuisance with the particularity section 1161(4) requires, or instead names protected activity as its grounds. "
          "(2) Whether the notice was served as section 1162 requires, given the disputed presence of the executing employee and the missing Exhibit 3. "
          "(3) Whether the summons was ever served on the named defendant. (4) Whether the action is barred as retaliatory under Civil Code section 1942.5 and Government "
          "Code section 12955(f), the notice having issued within 180 days of defendant's accommodation request and restraining-order petition. (5) Whether plaintiff, "
          "having accepted rent and continued the subsidy after the alleged conduct, waived the forfeiture. (6) Whether plaintiff comes to equity with clean hands."),
    ("n", "Defendant asks that judgment be entered for defendant on the complaint; alternatively that the notice be found defective and the action dismissed without "
          "prejudice to a new notice that complies with sections 1161 and 1162 and Civil Code section 1946.2; that the Court find the action retaliatory within the meaning "
          "of Civil Code section 1942.5 and award the statutory remedies; that plaintiff's unanswered preservation demand (Tab I \u00a7 II) support an adverse inference "
          "as to the original notice, proof of service, access logs and camera footage; and that the accommodations ordered under rule 1.100 remain in force for all "
          "further proceedings."),
]


# ------------------------------------------------------------------ renderers
def fig_flowable(figs, key):
    path, w, h, cap = figs[key]
    maxw = TEXT_W - 8; maxh = 5.6 * inch
    scale = min(maxw / w, maxh / h); iw, ih = w * scale, h * scale
    img = RLImage(path, width=iw, height=ih)
    box = Table([[img]], colWidths=[iw + 8]); box.setStyle(figbox)
    box.hAlign = "CENTER"
    return KeepTogether([Spacer(1, 4), box, P(f"<b>{fr(key)}.</b> {cap}", capstyle)])


def chk_flowable(shown, missing, asked):
    rows = [[P("<b>CHECK-<br/>POINT</b>", chkstyle), P("<b>Record shows</b>", chkstyle), P("<b>Record omits</b>", chkstyle), P("<b>Asked of the Court</b>", chkstyle)],
            ["", P(shown, chkstyle), P(missing, chkstyle), P(asked, chkstyle)]]
    t = Table(rows, colWidths=[1.0 * inch, 1.9 * inch, 1.8 * inch, 1.8 * inch]); t.setStyle(chkbox)
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def build_pdf(figs, path):
    f = caption("DEFENDANT'S INTEGRATED STATEMENT OF THE CASE (WITH THE RECORD EMBEDDED)")
    n = 0
    for item in CONTENT:
        kind = item[0]
        if kind == "h2":
            f.append(P(item[1], h2))
        elif kind == "h3":
            f.append(P(item[1], h3))
        elif kind == "p":
            f.append(P(item[1], body))
        elif kind == "n":
            n += 1
            f.append(P(f"{n}. {item[1]}", body))
        elif kind == "fig":
            f.append(fig_flowable(figs, item[1]))
        elif kind == "phase":
            f.append(P(item[1], phase))
        elif kind == "chk":
            f.append(chk_flowable(*item[1:]))
        elif kind == "table":
            f.append(Spacer(1, 6)); f.append(grid(item[1], item[2])); f.append(Spacer(1, 8))
    f.append(P("PHASE 2 \u2014 DESIGN (how to verify any sentence above)", phase))
    f.append(P("VI. Figure and Record Cross-Reference", h2))
    rows = [["Fig.", "Record cite (Tab H)", "What it shows"]]
    for key, src, pg, _, cap in FIGS:
        code = os.path.basename(src)[:3]
        rows.append([str(FIG_NO[key]), f"{code} p. {pg}", cap.split(" \u2014 ", 1)[1] if " \u2014 " in cap else cap])
    f.append(grid(rows, [0.5 * inch, 1.2 * inch, 4.8 * inch]))
    f.append(Spacer(1, 10))
    f.append(P("Verification", h2))
    f.append(P("I am the defendant. I have read the foregoing statement. The facts stated are true of my own knowledge except where stated on the record cited, "
               "which I have reviewed and which I believe to be accurately described. I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct.", body))
    f += signature()
    return rl(f, path, "Integrated Statement of the Case")


def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t)


def build_docx(figs, path):
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(BODY_PT)
    d.styles["Heading 1"].font.size = Pt(H2_PT); d.styles["Heading 2"].font.size = Pt(H3_PT)
    for s in d.sections:
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
    for line in [NAME, A.ADDR1, A.ADDR2, f"{A.PHONE} | {A.EMAIL}", "Defendant, in propria persona"]:
        p = d.add_paragraph(line); p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()
    p = d.add_paragraph(COURT.upper()); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t = d.add_table(rows=1, cols=2); t.style = "Table Grid"
    t.cell(0, 0).text = "SWORDS TO PLOWSHARES,\n\tPlaintiff,\nv.\nDONALD ERNEST GILLSON, Ed.D. (Dr. Donny Gillson), and all unnamed occupants,\n\tDefendant."
    t.cell(0, 1).text = f"Case No. {CASE_NO}\n{DEPT}\n{TRIAL}\n\nDEFENDANT'S INTEGRATED STATEMENT OF THE CASE (WITH THE RECORD EMBEDDED)"
    d.add_paragraph()
    n = 0
    for item in CONTENT:
        kind = item[0]
        if kind == "h2":
            d.add_heading(strip_tags(item[1]), level=1)
        elif kind == "h3":
            d.add_heading(strip_tags(item[1]), level=2)
        elif kind == "p":
            p = d.add_paragraph(strip_tags(item[1])); p.paragraph_format.line_spacing = 1.5
        elif kind == "n":
            n += 1
            p = d.add_paragraph(f"{n}. {strip_tags(item[1])}"); p.paragraph_format.line_spacing = 1.5
        elif kind == "phase":
            pp = d.add_paragraph(); rr = pp.add_run(strip_tags(item[1])); rr.font.size = Pt(9.5); rr.bold = True
        elif kind == "chk":
            tb = d.add_table(rows=2, cols=4); tb.style = "Table Grid"
            for j, hdr in enumerate(["CHECKPOINT", "Record shows", "Record omits", "Asked of the Court"]):
                tb.cell(0, j).text = hdr
            for j, val in enumerate(["", item[1], item[2], item[3]]):
                tb.cell(1, j).text = val
            for row in tb.rows:
                for c in row.cells:
                    for pp in c.paragraphs:
                        for rr in pp.runs:
                            rr.font.size = Pt(10); rr.bold = (row is tb.rows[0])
            d.add_paragraph()
        elif kind == "fig":
            fp, w, h, cap = figs[item[1]]
            width = min(6.3, 6.3 * (w / h) / (6.3 / 5.5)) if h > w else 6.3
            d.add_picture(fp, width=Inches(width))
            d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            c = d.add_paragraph(); r = c.add_run(f"{fr(item[1])}. "); r.bold = True; r.font.size = Pt(9.5)
            r2 = c.add_run(cap); r2.font.size = Pt(9.5)
        elif kind == "table":
            rows = item[1]; tb = d.add_table(rows=len(rows), cols=len(rows[0])); tb.style = "Table Grid"
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    tb.cell(i, j).text = strip_tags(val)
                    for pp in tb.cell(i, j).paragraphs:
                        for rr in pp.runs:
                            rr.font.size = Pt(9.5); rr.bold = (i == 0)
            d.add_paragraph()
    d.add_heading("VI. Figure and Record Cross-Reference", level=1)
    tb = d.add_table(rows=1, cols=3); tb.style = "Table Grid"
    for j, hdr in enumerate(["Fig.", "Record cite (Tab H)", "What it shows"]):
        tb.cell(0, j).text = hdr
    for key, src, pg, _, cap in FIGS:
        r = tb.add_row().cells; r[0].text = str(FIG_NO[key]); r[1].text = f"{os.path.basename(src)[:3]} p. {pg}"
        r[2].text = cap.split(" \u2014 ", 1)[1] if " \u2014 " in cap else cap
    for row in tb.rows:
        for c in row.cells:
            for pp in c.paragraphs:
                for rr in pp.runs:
                    rr.font.size = Pt(9.5)
    d.add_heading("Verification", level=1)
    d.add_paragraph("I am the defendant. I have read the foregoing statement. The facts stated are true of my own knowledge except where stated on the record cited, "
                    "which I have reviewed and which I believe to be accurately described. I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct.")
    d.add_paragraph(f"Dated: {DATED}")
    d.add_paragraph("\n______________________________\n" + NAME + "\nDefendant, in propria persona")
    d.save(path)
    return path


if __name__ == "__main__":
    figs = render_figs()
    contact_sheet(figs, "/tmp/aio/fig_sheet.png")
    if "--figs-only" in sys.argv:
        print("figs rendered"); sys.exit(0)
    print("statement pdf"); build_pdf(figs, OUT_PDF)
    print("statement docx"); build_docx(figs, OUT_DOCX)
    if "--no-binder" in sys.argv:
        sys.exit(0)
    # full binder with the integrated statement as Tab A
    from build import CATEGORIES
    from build_binders import WITNESSES, ADA_EXHIBITS, make_mc410, make_subpoena, medical_exhibit, compress_scans
    photo_counts = {l: len(items) for l, _, items in CATEGORIES}
    tabA = OUT_PDF
    tabB = A.irregularities(os.path.join(TMP, "int_B.pdf")); tabC = A.witness_list(os.path.join(TMP, "int_C.pdf"))
    tabD = A.evidence_list(os.path.join(TMP, "int_D.pdf"), photo_counts); tabE = A.video_list(os.path.join(TMP, "int_E.pdf"))
    tabF = A.points_authorities(os.path.join(TMP, "int_F.pdf")); tabG = A.closing(os.path.join(TMP, "int_G.pdf"))
    med_ex = medical_exhibit(os.path.join(TMP, "int_medical_exhibit.pdf"))
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} \u2014 {DEPT}",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further hearings in this case.", "Defendant", "Unlawful detainer",
                       "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    mc_sf_merged = A.merge(mc_sf, os.path.join(TMP, "int_mc_sf.pdf"))
    sub_items = []
    for w in WITNESSES:
        sub_items.append((f"Civil Subpoena (Duces Tecum) \u2013 {w['name']}", A.merge(make_subpoena(w), os.path.join(TMP, f"int_subp_{w['tag']}.pdf"))))
    svc_rows = [["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY", h1), grid(svc_rows, [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "int_svc.pdf"))
    ada_items = [(f"Ex. {i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]
    filing_items = [(f"{code} \u2013 {dt} \u2013 {desc}", os.path.join(FIL, fn)) for code, dt, desc, fn in FILINGS]
    sections = [
        ("A", "Integrated Statement of the Case (record embedded, 14 figures)", [("Defendant's Integrated Statement of the Case", tabA)]),
        ("B", "Index of Record Irregularities and Indicia of Fraud", [("Line-by-line index", tabB)]),
        ("C", "Witness List", [("Witness list and offer of proof", tabC)]),
        ("D", "Evidence List", [("Exhibit and evidence list", tabD)]),
        ("E", "Video List", [("Audio-visual exhibit list", tabE)]),
        ("F", "Points and Authorities", [("Memorandum with table of authorities", tabF)]),
        ("G", "Closing Argument", [("Closing argument outline", tabG)]),
        ("H", "The Filed Court Record (R01\u2013R10)", filing_items),
        ("I", "Notice to Counsel and Civil Subpoenas",
         [("Notice to Francisco Torres, Esq., October 31, 2026", os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")),
          ("Service directory", svc)] + sub_items),
        ("J", "Request for Accommodations \u2013 MC-410 \u2013 CONFIDENTIAL IN PART",
         [("MC-410 with Attachment", mc_sf_merged), ("CONFIDENTIAL Exhibit \u2013 John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
        ("K", "Rule 1.100 Orders and Responses of this Court", ada_items),
        ("L", "Evidence Exhibit Binder \u2013 Photographs, Notices, Agency Records",
         [("Gillson Evidence Exhibit Binder", os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
        ("M", "Related Administrative Complaints",
         [("BBS Complaint 2002026002097 \u2013 Kolby Losik", os.path.join(COMP, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
          ("BBS Complaint 2002026002098 \u2013 Mark Villalobos", os.path.join(COMP, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))]),
    ]
    cov = A.cover(os.path.join(TMP, "int_cover.pdf"))
    A.PREFIX = "AIO"
    n = A.assemble(OUT_BINDER, cov, sections, "Gillson \u2013 Master Trial Binder (Integrated) \u2013 CUD-26-682107 \u2013 Tab J confidential in part (CRC 1.100(c)(4))")
    print("binder pages", n)
    compress_scans(OUT_BINDER)
