"""FINAL: two all-in-one binders (San Francisco trial binder; Solano County binder).

Changes from the prior builds, per client instruction:
  * The Statement of the Case embeds the key record pages as numbered Record Exhibits (RX-1 ...) so each
    finding is shown and cited in place, instead of reproducing the 290-page filed record in full.
  * Tab H is now "Record Excerpts" (key pages only).  Full filings remain available on request.
  * Video evidence moved to Tab B and summarized inside the Statement.
  * New sections: hypocrisy / fraud on the court / dependent-adult abuse; fiduciary failures (landlord,
    agents, counsel); expanded Points and Authorities with case table; public-integrity context.
  * Redundant items removed (the Oct. 30 CamScanner ED pages duplicate the medical exhibit already in Tab J).
"""
import os, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer, Image, KeepTogether, PageBreak, Table, TableStyle
from reportlab.lib import colors

import build_allinone as A
from build_allinone import (P, rl, caption, grid, signature, h1, h2, h3, cen, small, cell, cellb, cellurl, quote,
                            assemble, merge, TMP, ART, COMP, FIL, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED, CASE, CASE_NO, COURT, DEPT, TRIAL)
from build_binders import make_mc410, make_subpoena, medical_exhibit, ADA_EXHIBITS, WITNESSES, compress_scans
from notices import NOTICES

HERE = os.path.dirname(os.path.abspath(__file__))
INC = os.path.join(HERE, "incoming")
OUT_SF = os.path.join(ART, "Gillson_FINAL_All_In_One_Trial_Binder_SAN_FRANCISCO_CUD-26-682107.pdf")
OUT_SOL = os.path.join(ART, "Gillson_FINAL_All_In_One_Binder_SOLANO_COUNTY.pdf")

R = {c: os.path.join(FIL, fn) for c, _, _, fn in A.FILINGS}
EXP = os.path.join(INC, "10224145.pdf")  # clean copy of the May 19, 2026 ex parte application (R02)

figcap = ParagraphStyle("figcap", parent=small, fontName="Times-Italic", fontSize=10, leading=14, spaceBefore=4, spaceAfter=10)

# ------------------------------------------------------------------ Record Exhibits embedded in the Statement
# (id, source pdf, 1-based page, crop (top, bottom) as fraction of page height, caption)
RX = [
    ("RX-1", R["R01"], 7, (0.03, 0.78),
     "Complaint, Attachment 18 (filed May 5, 2026). Plaintiff pleads that the lease \"contains a typographic error\" (¶ 18-3), that the HUD "
     "addenda \"were not attached\" and \"cannot be located\" (¶ 18-2), and that the Notice to Quit was \"submitted\" to the Rent Board and "
     "Housing Authority (¶¶ 18-5, 18-6). Plaintiff's own pleading admits an incomplete federal tenancy file."),
    ("RX-2", R["R01"], 33, (0.05, 0.80),
     "Notice to Quit, page 1 (April 8, 2026). The stated grounds are the volume of defendant's written communications and his February 25, 2026 "
     "petition for a restraining order (Case No. CCH-26-589086) – i.e., protected petitioning and protected complaints (Civ. Code, §§ 47(b), "
     "1942.5(a), (d))."),
    ("RX-3", R["R01"], 35, (0.03, 0.62),
     "Notice to Quit, page 3, signed by Jerome Bradford for Swords to Plowshares on April 8, 2026, with the HUD VAWA notice and the San Francisco "
     "eviction-prevention information attached – the plaintiff invokes federal tenant protections in the same breath that it terminates a "
     "HUD-VASH veteran's tenancy for sending e-mails."),
    ("RX-4", EXP, 2, (0.04, 0.68),
     "Declaration of Charity Martinez, Esq. (SBN 367234), filed May 19, 2026 (R02). Counsel declares under penalty of perjury that \"more than "
     "three attempts have been made\" and that defendant \"failed to answer the door,\" relying on the attached Falanga declaration."),
    ("RX-5", EXP, 4, (0.28, 0.86),
     "Falanga declaration (Exhibit 1 to R02), party: Donald Gilson [sic]. Four attempts are recited; the fourth is \"May 12, 2026, 6:06 PM.\" "
     "The declaration is dated and signed \"5/11/2026\" – one day before the event it swears to. Joseph Falanga, Spirit Courier, "
     "S.F. Reg. No. 1539."),
    ("RX-6", EXP, 5, (0.28, 0.86),
     "Second Falanga declaration (same Exhibit 1), party: \"All Unnamed Occupants.\" Identical attempts, identical impossibility: signed "
     "5/11/2026 while reciting a May 12, 2026 attempt. Two sworn statements, both facially false as to date."),
    ("RX-7", R["R05"], 1, (0.03, 0.62),
     "Proof of Service of Summons (POS-010) filed June 30, 2026 (R05). The only POS-010 in the record names \"All Unnamed Occupants\" as the "
     "party served. No proof of service on Donald Ernest Gillson was ever filed."),
    ("RX-8", R["R03"], 1, (0.03, 0.55),
     "Request for Entry of Default, stamped \"DEFAULT ENTERED AS REQUESTED\" on June 30, 2026 (R03), while defendant's Rule 1.100 request "
     "(MC-410) was pending with the Court's ADA Coordinator under written assurances that \"no further action is required.\""),
    ("RX-9", R["R04"], 1, (0.03, 0.70),
     "Judgment – Unlawful Detainer (UD-110), clerk's judgment by default entered June 30, 2026 (R04): possession only, $0.00, on a proof of "
     "service that does not name the defendant."),
    ("RX-10", R["R10"], 1, (0.02, 0.40),
     "Points and Authorities filed July 8, 2026 by Zanghi Torres Adams LLP, captioned \"Attorneys for Defendant\" (R10). Plaintiff's firm filed a "
     "pleading in the defendant's name – a recycled-form admission of the care taken with this record."),
]


def fig(rx_id, src, page, crop, cap, width=6.3 * inch):
    d = fitz.open(src); pg = d[page - 1]; r = pg.rect
    clip = fitz.Rect(r.x0, r.y0 + r.height * crop[0], r.x1, r.y0 + r.height * crop[1])
    pix = pg.get_pixmap(dpi=120, clip=clip)
    png = os.path.join(TMP, f"fig_{rx_id}.png"); pix.save(png); d.close()
    h = width * pix.height / pix.width
    maxh = 6.6 * inch
    if h > maxh:
        width = width * maxh / h; h = maxh
    img = Image(png, width=width, height=h)
    frame = Table([[img]], colWidths=[width + 8])
    frame.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.75, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return KeepTogether([frame, P(f"<b>Record Exhibit {rx_id}.</b> {cap}", figcap)])


RXMAP = {r[0]: r for r in RX}


def RXF(rx_id):
    return fig(*RXMAP[rx_id])


# ------------------------------------------------------------------ TAB A: Statement of the Case (final, consolidated)
def statement_of_case(path):
    f = caption("DEFENDANT'S MASTER STATEMENT OF THE CASE WITH EMBEDDED RECORD EXHIBITS")
    f.append(P("Record Exhibits RX-1 through RX-10 reproduced below are true copies of pages from the Court's own file (Evid. Code, §§ 452(d), 453). "
               "Tab H contains the excerpted record pages in full size; the complete filings are available on request. Citations to \"V-\" exhibits "
               "refer to the audio-visual exhibits at Tab B; \"GILLSON-\" Bates numbers refer to the Evidence Exhibit Binder at Tab L.", small))

    f.append(P("I. Nature of the Action and Why the Judgment Cannot Stand", h2))
    f.append(P(
        f"This is a summary unlawful detainer action by Swords to Plowshares, a veterans' services nonprofit, to remove a 90% service-connected disabled "
        "U.S. Navy veteran with traumatic brain injury, PTSD, mild cognitive impairment and Parkinsonism from Unit 301A at 1030 Girard Road in the Presidio "
        "(Jon W. Paulson Veterans Community), a HUD-VASH permanent supportive housing placement funded under 42 U.S.C. § 1437f(o)(19) and governed by "
        "24 C.F.R. part 982. Defendant appears in propria persona. The clerk's default judgment of June 30, 2026 rests on (1) a non-curable notice whose "
        "stated grounds are protected activity; (2) sworn diligence declarations that are impossible on their face; (3) a proof of service that never "
        "names the defendant; and (4) a default taken while the Court's own ADA Coordinator had the defendant's accommodation request under review and "
        "had told him in writing that no further action was required. Each defect is shown below from the record itself."))

    f.append(P("II. The Parties and Their Duties", h2))
    f.append(P(
        "Plaintiff is not an ordinary landlord. It is a VA-accredited veterans service organization and the HUD-VASH housing provider and supportive-services "
        "agency for the premises; it receives federal subsidy for the unit and holds itself out as the veteran's advocate. Its agents include William Landrum "
        "(Assistant Property Manager), Jerome Bradford (signatory of the Notice to Quit), Kobe/Kolby Losik and Mark Villalobos (clinical staff, subjects of "
        "Board of Behavioral Sciences complaints Nos. 2002026002097 and 2002026002098, Tab M), Joel Champion (management; party to the December 23, 2025 "
        "accommodation consensus), Bradley White (fiduciary/signatory), and resident advisor \"Dwayne.\" Its counsel are John P. Zanghi (SBN 145845), Charity "
        "Martinez (SBN 367234) and Francisco G. Torres of Zanghi Torres Adams LLP. Under Civil Code sections 2330 and 2338 the acts and declarations of these "
        "agents within the scope of their agency are plaintiff's acts. Defendant is a \"dependent adult\" within Welfare and Institutions Code section 15610.23, "
        "and plaintiff, as a supportive-housing provider rendering care and services to him, is a \"care custodian\" within section 15610.17."))

    f.append(P("III. Tenancy, Habitability and Protected Activity (2025)", h2))
    f.append(P(
        "The occupancy agreement for Unit 301A was executed January 9, 2025 (the complaint pleads January 9, 2024 and then admits the date is a \"typographic "
        "error,\" RX-1). Tenant rent share was $1,189, later $1,126; the HUD-50059, emergency-contact and accessible-unit addenda were never appended and, by "
        "plaintiff's own pleading, \"cannot be located\" (RX-1). From late 2025 the unit suffered a severe German cockroach infestation, plumbing defects, "
        "dampness and mold (photographs GILLSON- Category B; V-02 \"Habitability Collapse\"). Management's response was repeated chemical application in a "
        "small unventilated unit rather than integrated pest management; defendant sustained contact dermatitis and chemical burns, and his psychiatric "
        "service dog Jaxx was injured (Category C; V-03). Defendant's written grievances and maintenance requests of November 16, 2025 (Category A), his "
        "November 20, 2025 reasonable-accommodation request for cognitive-prosthetic communication (written, e-mail-only protocol), his 311/DPH complaint "
        "(Case 101003004371, Category F), the December 5, 2025 Adult Protective Services letter, and the January 2, 2026 BBS complaints are each protected "
        "activity under Civil Code section 1942.5 and San Francisco Administrative Code section 37.9(f). Every one of them precedes the April 8, 2026 notice "
        "and falls inside the 180-day presumption period."))
    f.append(RXF("RX-1"))

    f.append(P("IV. Retaliation Chronology (December 2025 – April 2026)", h2))
    rows = [["Date", "Event", "Source"],
            ["Dec. 23, 2025", "Reasonable-accommodation consensus (Gillson / Champion / Losik): written e-mail protocol for TBI/PTSD.", "Testimony; Ex. A (user binder)"],
            ["Jan. 2, 2026", "Losik: \"stop with the f---ing e-mails, or else.\" Same day: plaintiff's rent letter; defendant files BBS complaints.", "V-01 (suite 2); Cat. E; Tab M"],
            ["Jan. 3, 2026", "Landrum confrontation; hostile posturing and verbal abuse at the unit.", "V-01, V-04 (suite 2)"],
            ["Feb. 25, 2026", "Defendant petitions for restraining order against Landrum (CCH-26-589086).", "Court file"],
            ["Mar. 19, 2026", "Hearing; tenant witnesses testify; petition dismissed without prejudice. Adverse notices then issued to the witnesses.", "Court file; testimony"],
            ["Apr. 8, 2026", "Non-curable Notice to Quit; grounds = communications and the restraining-order petition.", "RX-2, RX-3"],
            ["May 5, 2026", "Complaint filed; HUD addenda admittedly missing; lease date wrong.", "RX-1"]]
    f.append(grid(rows, [1.0 * inch, 3.7 * inch, 1.8 * inch]))
    f.append(Spacer(1, 8))
    f.append(RXF("RX-2"))
    f.append(RXF("RX-3"))

    f.append(P("V. The Notice Is Void: Protected Activity Is Not \"Nuisance\"", h2))
    f.append(P(
        "A notice terminating a subsidized tenancy must state good cause with specificity (24 C.F.R. § 982.310(e); S.F. Admin. Code, § 37.9(c)) and is "
        "strictly construed (Kwok v. Bergren (1982) 130 Cal.App.3d 596, 599-600; Bevill v. Zoura (1994) 27 Cal.App.4th 694, 697). The notice here states "
        "two grounds: that defendant wrote too much, and that he petitioned the court for protection. Petitioning is absolutely privileged (Civ. Code, § 47(b)) "
        "and may not be the basis of a landlord's adverse action (Civ. Code, § 1942.5(d); Barela v. Superior Court (1981) 30 Cal.3d 244, 250-253). A notice "
        "whose only grounds are protected acts states no cause at all and cannot support the summary remedy (Delta Imports, Inc. v. Municipal Court (1983) "
        "146 Cal.App.3d 1033, 1036). The same notice attached the HUD VAWA notice and the City's eviction-prevention information (RX-3): plaintiff knew the "
        "federal and local protections and invoked them as boilerplate while violating them in substance."))

    f.append(P("VI. Service Fraud and Void Jurisdiction", h2))
    f.append(P(
        "On May 19, 2026 plaintiff's counsel applied ex parte for posting-and-mailing service under Code of Civil Procedure section 415.45 (R02; clean copy "
        "RX-4 to RX-6). Counsel's declaration swears that more than three attempts were made (RX-4). The attached declarations of registered process server "
        "Joseph Falanga are each dated and signed May 11, 2026 yet recite a fourth attempt on May 12, 2026 at 6:06 p.m. (RX-5, RX-6). A declaration cannot "
        "truthfully attest to an event that has not occurred; the statutory presumption that attaches to a registered process server's return (Evid. Code, "
        "§ 647) is rebutted by the document itself. Facility resident-advisor logs show no entry by Falanga on May 6, 8, 10 or 12 (testimony of \"Dwayne\"; "
        "V-03, V-05). The door was accessible and the resident advisor accepted other papers (V-05 \"Accidental Legal Service\"). Section 415.45 permits "
        "posting only on a showing that personal or substitute service \"cannot with reasonable diligence\" be made; three or four same-address knocks with "
        "no attempt at the workplace, no inquiry of on-site staff, and a false date do not meet that standard (Bein v. Brechtel-Jochim Group, Inc. (1992) "
        "6 Cal.App.4th 1387, 1391-1392; Watts v. Crawford (1995) 10 Cal.4th 743, 749, fn. 5). Posting on an apartment door is, in any event, a constitutionally "
        "disfavored method in eviction cases (Greene v. Lindsey (1982) 456 U.S. 444, 453-455)."))
    f.append(RXF("RX-4"))
    f.append(RXF("RX-5"))
    f.append(RXF("RX-6"))
    f.append(P(
        "The only proof of service ever filed (June 30, 2026, RX-7) names \"All Unnamed Occupants.\" No return of service on Donald Ernest Gillson exists. "
        "A default entered without a filed proof of service on the defaulting party is void, not merely voidable (Code Civ. Proc., §§ 585, 1169; Dill v. "
        "Berquist Construction Co. (1994) 24 Cal.App.4th 1426, 1439-1444; Kremerman v. White (2021) 71 Cal.App.5th 358, 371-372), and a judgment resting "
        "on a false return is subject to attack at any time as extrinsic fraud (County of San Diego v. Gorham (2010) 186 Cal.App.4th 1215, 1228-1231; "
        "Peralta v. Heights Medical Center, Inc. (1988) 485 U.S. 80, 84-87). Service by posting and mailing was in no event complete before June 15, 2026; "
        "with the Juneteenth holiday the responsive period had not run when default was requested."))
    f.append(RXF("RX-7"))

    f.append(P("VII. The Disability Default Trap (Rule 1.100)", h2))
    f.append(P(
        "Defendant's Answer is dated May 17, 2026 (R09). On June 1, 2026 the Court's ADA Coordinator, Joy Guandique, confirmed receipt of defendant's "
        "MC-410 and fourteen supporting filings, advised that the matter was confidential and under review, and stated that no further action was required; "
        "court administration repeated on June 10, 2026: \"At this time, no further action is required on your part.\" Relying on those written directives "
        "from the Court, defendant did not separately file on the public docket. On June 30, 2026 – the earliest arguable day – plaintiff requested and the "
        "clerk entered default and a possession-only judgment (RX-8, RX-9). A default obtained while the defendant is following the Court's own "
        "instructions is the paradigm of extrinsic mistake (Rappleyea v. Campbell (1994) 8 Cal.4th 975, 981-984), and the failure to rule on a pending "
        "rule 1.100 request before taking dispositive action is itself reversible error (Biscaro v. Stern (2010) 181 Cal.App.4th 702, 708-711; Vesco v. "
        "Superior Court (2013) 221 Cal.App.4th 275, 282-284). Counsel who knows an opposing party is unrepresented, disabled and actively engaged with the "
        "court has an ethical duty to warn before seeking default (Fasuyi v. Permatex, Inc. (2008) 167 Cal.App.4th 681, 701-702; Lasalle v. Vogel (2019) "
        "36 Cal.App.5th 127, 135-137). None was given."))
    f.append(RXF("RX-8"))
    f.append(RXF("RX-9"))

    f.append(P("VIII. Binding Prior Orders and Coordinate Jurisdiction", h2))
    f.append(P(
        "On July 7-8, 2026 the Hon. Charles F. Haines (Dept. 501) stayed execution of the July 1 writ, set the motion to vacate for hearing and fixed a "
        "briefing schedule (R08, R10). On August 27, 2026 Judge Haines denied plaintiff's motion to strike and expressly preserved Affirmative Defenses "
        "No. 5 (retaliation, Civ. Code, § 1942.5) and No. 9 (breach of the implied warranty of habitability). Between July 20 and October 14, 2026 this "
        "Court issued twenty rule 1.100 responses and orders (Tab K). After reassignment to Department 606, those orders were treated orally as if they "
        "did not exist. One department of the superior court may not nullify the ruling of another on the same matter except through the procedures of "
        "Code of Civil Procedure section 1008 (In re Alberto (2002) 102 Cal.App.4th 421, 427-430; Ford v. Superior Court (1986) 188 Cal.App.3d 737, 742; "
        "Williams v. Superior Court (1939) 14 Cal.2d 656, 662; see Le Francois v. Goel (2005) 35 Cal.4th 1094, 1107-1108). The Haines orders are the law "
        "of this case."))

    f.append(P("IX. Hypocrisy, Fraud on the Court, and Abuse of a Dependent Adult", h2))
    f.append(P(
        "<b>Hypocrisy.</b> Plaintiff's mission, funding and accreditation exist to keep disabled veterans housed. It accepted federal HUD-VASH subsidy for this "
        "unit, pleaded that it cannot find the HUD documents that condition that subsidy (RX-1), attached HUD's own tenant-protection notice to a termination "
        "whose stated cause is the tenant's protected speech (RX-2, RX-3), and then told this Court that the tenant's written requests for accommodation are a "
        "\"data dump.\" Its staff told residents it would \"kick their ass\" (V-04, V-06, suite 2); its clinician told a brain-injured veteran to stop with "
        "the e-mails \"or else\" (V-01, suite 2)."))
    f.append(P(
        "<b>Fraud on the court.</b> Fraud on the court is conduct by a party or counsel that corrupts the judicial process itself – false sworn statements "
        "used to obtain relief ex parte, concealment of material facts from the tribunal, or procuring judgment by preventing the adversary from being heard "
        "(Hazel-Atlas Glass Co. v. Hartford-Empire Co. (1944) 322 U.S. 238, 245-246; Kulchar v. Kulchar (1969) 1 Cal.3d 467, 471-473; In re Marriage of "
        "Stevenot (1984) 154 Cal.App.3d 1051, 1068-1069). The record shows each element: a counsel declaration vouching for diligence declarations that are "
        "false on their face (RX-4 to RX-6); an ex parte order obtained on them; a proof of service that never names the defendant (RX-7); a default taken "
        "while the defendant was following the Court's written instructions (RX-8); a notice of entry misstating the period for relief (R06); and a pleading "
        "filed by plaintiff's firm as \"Attorneys for Defendant\" (RX-10). Attorneys may never seek to mislead a judge by an artifice or false statement of "
        "fact (Bus. & Prof. Code, § 6068(d); Rules Prof. Conduct, rules 3.3, 4.1, 8.4(c)), and a court has inherent power to set aside what such conduct "
        "produced (Code Civ. Proc., § 473(d); Kim v. Westmoore Partners, Inc. (2011) 201 Cal.App.4th 267, 281-282, 288-290)."))
    f.append(RXF("RX-10"))
    f.append(P(
        "<b>Dependent-adult abuse.</b> Defendant is a dependent adult (Welf. & Inst. Code, § 15610.23). \"Abuse\" includes isolation, the deprivation by a care "
        "custodian of goods or services necessary to avoid physical harm or mental suffering, and financial abuse (§§ 15610.07, 15610.30, 15610.43). "
        "Wrongful use of legal process to take a dependent adult's housing and subsidy for a wrongful use or with intent to defraud is financial abuse "
        "(§ 15610.30(a), (b)), and when proven by a preponderance of the evidence entitles him to attorney's fees and costs (§ 15657.5(a)) and to enhanced "
        "remedies (Civ. Code, § 3345). Protective relief is available under section 15657.03 and is the subject of the Solano County petition."))

    f.append(P("X. Fiduciary Failures – Plaintiff, Its Agents, and Its Counsel", h2))
    f.append(P(
        "<b>Plaintiff and its agents.</b> As a VA-accredited representative and HUD-VASH supportive-housing provider, plaintiff undertook to act for defendant's "
        "benefit in housing and benefits matters. A party that undertakes to act for another in a relationship of trust and dependence owes the duties of a "
        "fiduciary: loyalty, candor, and care (Wolf v. Superior Court (2003) 107 Cal.App.4th 25, 29-31; Civ. Code, § 2322). Plaintiff breached each by (a) "
        "terminating the tenancy for the very communications its accommodation agreement invited; (b) failing to convene the HUD grievance conference and to "
        "notify the housing authority with the notice (24 C.F.R. § 982.310(e)(2)(B)); (c) failing to maintain the federal tenancy file (RX-1); (d) rendering the "
        "unit uninhabitable and then suing the tenant who complained; and (e) spending federal subsidy on a unit it did not maintain – conduct cognizable "
        "under the California and federal False Claims Acts (Gov. Code, § 12651; 31 U.S.C. § 3729)."))
    f.append(P(
        "<b>Counsel.</b> Plaintiff's counsel are not defendant's fiduciaries, but they are officers of the court bound to candor (Bus. & Prof. Code, § 6068(d)) "
        "and they are plaintiff's agents whose acts bind it (Civ. Code, § 2338). Counsel (i) vouched for impossible diligence declarations (RX-4); (ii) took "
        "default against a known disabled, unrepresented litigant without warning (Fasuyi; Lasalle); (iii) misstated the period for relief from default "
        "(R06); (iv) filed in defendant's name (RX-10); (v) when defendant's requests for e-mail-only communication were made as a disability accommodation, "
        "characterized them as a \"data dump\" and refused to meet and confer by the accommodated medium; and (vi) continued to press execution of the writ "
        "after the Haines stay. Those are sanctionable acts (Code Civ. Proc., §§ 128.5, 128.7) and grounds for the Court's inherent-power relief."))

    f.append(P("XI. Public-Integrity Context: Supportive-Housing Nonprofits and Misappropriation of City Homelessness Funds", h2))
    f.append(P(
        "The Court may take judicial notice of the pendency of public prosecutions (Evid. Code, § 452(d), (h)). In January 2026 the San Francisco District "
        "Attorney charged two employees of the Providence Foundation with defrauding a City-funded homeless shelter; in February 2026 the District Attorney's "
        "Public Integrity Task Force charged Gwendolyn Westbrook, former CEO of United Council of Human Services, with nine felonies including misappropriation "
        "of public funds and grand theft, alleging diversion of more than $1.2 million in City homelessness grants between 2019 and 2023 following a 2022 City "
        "audit. Defendant does not allege that plaintiff is a party to those cases. He cites them because they establish that the City's homelessness and "
        "supportive-housing contractors are presently under active public-integrity scrutiny, and because the same questions are presented here: whether a "
        "nonprofit housing provider that draws federal and City subsidy for a disabled veteran's unit maintained the unit, kept the required federal records "
        "(it pleads it cannot find them, RX-1), honored the grievance procedures that condition the subsidy, and used the courts to remove the tenant who "
        "reported the conditions. Defendant has lodged complaints with HHS Office for Civil Rights (No. 25-621293), the California Civil Rights Department "
        "(No. 202601-33270627), the California Victim Compensation Board (Claim No. A26-10224054), San Francisco Adult Protective Services (SOC 341), the "
        "Board of Behavioral Sciences (Tab M), and the Department of Public Health (Case 101003004371). The Court should require plaintiff to account for the "
        "HUD-VASH subsidy received for Unit 301A during the period the unit was uninhabitable."))

    f.append(P("XII. Video Evidence Summary (Tab B)", h2))
    f.append(P(
        "Thirteen recordings were designated to plaintiff's counsel by evidentiary notice on October 29, 2026 (11:00 p.m. and 11:21 p.m.), with a foundation "
        "notice that each was made in common areas or at open tenant-union meetings where no reasonable expectation of privacy existed (Pen. Code, § 632). "
        "The recordings that matter most to the issues above are:"))
    rows = [["Ex.", "What it shows", "Issue proved"],
            ["Suite 2, V-01", "Landrum verbal confrontation and hostile posturing (Jan. 3, 2026).", "Retaliation; motive; dependent-adult abuse"],
            ["Suite 2, V-03", "Resident advisor \"Dwayne\": management admissions; no process-server visits logged.", "Falsity of diligence declarations"],
            ["Suite 2, V-05", "Dwayne accepts papers at the door (\"accidental legal service\").", "Door accessible; posting unjustified"],
            ["Suite 2, V-04 / V-06", "Verbal assault; property-level hostility; staff threats (\"kick their ass\").", "Retaliation; hypocrisy; protective orders"],
            ["Suite 1, V-02", "Infestation and unit conditions.", "Habitability (Defense No. 9)"],
            ["Suite 1, V-03", "Service dog Jaxx safety and access interference.", "Disability nexus; FHA/FEHA"],
            ["Suite 1, V-04", "Courthouse confrontation and process-server intimidation.", "Credibility of service declarations"],
            ["Suite 1, V-06 / V-07", "Medical vulnerability; case-manager interaction and emergency intervention.", "Rule 1.100; dependent-adult status"]]
    f.append(grid(rows, [1.2 * inch, 3.3 * inch, 2.0 * inch]))

    f.append(P("XIII. Current Status and Relief Required", h2))
    f.append(P(
        "Despite the Haines stay, plaintiff has caused the writ to be executed and the Sheriff has posted a notice to vacate. Defendant was treated in the "
        "John Muir Health Concord Emergency Department on October 30, 2026 after a fall and is under medical orders through at least November 4, 2026 (Tab J, "
        "confidential). The default and judgment of June 30, 2026 are void for want of service and were procured by extrinsic fraud and mistake; the notice "
        "on which the action rests states no lawful cause; and the orders of Judge Haines preserving the retaliation and habitability defenses remain binding. "
        "Defendant asks the Court to vacate the default and judgment (Code Civ. Proc., §§ 473(d), 473.5; inherent power), recall and quash the writ and "
        "reinstate the stay, grant the rule 1.100 accommodations requested at Tab J, require plaintiff to serve a lawful notice and, if it elects, file a "
        "new action, order an accounting of the HUD-VASH subsidy for Unit 301A, and set an order-to-show-cause re sanctions under sections 128.5 and 128.7."))
    f += signature()
    return rl(f, path, "Master Statement of the Case")


# ------------------------------------------------------------------ TAB B: Video list (moved forward) with foundation notices
def video_list(path):
    f = caption("DEFENDANT'S AUDIO-VISUAL EXHIBIT LIST, FOUNDATION, AND PUBLICATION PLAN")
    f.append(P(
        "The recordings below were designated as trial exhibits by formal evidentiary notice e-mailed to plaintiff's counsel on October 29, 2026 at 11:00 p.m. "
        "and 11:21 p.m., forwarded to Department 606 on October 30, 2026 at 1:27 p.m., and e-served through Proceed Legal the same day (order confirmation and "
        "eService notice, CUD-26-682107). Native files with metadata will be lodged on a USB drive at trial call. Defendant authenticates each recording as the "
        "person who made it (Evid. Code, §§ 1400, 1401, 1553); staff statements are offered as party admissions (§ 1222) and, alternatively, for effect on the "
        "listener and as prior inconsistent statements (§ 1235)."))
    f.append(P("Foundation: privacy and consent", h2))
    f.append(P(
        "By notice of October 29, 2026 (11:40 and 11:43 p.m.), defendant placed on the record that every recording was made in common areas, exterior grounds, "
        "or at open meetings of the San Francisco Veterans Tenants Union with property-management agents present, where no reasonable expectation of privacy "
        "existed (Pen. Code, § 632(c)); that management was aware of active tenant organizing and public accountability documentation; and that the union "
        "membership has authorized submission of the record. The same notices demanded preservation of staff communications, incident logs, security reports "
        "and resident-advisor logs for Girard Road."))
    for suite_idx, heading in [(0, "Suite 1 – Exhibits V-01 through V-07 (notice sent 11:00:17 p.m. PDT)"), (1, "Suite 2 – Exhibits V-01 through V-06 (notice sent 11:21:32 p.m. PDT)")]:
        f.append(P(heading, h2))
        rows = [["Ex.", "Title and description", "Repository link"]]
        for code, title, url, desc in NOTICES[suite_idx]["videos"]:
            rows.append([P(code, cellb), P(f"<b>{title}</b><br/>{desc}", cell), P(url, cellurl)])
        f.append(grid(rows, [0.55 * inch, 3.6 * inch, 2.35 * inch]))
    f.append(P("Publication plan", h2))
    f.append(P(
        "Suite 2 V-03 and V-05 (Dwayne) during the service witnesses (Falanga, Martinez, Bradford, Landrum); Suite 2 V-01, V-04 and V-06 on retaliation, "
        "motive and dependent-adult abuse; Suite 1 V-02 and V-03 with the photographs at Tab L on habitability and the service animal; Suite 1 V-04 on the "
        "credibility of the service declarations; Suite 1 V-06 and V-07 in support of the rule 1.100 requests. Total running time under ninety minutes."))
    f += signature()
    return rl(f, path, "Video List")


# ------------------------------------------------------------------ TAB F: Points and Authorities (expanded)
AUTH = [
    ("Service of process and void judgments", [
        ("Code Civ. Proc., §§ 415.10, 415.20, 415.45, 412.20, 585, 1162, 1167, 1169; Evid. Code, § 647", "Statutory methods; posting only on showing of reasonable diligence; registered-server presumption is rebuttable."),
        ("Greene v. Lindsey (1982) 456 U.S. 444", "Posting on an apartment door in eviction proceedings is constitutionally inadequate notice where mail is available."),
        ("Peralta v. Heights Medical Center, Inc. (1988) 485 U.S. 80", "Judgment without valid service violates due process and must be set aside regardless of meritorious defense."),
        ("Mullane v. Central Hanover Bank & Trust Co. (1950) 339 U.S. 306", "Notice must be reasonably calculated to apprise the party."),
        ("Dill v. Berquist Construction Co. (1994) 24 Cal.App.4th 1426", "Default void where statutory service not accomplished; strict compliance."),
        ("County of San Diego v. Gorham (2010) 186 Cal.App.4th 1215", "False proof of service by process server = extrinsic fraud; void judgment may be set aside at any time."),
        ("Kremerman v. White (2021) 71 Cal.App.5th 358", "Defective substitute service; default and judgment void under § 473(d)."),
        ("American Express Centurion Bank v. Zara (2011) 199 Cal.App.4th 383", "Process server's declaration contradicted by evidence; no personal jurisdiction."),
        ("Bein v. Brechtel-Jochim Group, Inc. (1992) 6 Cal.App.4th 1387", "Reasonable diligence standard for departing from personal service."),
        ("Watts v. Crawford (1995) 10 Cal.4th 743", "Reasonable diligence requires exhausting likely avenues; service by publication/posting is last resort."),
        ("Olvera v. Olvera (1991) 232 Cal.App.3d 32", "Constructive service statutes strictly construed."),
        ("Summers v. McClanahan (2006) 140 Cal.App.4th 403", "Limits of substantial compliance; burden on plaintiff."),
        ("Strathvale Holdings v. E.B.H. (2005) 126 Cal.App.4th 1241", "Plaintiff bears burden to prove valid service when challenged."),
        ("Lewis v. Superior Court (1985) 175 Cal.App.3d 757", "Default void where served on wrong person/manner; vacated."),
    ]),
    ("Default, extrinsic fraud and mistake, and counsel's duties", [
        ("Code Civ. Proc., §§ 473(b), 473(d), 473.5; Rules Prof. Conduct, rules 3.3, 3.4, 4.1, 8.4; Bus. & Prof. Code, §§ 6068(d), 6106", "Relief from void or wrongfully procured defaults; candor to the tribunal."),
        ("Rappleyea v. Campbell (1994) 8 Cal.4th 975", "Extrinsic mistake; reliance on official misinformation; policy favoring trial on the merits."),
        ("Kulchar v. Kulchar (1969) 1 Cal.3d 467", "Equitable relief for extrinsic fraud and mistake."),
        ("In re Marriage of Stevenot (1984) 154 Cal.App.3d 1051", "Definition of extrinsic fraud: prevented from presenting case."),
        ("Sporn v. Home Depot USA, Inc. (2005) 126 Cal.App.4th 1294", "Extrinsic mistake standard; diligence."),
        ("Fasuyi v. Permatex, Inc. (2008) 167 Cal.App.4th 681", "Counsel's professional obligation to warn before taking default; quiet speed condemned."),
        ("Lasalle v. Vogel (2019) 36 Cal.App.5th 127", "Taking default without warning violates ethical duty; relief required."),
        ("Kim v. Westmoore Partners, Inc. (2011) 201 Cal.App.4th 267", "Court must scrutinize default judgments; counsel's misrepresentations condemned."),
        ("Au-Yang v. Barton (1999) 21 Cal.4th 958", "Default judgment may not exceed relief demanded in complaint."),
        ("Manson, Iver & York v. Black (2009) 176 Cal.App.4th 36", "§ 473(d) relief from void judgment; no time limit when void on face/for lack of service."),
        ("Hazel-Atlas Glass Co. v. Hartford-Empire Co. (1944) 322 U.S. 238", "Fraud on the court; judgment procured by fraud set aside."),
        ("Chambers v. NASCO, Inc. (1991) 501 U.S. 32", "Inherent power to sanction bad-faith litigation conduct."),
        ("Slesinger, Inc. v. Walt Disney Co. (2007) 155 Cal.App.4th 736", "California courts' inherent power to remedy deliberate misconduct."),
        ("Pierotti v. Torian (2000) 81 Cal.App.4th 17", "Sanctions for frivolous and bad-faith conduct; inherent authority."),
    ]),
    ("Unlawful detainer notice; subsidized tenancy; habitability; retaliation", [
        ("24 C.F.R. § 982.310; 42 U.S.C. § 1437f(o)(7), (o)(19); 24 C.F.R. part 247; 34 U.S.C. § 12491 (VAWA)", "Good cause; notice must state grounds; copy to PHA; HUD-VASH placement."),
        ("Civ. Code, §§ 47(b), 1941.1, 1942.4, 1942.5; S.F. Admin. Code, §§ 37.9(a)(3), (c), (f), 37.10B", "Litigation privilege; habitability; retaliation (180-day presumption); nuisance; harassment."),
        ("Kwok v. Bergren (1982) 130 Cal.App.3d 596", "Notice strictly construed; defective notice defeats UD."),
        ("Bevill v. Zoura (1994) 27 Cal.App.4th 694", "Notice must be accurate; summary remedy requires strict compliance."),
        ("Delta Imports, Inc. v. Municipal Court (1983) 146 Cal.App.3d 1033", "Valid notice is element of the UD cause of action."),
        ("Dr. Leevil, LLC v. Westlake Health Care Center (2018) 6 Cal.5th 474", "Strict compliance with statutory notice prerequisites."),
        ("Liebovich v. Shahrokhkhany (1997) 56 Cal.App.4th 511; Palm Property Investments, LLC v. Yadegar (2011) 194 Cal.App.4th 1419", "Service of notice strictly construed."),
        ("WDT-Winchester v. Nilsson (1994) 27 Cal.App.4th 516", "Nuisance-based termination requires substantive proof."),
        ("Wasatch Property Management v. Degrate (2005) 35 Cal.4th 1111", "Section 8 tenancy; notice requirements."),
        ("Mitchell v. Poole (1988) 203 Cal.App.3d Supp. 1", "Federal notice requirements for subsidized tenancy."),
        ("Green v. Superior Court (1974) 10 Cal.3d 616", "Implied warranty of habitability is a defense in UD."),
        ("Knight v. Hallsthammar (1981) 29 Cal.3d 46", "Habitability breach; no prior-notice prerequisite."),
        ("Erlach v. Sierra Asset Servicing, LLC (2014) 226 Cal.App.4th 1281", "Habitability and retaliation claims; landlord duties."),
        ("Barela v. Superior Court (1981) 30 Cal.3d 244", "Retaliatory eviction for reporting to authorities barred."),
        ("Schweiger v. Superior Court (1970) 3 Cal.3d 507", "Retaliatory eviction defense in UD."),
        ("Western Land Office, Inc. v. Cervantes (1985) 175 Cal.App.3d 724", "Retaliation; § 1942.5 remedies."),
    ]),
    ("Disability access, accommodation, and dependent adults", [
        ("Cal. Rules of Court, rule 1.100; 42 U.S.C. §§ 12131-12132; Gov. Code, §§ 11135, 12927(c)(1), 12955; 42 U.S.C. § 3604(f)(3)(B); Civ. Code, §§ 54.1, 54.2", "Court access accommodations; FHA/FEHA reasonable accommodation; service animals."),
        ("Tennessee v. Lane (2004) 541 U.S. 509", "Title II guarantees access to the courts for persons with disabilities."),
        ("Vesco v. Superior Court (2013) 221 Cal.App.4th 275", "Rule 1.100 requests must be granted unless fundamental alteration/undue burden; procedure."),
        ("Biscaro v. Stern (2010) 181 Cal.App.4th 702", "Failure to rule on accommodation request before proceeding is reversible."),
        ("In re Marriage of James & Christine C. (2008) 158 Cal.App.4th 1261", "Rule 1.100 denial without findings reversed."),
        ("Auburn Woods I Homeowners Assn. v. Fair Employment & Housing Com. (2004) 121 Cal.App.4th 1578", "Assistance animal as reasonable accommodation."),
        ("Welf. & Inst. Code, §§ 15610.07, 15610.17, 15610.23, 15610.30, 15610.43, 15657, 15657.03, 15657.5; Civ. Code, § 3345; Pen. Code, § 368", "Dependent-adult abuse, care custodian, financial abuse, protective orders, enhanced remedies."),
        ("Wolf v. Superior Court (2003) 107 Cal.App.4th 25", "When a fiduciary/confidential relationship arises from undertaking to act for another."),
        ("Civ. Code, §§ 2322, 2330, 2338", "Agent's acts bind the principal; agent's duties."),
    ]),
    ("Coordinate jurisdiction and reconsideration", [
        ("Code Civ. Proc., § 1008", "Exclusive procedure for reconsidering a prior ruling."),
        ("In re Alberto (2002) 102 Cal.App.4th 421", "One judge may not overrule another judge of the same court on the same matter."),
        ("Ford v. Superior Court (1986) 188 Cal.App.3d 737", "Coordinate-jurisdiction rule; second judge lacks power to reverse."),
        ("Williams v. Superior Court (1939) 14 Cal.2d 656", "Departments are one court; orders of one bind the others."),
        ("People v. Konow (2004) 32 Cal.4th 995", "Coordinate jurisdiction principles."),
        ("Le Francois v. Goel (2005) 35 Cal.4th 1094", "Court's own-motion reconsideration must follow § 1008 constraints."),
    ]),
    ("Public integrity and subsidy accountability", [
        ("Gov. Code, § 12650 et seq. (California False Claims Act); 31 U.S.C. § 3729 et seq.", "Liability for subsidy claimed while failing conditions of participation."),
        ("Evid. Code, §§ 452(d), (h), 453", "Judicial notice of court records and public prosecutions (People v. Westbrook, S.F. Super. Ct., filed Feb. 2026; Providence Foundation employees, Jan. 2026)."),
        ("24 C.F.R. § 982.310(e); HUD-VASH Operating Requirements (77 Fed.Reg. 17086, Mar. 23, 2012)", "Owner obligations and PHA notice as conditions of subsidy."),
    ]),
]


def points_authorities(path):
    f = caption("MEMORANDUM OF POINTS AND AUTHORITIES WITH TABLE OF AUTHORITIES AND CASE SUMMARIES")
    f.append(P("I. Summary of Argument", h2))
    f.append(P(
        "(1) The judgment is void: no proof of service on the defendant was ever filed, and the diligence declarations supporting the posting order are "
        "false on their face (Statement, §§ VI, RX-4 to RX-7). (2) The default was procured by extrinsic fraud and mistake while defendant's rule 1.100 request "
        "was pending under the Court's written assurance (§ VII). (3) The notice states only protected activity and is void; a HUD-VASH tenancy may be "
        "terminated only for good cause stated with specificity (§ V). (4) Judge Haines's stay and his August 27, 2026 order preserving Defenses 5 and 9 bind "
        "Department 606 absent section 1008 proceedings (§ VIII). (5) The conduct of plaintiff and counsel constitutes fraud on the court, abuse of a "
        "dependent adult, and breach of fiduciary and agency duties warranting relief and sanctions (§§ IX, X). (6) Substitution or association of counsel "
        "does not cure a void record; the remedy is a new notice and, if plaintiff elects, a new action."))
    f.append(P("II. Why Substitution of Counsel Does Not Cure the Record", h2))
    f.append(P(
        "The defects are jurisdictional and attach to the proceeding, not to the lawyer. A void judgment cannot be ratified by later appearance of new counsel "
        "(Dill, supra, 24 Cal.App.4th at pp. 1439-1444); a notice that states no lawful cause cannot be amended mid-case (Kwok, supra; Delta Imports, supra); "
        "and declarations already filed remain in the record for every purpose, including sanctions and referral (Bus. & Prof. Code, § 6068(d); Code Civ. "
        "Proc., § 128.7(c))."))
    f.append(P("III. Table of Authorities with Holdings", h2))
    for heading, items in AUTH:
        f.append(P(heading, h3))
        rows = [["Authority", "Holding / use in this case"]] + [[a, b] for a, b in items]
        f.append(grid(rows, [3.1 * inch, 3.4 * inch]))
        f.append(Spacer(1, 6))
    f.append(P("IV. Matching the Authorities to the Record", h2))
    rows = [["Record fact (RX / Tab)", "Controlling authority", "Result"],
            ["Falanga declarations dated 5/11 reciting 5/12 attempt (RX-5, RX-6); counsel vouches (RX-4)", "Gorham; Zara; Evid. Code § 647; B&P § 6068(d)", "Presumption rebutted; posting order void; referral"],
            ["POS-010 names only \"All Unnamed Occupants\" (RX-7)", "Dill; Kremerman; CCP §§ 585, 1169; Peralta", "Default and judgment void (§ 473(d))"],
            ["Default taken while MC-410 pending; \"no further action required\" (RX-8)", "Rappleyea; Biscaro; Vesco; Fasuyi; Lasalle", "Extrinsic mistake; set aside; accommodation first"],
            ["Notice grounds = e-mails and RO petition (RX-2)", "Civ. Code §§ 47(b), 1942.5(d); Barela; 24 C.F.R. § 982.310; Kwok", "Notice void; no cause of action"],
            ["HUD addenda \"cannot be located\" (RX-1)", "24 C.F.R. § 982.310(e); Mitchell v. Poole; Wasatch", "Subsidy conditions unmet; accounting"],
            ["Haines stay and Aug. 27 order; later oral disregard", "In re Alberto; Ford; Williams; CCP § 1008", "Prior orders binding; defenses 5 and 9 preserved"],
            ["\"Attorneys for Defendant\" filing (RX-10); notice of entry misstating relief period (R06)", "Kim v. Westmoore; Rules 3.3, 8.4(c); CCP § 128.7", "Sanctions OSC; credibility of record"],
            ["Staff threats; clinician \"or else\"; writ pressed despite stay (V-01, V-04, V-06)", "W&I §§ 15610.07, 15610.30, 15657.03; Civ. Code § 3345", "Dependent-adult abuse; protective relief; fees"]]
    f.append(grid(rows, [2.5 * inch, 2.3 * inch, 1.7 * inch]))
    f += signature()
    return rl(f, path, "Points and Authorities")


# ------------------------------------------------------------------ TAB H: Record excerpts (key pages only)
EXCERPTS = [
    ("R01 – Summons, Complaint and Notice (May 5, 2026): pp. 1, 3, 5-8, 33-35, 55", R["R01"], [1, 3, 5, 6, 7, 8, 33, 34, 35, 55]),
    ("R02 – Ex Parte Application for Posting with Martinez and Falanga declarations (May 19, 2026), complete clean copy", EXP, [1, 2, 3, 4, 5]),
    ("R03 – Request for Entry of Default, entered June 30, 2026, p. 1", R["R03"], [1]),
    ("R04 – Clerk's Judgment by Default (UD-110), June 30, 2026, complete", R["R04"], [1, 2]),
    ("R05 – POS-010 by posting, \"All Unnamed Occupants,\" June 30, 2026, pp. 1-2", R["R05"], [1, 2]),
    ("R06 – Notice of Entry of Judgment, July 1, 2026, p. 1", R["R06"], [1]),
    ("R07 – Writ request (MC-030), July 1, 2026", R["R07"], [1]),
    ("R08 – Defendant's Emergency Ex Parte Application, July 7, 2026, p. 1", R["R08"], [1]),
    ("R09 – Defendant's Ex Parte Packet with Answer dated May 17, 2026, pp. 1-3", R["R09"], [1, 2, 3]),
    ("R10 – Order re Ex Parte and \"Attorneys for Defendant\" P&A, July 8, 2026, complete", R["R10"], [1, 2, 3]),
]


def excerpt_items():
    items = []
    for label, src, pages in EXCERPTS:
        d = fitz.open(src); out = fitz.open()
        for p in pages:
            if p <= len(d):
                out.insert_pdf(d, from_page=p - 1, to_page=p - 1)
        path = os.path.join(TMP, f"exc_{label[:3]}.pdf"); out.save(path); out.close(); d.close()
        items.append((label, path))
    return items


# ------------------------------------------------------------------ witnesses: add the missing names once
EXTRA_WITNESSES = [
    ["17", "Charity Martinez, Esq. (SBN 367234)", "Associate, Zanghi Torres Adams LLP; declarant on the May 19, 2026 ex parte application", "Basis for swearing to \"more than three attempts\"; receipt and review of the Falanga declarations dated before the event they recite (RX-4 to RX-6)."],
    ["18", "Kobe/Kolby Losik", "Clinician, Swords to Plowshares", "December 23, 2025 accommodation consensus; January 2, 2026 statement \"stop with the e-mails, or else\" (V-01, suite 2)."],
    ["19", "Joel Champion", "Management, Swords to Plowshares", "December 23, 2025 written-communication accommodation agreement."],
    ["20", "Bradley White", "Fiduciary / signatory, Swords to Plowshares", "Decision to terminate; blocking of legal service providers; HUD grievance procedure; subsidy accounting."],
    ["21", "Joy Guandique, ADA Coordinator (personally)", "San Francisco Superior Court", "June 1 and June 10, 2026 communications: MC-410 received, under review, \"no further action is required.\""],
]


def witness_list(path):
    existing = " ".join(r[1] for r in A.WITNESS_ROWS).lower()
    rows = [list(r) for r in A.WITNESS_ROWS]
    # Correct Martinez's capacity (she is counsel of record, not staff) and avoid a duplicate entry.
    for r in rows:
        if r[1].startswith("Martinez"):
            r[1] = "Charity Martinez, Esq. (SBN 367234)"; r[2] = "Associate, Zanghi Torres Adams LLP; ex parte declarant (RX-4)"
        if r[1].startswith("Process server Falanga"):
            r[1] = "Joseph Falanga, Spirit Courier (S.F. Reg. No. 1539)"
    for e in EXTRA_WITNESSES:
        if e[1].split(",")[0].split(" (")[0].lower() in existing and "Martinez" in e[1]:
            continue
        rows.append(e)
    for i, r in enumerate(rows):
        r[0] = str(i + 1)
    f = caption("DEFENDANT'S WITNESS LIST AND OFFER OF PROOF")
    f.append(P("Defendant identifies the following witnesses and the reason each is called. Subpoenas duces tecum for the subpoenaed witnesses are at Tab I. "
               "Defendant reserves the right to call any witness identified by plaintiff and rebuttal witnesses."))
    f.append(Spacer(1, 10))
    f.append(grid([["No.", "Witness", "Capacity", "Why the witness is called"]] + rows, [0.45 * inch, 1.7 * inch, 1.65 * inch, 2.7 * inch]))
    f.append(P("Estimated time", h2))
    f.append(P("Two court days for defendant's case, exclusive of cross-examination. Dr. Gillson will testify with the accommodations requested under rule 1.100 (Tab J)."))
    f += signature()
    return rl(f, path, "Witness List")


# ------------------------------------------------------------------ covers
def cover_sf(path):
    f = [Spacer(1, 1.2 * inch), P("FINAL ALL-IN-ONE TRIAL BINDER", ParagraphStyle("big", parent=h1, fontSize=24, leading=32)),
         P("San Francisco – Statement of the Case with Embedded Record Exhibits, Video Evidence, Witnesses, Authorities, and Record Excerpts",
           ParagraphStyle("sub", parent=cen, fontSize=13, leading=20)), Spacer(1, 20),
         P(f"<i>{CASE}</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P(f"Case No. {CASE_NO} (related: CCH-26-589086, CCH-26-589728)", cen), P(COURT, cen), P(DEPT, cen), P(TRIAL, cen), Spacer(1, 24),
         P(f"Submitted by {NAME}", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 24),
         P("Tab A shows and cites the record pages that prove each finding (Record Exhibits RX-1 to RX-10). Tab B brings the thirteen video exhibits to the "
           "forefront. Tabs C-G are the witness list, exhibit list, index of irregularities, points and authorities, and closing. Tab H contains the excerpted "
           "record pages at full size; the complete filings (290 pages) are omitted as redundant and available on request. Tab J is confidential in part "
           "(Cal. Rules of Court, rule 1.100(c)(4)). The Solano County binder is a separate volume.", small),
         Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


def cover_sol(path):
    f = [Spacer(1, 1.2 * inch), P("FINAL ALL-IN-ONE BINDER", ParagraphStyle("big", parent=h1, fontSize=24, leading=32)),
         P("Solano County – Civil Harassment / Dependent-Adult Protective Petition, Order Shortening Time, Rule 1.100 Request, and Supporting Record",
           ParagraphStyle("sub", parent=cen, fontSize=13, leading=20)), Spacer(1, 20),
         P("<i>Gillson v. Landrum, Torres &amp; Zanghi</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P("Code Civ. Proc., § 527.6; Welf. &amp; Inst. Code, § 15657.03", cen),
         P("Superior Court of California, County of Solano", cen), P("Case No. ______________ – Dept. ______", cen), Spacer(1, 24),
         P(f"Submitted by {NAME}, Petitioner in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 24),
         P("Tab A is filed with the petition. Tab B is for the Court's ADA Coordinator and is confidential in part (rule 1.100(c)(4)). Tabs C-F supply the "
           "San Francisco record that establishes the course of conduct: the Statement of the Case with embedded record exhibits, the video evidence, the "
           "points and authorities, and the excerpted court record. Tab G contains the twenty San Francisco rule 1.100 orders. Materials duplicated in the "
           "San Francisco binder are included here only where the Solano Court needs them to rule.", small),
         Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


if __name__ == "__main__":
    photo_counts = {l: len(items) for l, _, items in A.CATEGORIES}
    print("drafting shared sections")
    tabA = statement_of_case(os.path.join(TMP, "fin_A.pdf"))
    tabB = video_list(os.path.join(TMP, "fin_B.pdf"))
    tabC = witness_list(os.path.join(TMP, "fin_C.pdf"))
    tabD = A.evidence_list(os.path.join(TMP, "fin_D.pdf"), photo_counts)
    tabE = A.irregularities(os.path.join(TMP, "fin_E.pdf"))
    tabF = points_authorities(os.path.join(TMP, "fin_F.pdf"))
    tabG = A.closing(os.path.join(TMP, "fin_G.pdf"))
    excerpts = excerpt_items()
    ada_items = [(f"Ex. {i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]
    med_ex = medical_exhibit(os.path.join(TMP, "medical_exhibit.pdf"))

    # ---------------- San Francisco
    print("SF: MC-410, subpoenas")
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", CASE_NO, f"{COURT} – {DEPT}",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted, and that all communications with opposing counsel be in writing by e-mail as previously agreed. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further hearings in this case.", "Defendant", "Unlawful detainer",
                       "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    mc_sf_merged = merge(mc_sf, os.path.join(TMP, "fin_mc_sf.pdf"))
    sub_items = []
    for w in WITNESSES:
        sub_items.append((f"Civil Subpoena (Duces Tecum) – {w['name']}", merge(make_subpoena(w), os.path.join(TMP, f"fin_subp_{w['tag']}.pdf"))))
    svc_rows = [["Witness", "Capacity", "Service address"]] + [[w["name"], w["role"], w["addr"]] for w in WITNESSES]
    svc = rl([P("SUBPOENA SERVICE DIRECTORY", h1),
              P("Subpoenas must be issued by the clerk before service and personally served with fees tendered on demand (Code Civ. Proc., §§ 1985, 1987; Gov. Code, § 68093).", small),
              Spacer(1, 10), grid(svc_rows, [2.1 * inch, 2.2 * inch, 2.2 * inch])], os.path.join(TMP, "fin_svc.pdf"))

    A.PREFIX = "SF"
    sections_sf = [
        ("A", "Master Statement of the Case with Embedded Record Exhibits RX-1 to RX-10", [("Statement of the Case (Sections I–XIII)", tabA)]),
        ("B", "Video Evidence – Thirteen Audio-Visual Exhibits, Foundation, Publication Plan", [("Audio-visual exhibit list", tabB)]),
        ("C", "Witness List and Offer of Proof", [("Witness list, 21 witnesses", tabC)]),
        ("D", "Exhibit and Evidence List", [("Exhibit and evidence list, Parts 1–4", tabD)]),
        ("E", "Index of Record Irregularities and Indicia of Fraud", [("Line-by-line index", tabE)]),
        ("F", "Points and Authorities – Table of Authorities with Case Summaries", [("Memorandum", tabF)]),
        ("G", "Closing Argument", [("Closing argument outline", tabG)]),
        ("H", "Record Excerpts – Key Pages of the Filed Court Record (R01–R10)", excerpts),
        ("I", "Notice to Counsel and Civil Subpoenas (SUBP-002 with Attachment 3)",
         [("Notice to Francisco Torres, Esq., October 31, 2026", os.path.join(COMP, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")),
          ("Service directory", svc)] + sub_items),
        ("J", "Request for Accommodations – MC-410 (Dept. 606) – CONFIDENTIAL IN PART",
         [("MC-410 with Attachment", mc_sf_merged), ("CONFIDENTIAL Exhibit – John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
        ("K", "Rule 1.100 Orders and Responses of this Court (July–October 2026)", ada_items),
        ("L", "Evidence Exhibit Binder – Photographs, Notices, and Agency Records (Categories A–K)",
         [("Gillson Evidence Exhibit Binder (Bates GILLSON-)", os.path.join(COMP, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
        ("M", "Related Administrative Complaints (Board of Behavioral Sciences)",
         [("BBS Complaint 2002026002097 – Kolby Losik", os.path.join(COMP, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
          ("BBS Complaint 2002026002098 – Mark Villalobos", os.path.join(COMP, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))]),
    ]
    n_sf = assemble(OUT_SF, cover_sf(os.path.join(TMP, "fin_cover_sf.pdf")), sections_sf,
                    "Gillson – FINAL All-in-One Trial Binder – San Francisco – CUD-26-682107 – Tab J confidential in part (CRC 1.100(c)(4))")
    compress_scans(OUT_SF)
    print("SF pages", n_sf)

    # ---------------- Solano
    print("Solano: MC-410")
    mc_sol = make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)",
                        "Superior Court of California, County of Solano – Civil Harassment (Code Civ. Proc., § 527.6)",
                        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026. I ask to appear by Zoom at every hearing in this matter until those orders are lifted. The emergency department record is attached as a confidential exhibit."],
                        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings.")
    mcsp = merge(mc_sol, os.path.join(TMP, "fin_mc_sol.pdf"))
    A.PREFIX = "SOL"
    sections_sol = [
        ("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order",
         [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
        ("B", "Request for Accommodations – MC-410 (Solano County) – CONFIDENTIAL IN PART",
         [("MC-410 with Attachment", mcsp), ("CONFIDENTIAL Exhibit – John Muir Health ED record (Oct. 30, 2026)", med_ex)]),
        ("C", "Course of Conduct – Master Statement of the Case with Embedded Record Exhibits (San Francisco, CUD-26-682107)", [("Statement of the Case (Sections I–XIII)", tabA)]),
        ("D", "Video Evidence – Thirteen Audio-Visual Exhibits, Foundation, Publication Plan", [("Audio-visual exhibit list", tabB)]),
        ("E", "Points and Authorities – Table of Authorities with Case Summaries", [("Memorandum", tabF)]),
        ("F", "Record Excerpts – Key Pages of the San Francisco Court Record (R01–R10)", excerpts),
        ("G", "San Francisco Superior Court Rule 1.100 Orders and Responses (July–October 2026)", ada_items),
    ]
    n_sol = assemble(OUT_SOL, cover_sol(os.path.join(TMP, "fin_cover_sol.pdf")), sections_sol,
                     "Gillson – FINAL All-in-One Binder – Solano County – Confidential in part (CRC 1.100(c)(4))")
    compress_scans(OUT_SOL)
    print("Solano pages", n_sol)

    # remove superseded artifacts so exactly two binders remain
    for old in ["Gillson_All_In_One_Trial_Binder_CUD-26-682107.pdf", "Gillson_Solano_All_In_One_Accommodation_Binder.pdf", "Gillson_Evidence_Exhibit_Binder.pdf"]:
        p = os.path.join(ART, old)
        if os.path.exists(p):
            if old.startswith("Gillson_Evidence"):
                os.replace(p, os.path.join(COMP, old))
            else:
                os.remove(p)
