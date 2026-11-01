"""All-in-one trial binder for CUD-26-682107. The Solano MC-410 binder is built separately by build_binders.py and is NOT included here."""
import os, shutil, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

from build_binders import (HERE, ART, TMP, NAME, ADDR1, ADDR2, PHONE, EMAIL, body, small, h1, h2, cen, num, P, rl_pdf,
                           cover_page, assemble, medical_exhibit, make_mc410, make_subpoena, WITNESSES, ADA_EXHIBITS, compress_scans)
from notices import NOTICES

CASE = "Swords to Plowshares v. Donald Ernest Gillson, Ed.D., Case No. CUD-26-682107"
COURT = "Superior Court of California, County of San Francisco, Dept. 606 (Hon. Stephen M. Murphy)"
h3 = ParagraphStyle("h3", fontName="Times-BoldItalic", fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=3)
cell = ParagraphStyle("cell", fontName="Times-Roman", fontSize=9, leading=11)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Times-Bold")
quote = ParagraphStyle("q", parent=body, leftIndent=30, rightIndent=20, fontSize=10.5, leading=13.5)


def caption(title):
    return [P(f"<b>{title}</b>", h1), P(f"<i>{CASE}</i><br/>{COURT}<br/>Defendant: {NAME}, in propria persona", cen), Spacer(1, 10)]


def grid(data, widths, header=True):
    if header:
        data = [[Paragraph(c, cellb) if isinstance(c, str) else c for c in data[0]]] + data[1:]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("FONT", (0, 0), (-1, -1), "Times-Roman", 9), ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st += [("FONT", (0, 0), (-1, 0), "Times-Bold", 9), ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9))]
    t.setStyle(TableStyle(st))
    return t


def sig(flow):
    flow += [Spacer(1, 10),
             P("I declare under penalty of perjury under the laws of the State of California that the factual statements above are true "
               "of my own knowledge, except those stated on information and belief, which I believe to be true.", small),
             Spacer(1, 6), P("Dated: October 31, 2026&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________________<br/>"
                             "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                             "Dr. Donny Gillson, Ed.D., Defendant in pro per", body)]
    return flow


# ======================================================================= TAB: STATEMENT OF THE CASE
def statement_of_case(path):
    F = caption("STATEMENT OF THE CASE")
    F.append(P("1. The parties and the premises", h2))
    F.append(P("Plaintiff Swords to Plowshares, a California non-profit, operates the Girard Road supportive-housing program at 1030 Girard Road in the "
               "Presidio of San Francisco. Defendant Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson) is a disabled veteran, a dependent adult with an open "
               "Adult Protective Services case, and the tenant of Unit 301A under a HUD-VASH / SSVF supported tenancy. He lives with his PTSD service dog, Jaxx. "
               "He is Secretary of the San Francisco Veterans Tenants Union, which organizes residents of the building."))
    F.append(P("2. The conditions that preceded the notice", h2))
    F.append(P("Beginning November 16, 2025, defendant submitted written grievances and maintenance requests to management (Exs. 1-2) documenting a German "
               "cockroach infestation, sewage and sanitation failures, and unsafe conditions in the unit (Exs. 3-20). The infestation injured his service dog "
               "(Exs. 21-27, veterinary treatment Dec. 11, 2025) and defendant himself (Exs. 28-44, including UCSF and emergency-department records of Nov. 26 and "
               "Dec. 9, 2025). Defendant reported the conditions to the San Francisco Department of Public Health (311 / Environmental Health Case No. 101003004371) "
               "and other agencies (Exs. 53-56). Management's written responses are at Exs. 45-52. A vehicle break-in at the premises was reported to the U.S. "
               "Park Police on December 25, 2025 (Exs. 57-65). Defendant filed complaints with the Board of Behavioral Sciences against two program clinicians on "
               "January 2, 2026 (Exs. 77-78)."))
    F.append(P("3. Protected activity in 2026", h2))
    F.append(P("From July 2026 forward defendant made repeated requests for disability accommodation to this Court under California Rules of Court, rule 1.100, "
               "which the Court granted in a series of orders and responses dated July 20 and 22, August 6, 14, 27 and 31, September 8, 10, 18, 22 and 24, and "
               "October 8 and 14, 2026 (Tab I). On September 8, 2026 defendant submitted a formal administrative complaint (Attachment B) which the Court "
               "acknowledged the same day. Defendant also requested accommodations from the landlord for his service animal, assistive technology, and "
               "written-only communication. Plaintiff's counsel was served with the Court's orders."))
    F.append(P("4. The three-day notice and the complaint", h2))
    F.append(P("Plaintiff then caused a three-day notice to be served on defendant. The notice is written in the third person and alleges generalized "
               "\u201cstaff harassment\u201d; it names no staff member, no date, and no incident. The proof of service identifies Jerome Bradford as the person who "
               "executed and/or served the notice and William Landrum, the assistant property manager, as the declarant or witness. Defendant's position, supported "
               "by his own dated records and by the video statements of resident advisor Dwayne (Video Exs. V-03 and V-05, second suite), is that Mr. Bradford was "
               "not at the premises at the date and time declared, that the papers were in fact left by accident, and that the proof of service therefore does not "
               "describe what happened. No written warning, incident report, or notice to cure preceded the notice. The only dispute that actually occurred was a "
               "personal one between Mr. Landrum and defendant; Mr. Landrum is at once the complaining witness, the person who caused the notice to issue, and the "
               "declarant on service. Plaintiff's counsel has described the reason for the eviction as \u201cthe way that staff was treated.\u201d"))
    F.append(P("Plaintiff, through John P. Zanghi, Esq. and Francisco G. Torres, Esq. of Zanghi Torres Adams LLP, filed this unlawful detainer action, "
               "CUD-26-682107. Defendant answered in propria persona and served special interrogatories and demands for production; plaintiff served no responses. "
               "Trial call is set for November 2, 2026 at 9:00 a.m. in Department 606. Related civil-harassment matters are pending as CCH-26-589086 and "
               "CCH-26-589728, and a petition under Code of Civil Procedure section 527.6 is being filed in Solano County against Mr. Landrum, Mr. Torres and Mr. Zanghi; "
               "the Solano accommodation papers are kept in a separate binder."))
    F.append(P("5. Conduct during the litigation", h2))
    F.append(P("On a hearing date in Department 505, plaintiff's counsel caused a box of documents to be deposited on defendant without an index, cover letter, or proof "
               "of service, in disregard of the Court's accommodation orders. Defendant was confronted at the courthouse by a process server who handled his "
               "driver's license data (Video Ex. V-04, first suite). Staff and resident advisors at the building have threatened residents that they will "
               "\u201ckick their ass\u201d (Tab H, Notice 3). On October 29, 2026 defendant served four formal evidentiary notices on counsel designating thirteen "
               "audio-visual recordings as trial exhibits, and forwarded them to Department 606 on October 30, 2026 (Exs. 72-76). Counsel replied the same day to three "
               "other notices from defendant (fraud notice; Solano filings notice; State Bar complaint notice) and e-served a filing through Proceed Legal (Tab G, "
               "transmission log). Defendant understands Mr. Zanghi has been or is being removed from the case."))
    F.append(P("6. Defendant's medical status", h2))
    F.append(P("On October 30, 2026 defendant was treated in the John Muir Health Concord Emergency Department after a fall (CT head, CT cervical spine; acute cervical "
               "strain) and was placed off work through November 3, 2026, return no earlier than November 4, with directed follow-up at David Grant USAF Medical Center, "
               "Travis AFB, on or about November 1, 2026, where an extension of approximately two weeks is anticipated. A neuropsychological evaluation was performed "
               "October 27, 2026 and results are pending. Defendant has asked, by MC-410 (Tab H), to appear by Zoom at the November 2 trial call and all further "
               "hearings or, alternatively, for a continuance. The medical record is lodged as a confidential exhibit (Tab L)."))
    F.append(P("7. Issues for trial", h2))
    for t in [
        "Whether the three-day notice states the facts constituting the alleged breach with the particularity required by Code of Civil Procedure section 1161, subdivision (3).",
        "Whether the notice was served in a manner authorized by section 1162, and whether the proof of service is true.",
        "Whether the action is retaliatory under Civil Code section 1942.5 and Government Code section 12955, subdivision (f), given the sequence of accommodation requests, the September 8, 2026 administrative complaint, the habitability complaints, and union activity.",
        "Whether plaintiff can prove the alleged conduct with admissible evidence rather than hearsay relayed by the complaining manager (Evid. Code, § 1200).",
        "Whether plaintiff breached the warranty of habitability (Civ. Code, §§ 1941, 1941.1; Green v. Superior Court (1974) 10 Cal.3d 616) and failed to accommodate defendant's disabilities.",
        "Whether, in light of the change in counsel and the challenged pleadings, plaintiff must dismiss, re-notice, and refile if it wishes to proceed.",
    ]:
        F.append(P("\u2022&nbsp;&nbsp;" + t, num))
    F.append(P("8. Relief sought", h2))
    F.append(P("Judgment for defendant; dismissal of the complaint; a finding of retaliation; attorney's fees and costs as allowed by the lease and Civil Code section 1942.5, "
               "subdivision (i); and such further relief as the Court finds proper. Defendant reserves the right to seek sanctions under Code of Civil Procedure section "
               "128.7 and to refer the proof of service to the appropriate authorities."))
    return rl_pdf(sig(F), path, "Statement of the Case")


# ======================================================================= TAB: FRAUD ANALYSIS (line by line)
def fraud_analysis(path):
    F = caption("FRAUD ANALYSIS: LINE-BY-LINE REVIEW OF THE THREE-DAY NOTICE, PROOF OF SERVICE, AND COMPLAINT")
    F.append(P("Purpose. This review takes each element of the notice, the proof of service, and the complaint in order, states what the document says, states "
               "what the record shows, and identifies the defect. Where a quotation from the notice is needed, a blank is left so the exact words can be copied in "
               "from the filed document at trial; the analysis does not depend on paraphrase.", body))

    F.append(P("Part A. The three-day notice", h2))
    rows = [["#", "Element / line of the notice", "What the notice says", "What the record shows", "Defect and authority"]]
    A = [
        ("A-1", "Caption: tenant name and premises", "Addressed to \u201c____________\u201d at Unit 301A.",
         "Tenant is Donald Ernest Gillson, Unit 301A. Any misnomer or wrong unit designation is noted here.", "Notice must identify the premises and the tenant with reasonable certainty (CCP § 1161(3)); strict compliance is required (Kwok v. Bergren (1982) 130 Cal.App.3d 596)."),
        ("A-2", "Date of notice", "Dated \u201c____________, 2026.\u201d",
         "Compare with the date of the Landrum/Gillson dispute, the Court's rule 1.100 orders, and the Sept. 8, 2026 administrative complaint. Notice issued within 180 days of protected activity.", "Civ. Code § 1942.5(a), (d): notice within 180 days of protected activity raises retaliation; landlord bears burden of a non-retaliatory reason (§ 1942.5(e))."),
        ("A-3", "Statement of the covenant breached", "Alleges, in the third person, \u201cstaff harassment\u201d / \u201cthe way that staff was treated.\u201d",
         "No staff member, date, time, place, or act is identified. No written warning, incident report, or grievance predates the notice. The only dispute was personal, between Landrum and defendant.", "CCP § 1161(3) requires the notice to state the facts of the breach so the tenant can cure or respond; a conclusory notice is insufficient (Kwok; Liebovich v. Shahrokhkhany (1997) 56 Cal.App.4th 511). A notice that cannot be cured must at minimum identify what was done."),
        ("A-4", "Cure or quit vs. unconditional quit", "Form of demand: \u201c____________.\u201d",
         "If the notice demands cure, the generalized allegation gives no act to cure. If it is an unconditional quit under § 1161(4) (nuisance/waste), the notice must allege facts amounting to nuisance; none are alleged.", "CCP § 1161(3), (4); an unconditional notice on a curable covenant is defective; a nuisance notice without facts is defective."),
        ("A-5", "Three-day period and computation", "Demands compliance within three days of service.",
         "Three days excludes Saturdays, Sundays, and judicial holidays (CCP § 1161(2)-(3) as amended by AB 2343, eff. Sept. 1, 2019). Check whether the complaint was filed before the period, properly computed from actual service, expired.", "A complaint filed before expiration of a properly computed period is premature and must be dismissed (Bevill v. Zoura (1994) 27 Cal.App.4th 694)."),
        ("A-6", "Signature block", "Signed by \u201c____________\u201d for Swords to Plowshares.",
         "Identify signer; confirm authority. Landrum is both the complaining witness and the person who prepared or caused the notice.", "A notice must be given by the landlord or an authorized agent; where the agent is the complaining party, his declaration is interested testimony to be weighed accordingly (Evid. Code § 780)."),
        ("A-7", "Attachment of lease provision", "Cites lease paragraph \u201c____________\u201d or none.",
         "Confirm the lease actually contains a covenant that the alleged conduct would breach and that the covenant is material.", "Forfeiture requires breach of a material covenant actually in the lease (Civ. Code § 1442; Boston LLC v. Juarez (2016) 245 Cal.App.4th 75)."),
        ("A-8", "Retaliation disclosure", "Silent.",
         "Notice followed rule 1.100 orders (July-Oct. 2026), the Sept. 8 administrative complaint, habitability complaints to DPH, and union activity.", "Civ. Code § 1942.5; Gov. Code § 12955(f) (retaliation for requesting accommodation); Barela v. Superior Court (1981) 30 Cal.3d 244 (retaliation defense available in UD)."),
    ]
    for r in A:
        rows.append([r[0], Paragraph(r[1], cellb), Paragraph(r[2], cell), Paragraph(r[3], cell), Paragraph(r[4], cell)])
    F.append(grid(rows, [0.4 * inch, 1.15 * inch, 1.35 * inch, 1.75 * inch, 1.75 * inch]))

    F.append(P("Part B. The proof of service of the notice", h2))
    rows = [["#", "Element / line", "What the proof says", "What the record shows", "Defect and authority"]]
    B = [
        ("B-1", "Identity of server", "Jerome Bradford executed and/or served the notice.",
         "Defendant's dated records place Bradford away from the premises at the stated time. Dwayne (resident advisor) describes an accidental delivery of unverified papers (Video V-05, 2d suite).", "A declaration of service that misstates who served, when, or how is not a proof of service at all; false declaration under penalty of perjury (CCP § 2015.5; Pen. Code § 118)."),
        ("B-2", "Date and time of service", "\u201c____________, 2026 at ____:____ __.m.\u201d",
         "Compare against building key-fob/access logs, camera footage, payroll/timekeeping, and defendant's own location record for that hour (subpoenaed, Tab H).", "Service method and timing must be proved by the landlord (CCP § 1162; Liebovich, 56 Cal.App.4th at 513-514)."),
        ("B-3", "Method of service checked", "Personal / substituted / post-and-mail: \u201c____________.\u201d",
         "If personal service is claimed and Bradford was absent, the box is false. If substituted or post-and-mail, the declaration must show the diligence and the mailing that § 1162 requires; it does not.", "CCP § 1162(a)(1)-(3): each method has mandatory steps; a declaration that omits them does not prove service."),
        ("B-4", "Witness / declarant", "William Landrum declares or witnesses service.",
         "Landrum is the complaining party. He did not personally serve. A declaration that he \u201cwitnessed\u201d service by an absent person is impossible.", "Declarations must be on personal knowledge (Evid. Code § 702); the Court may disregard an interested witness's testimony found false in part (CACI 107; Evid. Code § 780)."),
        ("B-5", "Place of service", "Unit 301A / \u201c____________.\u201d",
         "Dwayne's account suggests papers were left with or by staff, not delivered to defendant.", "Delivery to a staff member is not service on the tenant under § 1162."),
        ("B-6", "Mailing declaration", "Mailed on \u201c____________\u201d / not stated.",
         "No mailing envelope or postmark has been produced.", "Where posting or substituted service is used, mailing is mandatory and must be declared (CCP § 1162(a)(2), (3))."),
        ("B-7", "Signature / penalty of perjury", "Signed by \u201c____________\u201d under penalty of perjury.",
         "If the declarant did not do or observe what is declared, the declaration is false when signed.", "CCP § 2015.5; Pen. Code § 118; CCP § 128.7(b)(3) as to counsel who files it."),
    ]
    for r in B:
        rows.append([r[0], Paragraph(r[1], cellb), Paragraph(r[2], cell), Paragraph(r[3], cell), Paragraph(r[4], cell)])
    F.append(grid(rows, [0.4 * inch, 1.15 * inch, 1.35 * inch, 1.75 * inch, 1.75 * inch]))

    F.append(P("Part C. The complaint and the papers that followed", h2))
    rows = [["#", "Element / line", "What the paper says", "What the record shows", "Defect and authority"]]
    C = [
        ("C-1", "Verification", "Verified by \u201c____________\u201d (officer / attorney).",
         "If verified by counsel, the verification is on information and belief and carries no personal knowledge of service.", "CCP § 1166(a)(1) requires a verified UD complaint; attorney verification is permitted only when the party is absent from the county (CCP § 446) and must say so."),
        ("C-2", "Attachment of notice and proof", "Notice and proof of service attached as Exhibit \u201c__.\u201d",
         "Compare the attached copies against the copy actually left for defendant for differences in date, text, signature, or service boxes.", "CCP § 1166(d)(1)(A) requires the notice to be attached; a variance between the served and filed versions is itself evidence of fabrication."),
        ("C-3", "Allegation of service", "Alleges service on \u201c____________\u201d by \u201c____________.\u201d",
         "Must match the proof; any inconsistency is noted here.", "Plaintiff must plead and prove service (CCP § 1166(a)(5))."),
        ("C-4", "Signing attorney", "Signed by John P. Zanghi, Esq.",
         "Mr. Zanghi has been or is being removed from the case. No substitution has been served on defendant.", "CCP §§ 284, 285 (substitution must be filed and noticed); CCP § 128.7(a) (signature is certification); a successor cannot adopt a challenged false declaration without inquiry (Bus. & Prof. Code § 6068(d); Rules Prof. Conduct 3.3)."),
        ("C-5", "Discovery", "Defendant's special interrogatories and demands for production served; no responses.",
         "Plaintiff has produced nothing about who served, when, or what staff complaint existed.", "CCP §§ 2030.290, 2031.300: waiver of objections; evidence sanctions available (§ 2023.030); inference from failure to produce (Evid. Code § 412)."),
        ("C-6", "Dept. 505 document drop", "A box of documents deposited on defendant with no index or proof of service.",
         "Violates the Court's rule 1.100 orders requiring written, accessible communication.", "CRC 1.100; Gov. Code § 11135; 42 U.S.C. § 12132."),
        ("C-7", "Oct. 30, 2026 e-service", "Proceed Legal eService notice and order confirmation, CUD-26-682107.",
         "Content of the filing not yet reviewed in this binder; to be matched against the docket at trial call.", "Any paper filed after the challenge to service that repeats the service allegation is a further § 128.7 certification."),
    ]
    for r in C:
        rows.append([r[0], Paragraph(r[1], cellb), Paragraph(r[2], cell), Paragraph(r[3], cell), Paragraph(r[4], cell)])
    F.append(grid(rows, [0.4 * inch, 1.15 * inch, 1.35 * inch, 1.75 * inch, 1.75 * inch]))

    F.append(P("Part D. Conclusion of the review", h2))
    F.append(P("The notice fails for want of particularity (A-3, A-4). The proof of service is contradicted by the absence of the named server, by the account of "
               "plaintiff's own resident advisor, and by the interested position of the declarant (B-1, B-4, B-5). The complaint rests on both and was signed by an "
               "attorney who is leaving the case (C-4). None of these defects can be cured by amendment; the remedy is dismissal, and if plaintiff wishes to proceed, "
               "a new notice, truthfully served and declared, and a new verified complaint signed by the attorney who will try the case. The blanks above are to be "
               "completed from the filed documents at trial and the completed sheet offered as a demonstrative."))
    return rl_pdf(sig(F), path, "Fraud Analysis")


# ======================================================================= TAB: POINTS AND AUTHORITIES
def points_authorities(path):
    F = caption("MEMORANDUM OF POINTS AND AUTHORITIES")
    F.append(P("I. The three-day notice is insufficient under Code of Civil Procedure section 1161 and cannot support judgment", h2))
    F.append(P("Unlawful detainer is a summary statutory remedy, and the statutory requirements are strictly construed against the landlord. A notice that does not comply "
               "with section 1161 is void and will not support a judgment. (<i>Kwok v. Bergren</i> (1982) 130 Cal.App.3d 596, 599-600; <i>Liebovich v. Shahrokhkhany</i> (1997) "
               "56 Cal.App.4th 511, 513; <i>Bevill v. Zoura</i> (1994) 27 Cal.App.4th 694, 697.) Section 1161, subdivision (3), requires a notice based on breach of covenant to "
               "state the facts constituting the breach so that the tenant can cure or respond. A third-person recital of \u201cstaff harassment\u201d that names no person, "
               "date, or act does not state any fact. The defect goes to the sufficiency of the notice itself and is tested at trial or on demurrer, not by motion to quash "
               "(<i>Borsuk v. Appellate Division</i> (2015) 242 Cal.App.4th 607, 612-613); defendant raises it as a complete defense."))
    F.append(P("II. Plaintiff must prove service as declared; a false proof of service is no proof", h2))
    F.append(P("The landlord bears the burden of proving that the notice was served by a method authorized by section 1162. (<i>Liebovich</i>, 56 Cal.App.4th at 513-514; "
               "<i>Palm Property Investments, LLC v. Yadegar</i> (2011) 194 Cal.App.4th 1419, 1425.) Each method in section 1162, subdivision (a), has mandatory steps. A declaration "
               "reciting personal delivery by a person who was not present is not a mistake of form; it is a false statement under penalty of perjury (Code Civ. Proc., § 2015.5; "
               "Pen. Code, § 118). The trier of fact may reject the whole of a witness's testimony when it finds he has deliberately testified falsely in part (Evid. Code, § 780; "
               "CACI No. 107), and may draw an adverse inference from a party's failure to produce the records within its control that would resolve the question (Evid. Code, § 412). "
               "Plaintiff has produced no access logs, footage, or timekeeping records despite written discovery and subpoena."))
    F.append(P("III. The action is retaliatory", h2))
    F.append(P("Civil Code section 1942.5, subdivision (a), prohibits a lessor from serving a notice to quit or bringing an action to recover possession within 180 days after the "
               "tenant has complained to a public agency about habitability, or has lawfully organized or participated in a tenants' association (subd. (d)), or has exercised "
               "any right under the law. Government Code section 12955, subdivision (f), separately prohibits retaliation against a person for requesting a reasonable accommodation. "
               "Retaliation is a defense in unlawful detainer (<i>Barela v. Superior Court</i> (1981) 30 Cal.3d 244, 249-251; <i>Schweiger v. Superior Court</i> (1970) 3 Cal.3d 507). "
               "The notice followed the Court's rule 1.100 orders of July through October 2026, defendant's September 8, 2026 administrative complaint, his complaints to the "
               "Department of Public Health, and his union activity. The landlord must then prove a legitimate, non-retaliatory reason by a preponderance (§ 1942.5, subd. (e)); "
               "an anonymous, undocumented \u201cstaff\u201d complaint relayed by the manager who is himself the complaining party does not meet that burden. A tenant who prevails "
               "recovers reasonable attorney's fees and costs (§ 1942.5, subd. (i))."))
    F.append(P("IV. Hearsay cannot prove the alleged conduct", h2))
    F.append(P("Evidence of a statement made other than by a witness while testifying, offered to prove the truth of the matter stated, is inadmissible (Evid. Code, § 1200). "
               "Statements of unidentified staff relayed by Mr. Landrum or counsel are hearsay with no applicable exception. Business records require foundation that the record was "
               "made at or near the event in the regular course of business (Evid. Code, § 1271); no contemporaneous record exists. Defendant objects in advance to any such testimony."))
    F.append(P("V. Breach of the warranty of habitability and failure to accommodate", h2))
    F.append(P("Every residential lease carries an implied warranty of habitability (<i>Green v. Superior Court</i> (1974) 10 Cal.3d 616, 637), and a dwelling infested with vermin or "
               "lacking sanitary plumbing is untenantable (Civ. Code, § 1941.1, subds. (a)(1), (a)(6)). Exhibits 1-20 and 45-56 document the conditions and the landlord's notice of them. "
               "A housing provider must also make reasonable accommodations necessary to afford a disabled tenant equal use and enjoyment (Gov. Code, § 12927, subd. (c)(1); 42 U.S.C. "
               "§ 3604(f)(3)(B)); interference with a service animal and refusal of written-only communication are failures to accommodate. These facts support both the defense "
               "and a cross-claim, which defendant reserves."))
    F.append(P("VI. Substitution of counsel; the pleadings must be re-executed and the action re-noticed and refiled", h2))
    F.append(P("An attorney may be changed only by consent of client and attorney filed with the clerk, or by court order, and written notice of the change must be given to the adverse "
               "party; until then the former attorney must be recognized (Code Civ. Proc., §§ 284, 285). Every pleading must be signed by an attorney of record, and the signature "
               "certifies that the factual contentions have evidentiary support (Code Civ. Proc., § 128.7, subds. (a), (b)(3)). An unlawful detainer complaint must be verified (§ 1166, "
               "subd. (a)(1)). An attorney may not seek to mislead the court by a false statement of fact and may not offer evidence he knows to be false (Bus. & Prof. Code, § 6068, "
               "subd. (d); Rules Prof. Conduct, rule 3.3(a)(1), (3)). If Mr. Zanghi is removed, Mr. Torres cannot proceed on a complaint and proof of service he did not sign and that are "
               "challenged as false without making his own inquiry and his own certification. And because the defects lie in the notice and its service, amendment cannot cure them: "
               "the only course is dismissal, a new notice that complies with sections 1161 and 1162, and a new verified complaint. (<i>Kwok</i>, 130 Cal.App.3d at 600; <i>Bevill</i>, "
               "27 Cal.App.4th at 697.) Any new notice will be measured against section 1942.5."))
    F.append(P("VII. Remote appearance and accommodation", h2))
    F.append(P("The Court must grant reasonable accommodation to a person with a disability unless it would create an undue burden or fundamentally alter the proceeding (Cal. Rules of "
               "Court, rule 1.100(f); Gov. Code, § 11135; 42 U.S.C. § 12132). Remote appearance in civil matters is authorized by Code of Civil Procedure section 367.75. Defendant is under "
               "medical orders to rest through at least November 4, 2026 with follow-up at Travis AFB; he has requested, by MC-410, to appear by Zoom or in the alternative a short continuance "
               "(§ 1170.5, subd. (c), good cause). The Court has already granted remote appearance in this case."))
    F.append(P("VIII. Sanctions and referral", h2))
    F.append(P("Presenting a paper to the court for an improper purpose or with factual contentions lacking evidentiary support is sanctionable (Code Civ. Proc., § 128.7, subds. (b), (c)), "
               "subject to the 21-day safe harbor, which the Notice to Counsel at Tab H begins. Defendant reserves referral of the proof of service under Penal Code section 118 and of "
               "counsel's conduct to the State Bar."))
    F.append(P("IX. Conclusion", h2))
    F.append(P("The notice is insufficient, the service is unproved and contradicted, the motive is retaliatory, and the proof offered is hearsay. Judgment should be entered for defendant, "
               "with fees and costs. If plaintiff wishes to pursue possession, it must dismiss, re-notice in compliance with the statute, and refile through counsel who will actually "
               "sign and appear."))
    return rl_pdf(sig(F), path, "Points and Authorities")


# ======================================================================= TAB: WITNESS LIST
def witness_list(path):
    F = caption("DEFENDANT'S WITNESS LIST AND STATEMENT OF EXPECTED TESTIMONY")
    F.append(P("Each witness is listed with the reason he or she is called and the exhibits through which the testimony will be presented. Witnesses marked (S) are under "
               "trial subpoena duces tecum (Tab H). Witnesses marked (V) appear on video exhibits (Tab G) and are called to authenticate and to be examined on their recorded statements.", body))
    W = [
        ("William Landrum (S)(V)", "Assistant Property Manager, Swords to Plowshares, 1030 Girard Rd.",
         "Adverse. Declarant/witness on the proof of service; the person with whom the only actual dispute occurred; prepared or caused the notice to issue; gave an account to the SF Housing Authority that omitted the dispute. Examined on: what he personally saw of service; whether Bradford was present; what written complaint existed before the notice; his hostility on video (2d suite V-01, V-04, V-06).", "Notice; proof of service; Exs. 45-52; Video V-01, V-04, V-06 (2d)"),
        ("Jerome Bradford (S)", "Property/operations staff, Swords to Plowshares",
         "Adverse. Named as the person who executed and/or served the notice. Examined on his whereabouts at the declared date and time, who told him to sign, and what he actually did with the papers. Key-fob, schedule, and payroll records subpoenaed.", "Proof of service; subpoenaed logs"),
        ("\u201cDwayne\u201d (surname to be confirmed) (S)(V)", "Resident Advisor, Swords to Plowshares, 1030 Girard Rd.",
         "On video he describes the accidental delivery of unverified legal papers and management's disorganized service practices (V-05, 2d suite) and management instructions and selective enforcement (V-03, 2d suite). Called to authenticate the recordings and confirm the account under oath. Directly contradicts the proof of service.", "Video V-03, V-05 (2d)"),
        ("Francisco G. Torres, Esq. (S)", "Partner, Zanghi Torres Adams LLP; counsel for plaintiff",
         "Custodian of the notice, proof of service, and firm communications about their preparation and service; recipient of the Oct. 29-30, 2026 evidentiary notices and author of same-day replies; stated the basis for eviction as \u201cthe way staff was treated.\u201d Called on records, not strategy; privilege log requested.", "Tab H notices; mailbox log"),
        ("John P. Zanghi, Esq. (S)", "Partner, Zanghi Torres Adams LLP; signing attorney on complaint",
         "Signed the complaint; served with the Court's rule 1.100 orders; directed the Dept. 505 document drop. If removed from the case, called on the circumstances of removal and on what he knew about service when he signed.", "Complaint; Tab I orders"),
        ("Custodian of Records, Swords to Plowshares (attn. Michael Blecker, Exec. Dir.) (S)", "Plaintiff",
         "Tenant file, ledger, maintenance and pest-control records, staff incident reports (or their absence), communications with SFHA/HUD-VASH/SSVF, access-control and camera records for the date of claimed service.", "Subpoena, Tab H"),
        ("Custodian of Records, SF Dept. of Public Health, Environmental Health (S)", "Non-party agency",
         "Inspection file for 311 Case No. 101003004371: independent proof of conditions and of defendant's protected complaint.", "Exs. 53-56"),
        ("Custodian of Records / ADA Coordinator Joy Guandique, SF Superior Court (S)", "Court administrative office",
         "Dates and dispositions of each rule 1.100 request and transmittal of orders to plaintiff's counsel; establishes protected-activity timeline and counsel's notice.", "Tab I"),
        ("Jeffrey Tims and Regina Gibson", "Adult Protective Services caseworkers (current)",
         "Confirm defendant is a dependent adult with an open, reopened APS case; conditions reported; crisis intervention (Video V-07, 1st suite). Supports vulnerability and the Elder/Dependent Adult protections.", "Video V-07 (1st); binder statement"),
        ("Drew Yorkov", "Former APS caseworker",
         "Assigned during the period of the exhibits; failed to act; called only if plaintiff disputes the APS history.", "Binder statement"),
        ("HUD-VASH / SSVF Case Manager (name to be confirmed) (V)", "VA / program case manager",
         "Crisis intervention, APS notification, suicide-prevention protocol (V-07, 1st suite); knowledge of accommodation requests to the landlord.", "Video V-07 (1st)"),
        ("Custodian of Records, San Francisco Housing Authority (HUD-VASH)", "Non-party agency",
         "The account Mr. Landrum gave the Authority about defendant and what it omitted.", "Subpoena to be issued"),
        ("Officer(s), U.S. Park Police", "Law enforcement, Presidio",
         "Vehicle break-in report Dec. 25, 2025 (Exs. 57-65); security conditions at the premises.", "Exs. 57-65"),
        ("Custodians of Records: UCSF Health; John Muir Health Concord ED; VA / David Grant USAF Medical Center", "Medical providers",
         "Authenticate records of Nov. 26 and Dec. 9, 2025 (Exs. 31, 39-44) and Oct. 30, 2026 (Tab L); establish injuries, functional status, and the medical basis for remote appearance. Offered under seal or redacted.", "Exs. 31, 39-44; Tab L"),
        ("Veterinary provider (Dec. 11, 2025)", "Treating veterinarian for service dog Jaxx",
         "Bite injuries and treatment consistent with infestation (Exs. 25-27).", "Exs. 21-27"),
        ("Members, San Francisco Veterans Tenants Union (two to three, names on separate confidential list)", "Residents of 1030 Girard Rd.",
         "Staff threats to \u201ckick their ass,\u201d selective enforcement, retaliation against union participants; collective awareness of the recordings (Notices 3 and 4, Tab H).", "Tab H Notices 3-4; Video suites"),
        ("Kolby Losik; Mark Villalobos", "Program clinicians, subjects of BBS complaints Jan. 2, 2026",
         "Called only if plaintiff relies on clinical or behavioral characterizations of defendant; their conduct is the subject of pending Board complaints (Exs. 77-78).", "Exs. 77-78"),
        ("Itzayana Flores; Nicholas P. Wagener", "Zanghi Torres Adams LLP",
         "Firm personnel involved in filings and service; subjects of defendant's State Bar complaint notice of Oct. 30, 2026. Called only on records of service and the Dept. 505 delivery.", "Mailbox log, Tab G"),
        ("Dr. Donny Gillson, Ed.D.", "Defendant",
         "Conditions, notices, injuries, accommodation requests, the Landrum dispute, what actually happened on the date of claimed service, and authentication of Exs. 1-78 and the video suites. Will testify by Zoom under the Court's rule 1.100 orders.", "All"),
    ]
    rows = [["Witness", "Capacity", "Why called / expected testimony", "Exhibits"]]
    for w in W:
        rows.append([Paragraph(w[0], cellb), Paragraph(w[1], cell), Paragraph(w[2], cell), Paragraph(w[3], cell)])
    F.append(grid(rows, [1.35 * inch, 1.2 * inch, 2.75 * inch, 1.1 * inch]))
    F.append(Spacer(1, 8))
    F.append(P("Defendant reserves the right to call any witness listed by plaintiff and rebuttal witnesses. Addresses for subpoenaed witnesses appear in the Service Directory at Tab H.", small))
    return rl_pdf(sig(F), path, "Witness List")


# ======================================================================= TAB: EVIDENCE LIST
def evidence_list(path):
    F = caption("DEFENDANT'S EVIDENCE LIST (DOCUMENTARY AND PHOTOGRAPHIC)")
    F.append(P("Exhibits 1-78 are reproduced in full in the Evidence Exhibit Binder at Tab J, each with device filename, capture timestamp, dimensions, size, and SHA-256 hash. "
               "Court orders are at Tab I; the confidential medical exhibit is at Tab L; video exhibits are listed separately at Tab G.", body))
    cats = [
        ("A", "Written notices and grievances to management", "1-2", "11/16/2025", "Notice to landlord of conditions; start of protected activity; Civ. Code §§ 1942, 1942.5."),
        ("B", "Cockroach infestation and unsanitary conditions in the unit", "3-20", "11/16/2025 - 01/05/2026", "Habitability (Civ. Code § 1941.1); conditions persisted after treatment (Exs. 17-20)."),
        ("C", "Injuries to service animal Jaxx", "21-27", "11/18/2025 - 12/11/2025", "Harm from conditions; service-animal interference; damages."),
        ("D", "Injuries to defendant and medical records", "28-44", "11/18/2025 - 12/09/2025", "UCSF visit 11/26/2025 (Ex. 31); ED visit 12/09/2025 with concussion and cervical sprain discharge (Exs. 34-44); baseline functional status."),
        ("E", "Correspondence from Swords to Plowshares management", "45-52", "11/19/2025 - 01/04/2026", "Landlord's knowledge; absence of any complaint about defendant's conduct toward staff in the same period."),
        ("F", "Government agency records and reports", "53-56", "11/20/2025 - 12/18/2025", "DPH 311 Case 101003004371; protected complaints to public agencies."),
        ("I", "Vehicle break-in reported to U.S. Park Police", "57-65", "12/25/2025", "Security conditions; damages."),
        ("G", "Defendant's contemporaneous digital notes and messages", "66-69", "11/20/2025", "Contemporaneous record; Evid. Code § 1237 (past recollection recorded)."),
        ("H", "Building common areas and repair activity", "70-71", "12/26/2025", "Repairs undertaken after complaints; admission of conditions."),
        ("J", "Evidentiary notices served on counsel Oct. 29, 2026 and forwarded to Dept. 606 Oct. 30, 2026", "72-76", "10/29/2026 - 10/30/2026", "Notice to plaintiff of video exhibits and preservation demand; counsel's same-day replies."),
        ("K", "Complaints to Board of Behavioral Sciences", "77-78", "01/02/2026", "Protected complaints to a licensing agency; context for program hostility."),
    ]
    rows = [["Cat.", "Subject", "Exs.", "Dates", "Purpose / relevance"]]
    for c in cats:
        rows.append([c[0], Paragraph(c[1], cellb), c[2], Paragraph(c[3], cell), Paragraph(c[4], cell)])
    F.append(grid(rows, [0.45 * inch, 2.0 * inch, 0.6 * inch, 1.15 * inch, 2.2 * inch]))
    F.append(P("Court records and filings", h2))
    rows = [["Item", "Description", "Location", "Purpose"]]
    items = [
        ("CR-1", "SF Superior Court rule 1.100 orders and responses, July 20 - Oct. 14, 2026 (20 documents)", "Tab I", "Protected-activity timeline; Court-ordered accommodations; counsel's notice."),
        ("CR-2", "Three-day notice and proof of service (plaintiff's exhibit; to be marked from the court file)", "Court file", "Subject of Fraud Analysis, Tab C."),
        ("CR-3", "Complaint, CUD-26-682107, signed by J. Zanghi (court file)", "Court file", "Verification, attachment of notice, signing attorney."),
        ("CR-4", "Defendant's special interrogatories and demands for production; proof of service; no responses", "Defendant's file", "Waiver of objections; adverse inference."),
        ("CR-5", "Proceed Legal eService notice and order confirmation, Oct. 30, 2026", "Tab G log", "Plaintiff's post-notice filing."),
        ("CR-6", "Notice to Francisco Torres, Esq. re fraudulent service, retaliation, hearsay, medical chronology, and substitution/refiling, Oct. 31, 2026", "Tab H", "Safe-harbor notice; preservation demand."),
        ("CR-7", "Civil subpoenas duces tecum (SUBP-002) to seven witnesses with Attachment 3", "Tab H", "Records of service, staff complaints, habitability, ledger, ADA file."),
        ("CR-8", "MC-410 Request for Accommodations (SF, Dept. 606) with attachment", "Tab H", "Remote appearance / continuance."),
        ("CR-9", "BBS complaint summaries 2002026002097 and 2002026002098", "Tab K", "Protected complaints."),
        ("CR-10", "CONFIDENTIAL: John Muir Health ED record Oct. 30, 2026 and wristband photographs", "Tab L (sealed)", "Medical basis for remote appearance; CRC 1.100(c)(4)."),
    ]
    for it in items:
        rows.append([it[0], Paragraph(it[1], cell), Paragraph(it[2], cell), Paragraph(it[3], cell)])
    F.append(grid(rows, [0.55 * inch, 3.0 * inch, 1.0 * inch, 1.85 * inch]))
    F.append(P("Authentication. Photographs and screenshots: Evid. Code §§ 1400-1401, 250, 1552-1553 (printed representations of digital images presumed accurate), with the "
               "declarant's testimony. Court records: Evid. Code §§ 452(d), 1530. Business and public records: Evid. Code §§ 1271, 1280, 1560-1562 (custodian declarations under subpoena).", small))
    return rl_pdf(sig(F), path, "Evidence List")


# ======================================================================= TAB: VIDEO LIST
def video_list(path):
    F = caption("DEFENDANT'S VIDEO AND AUDIO EXHIBIT LIST")
    F.append(P("Two suites of recordings were designated as trial exhibits by formal notice served on Zanghi Torres Adams LLP on October 29, 2026 and forwarded to Department 606 "
               "on October 30, 2026 (Exs. 72-76). Recordings are hosted in a Google Drive repository at the links below; native files with metadata are preserved on the "
               "recording device and will be lodged on USB media at trial. Each recording was made by defendant or at an authorized meeting of the San Francisco Veterans Tenants "
               "Union in common areas or exterior grounds where no reasonable expectation of privacy existed (Pen. Code, § 632; Notice 4, Tab H). Foundation: Evid. Code §§ 250, "
               "1400-1401, 1553; <i>People v. Goldsmith</i> (2014) 59 Cal.4th 258, 267-268.", body))
    for n_i, (title, idx) in enumerate([("First suite (served 10/29/2026, 11:00 PM): Exhibits V-01 through V-07", 0), ("Second suite (served 10/29/2026, 11:21 PM): Exhibits V-01 through V-06", 1)]):
        F.append(P(title, h2))
        rows = [["Ex.", "Title", "Description / what it proves", "Witness(es)", "Repository link"]]
        for code, t, url, d in NOTICES[idx]["videos"]:
            who = {"V-01": "Gillson; Landrum", "V-02": "Gillson", "V-03": "Gillson; Dwayne" if idx == 1 else "Gillson; case manager",
                   "V-04": "Gillson; Landrum" if idx == 1 else "Gillson; process server", "V-05": "Gillson; Dwayne" if idx == 1 else "Gillson",
                   "V-06": "Gillson; staff" if idx == 1 else "Gillson", "V-07": "Gillson; case manager; APS"}[code]
            rows.append([f"{'1st' if idx == 0 else '2d'} {code}", Paragraph(t, cellb), Paragraph(d, cell), Paragraph(who, cell),
                         Paragraph(f'<link href="{url}"><font color="blue">{url.replace("https://drive.google.com/file/d/", "drive.google.com/.../")[:40]}</font></link>', cell)])
        F.append(grid(rows, [0.6 * inch, 1.35 * inch, 2.35 * inch, 0.95 * inch, 1.15 * inch]))
    F.append(P("Key recordings for the service question", h2))
    F.append(P("Second suite V-05 (Dwayne: accidental delivery of unverified legal papers; chaotic service practices) and V-03 (Dwayne: management instructions and selective "
               "enforcement) go directly to whether the proof of service is true. Second suite V-01 and V-04 (Landrum's hostility and verbal assault) establish that the only dispute "
               "was personal and that Landrum is an interested declarant. First suite V-04 (process server confrontation at the courthouse) bears on the firm's service practices generally."))
    F.append(P("Publication plan", h2))
    F.append(P("Clips will be cued by exhibit number and time-stamp; a clip log with start/stop times will be served before trial. Transcripts of audible statements will be provided for "
               "the Court's convenience and are not themselves offered as evidence. Full-length files remain available to plaintiff at the links served October 29, 2026."))
    F.append(P("Transmission log (defendant's mailbox, Oct. 29-30, 2026)", h2))
    from notices import MAILBOX_ROWS, FORWARD
    rows = [["Date", "From", "Subject"]]
    for n in NOTICES:
        rows.append(["Oct 29", Paragraph("donny@18fu.ai to ftorres@ztalaw.com; jzanghi@ztalaw.com", cell), Paragraph(n["sent"].split(" at ")[1] + " - " + n["subject"], cell)])
    rows.append(["Oct 30", Paragraph(FORWARD["from"] + " to " + FORWARD["to"], cell), Paragraph(FORWARD["sent"].split(" at ")[1] + " - " + FORWARD["subject"], cell)])
    for d, f, s in MAILBOX_ROWS:
        rows.append([d, Paragraph(f, cell), Paragraph(s, cell)])
    F.append(grid(rows, [0.55 * inch, 1.9 * inch, 3.95 * inch]))
    return rl_pdf(sig(F), path, "Video List")


# ======================================================================= TAB: CLOSING ARGUMENT
def closing_argument(path):
    F = caption("DEFENDANT'S CLOSING ARGUMENT (OUTLINE FOR DELIVERY)")
    F.append(P("1. What this case is", h2))
    F.append(P("Your Honor, this is a case about a piece of paper. Swords to Plowshares asks the Court to take a disabled veteran's home on the strength of a three-day notice "
               "and a proof of service. Everything else in this trial, every characterization of how staff were treated, rests on those two documents. If they do not hold, "
               "nothing else matters."))
    F.append(P("2. The notice does not say what I did", h2))
    F.append(P("Read the notice. It says \u201cstaff harassment.\u201d It does not say which staff member, on what day, in what place, or what was said or done. The law requires the "
               "notice to state the facts of the breach so that the tenant can answer it. (Code Civ. Proc., § 1161(3); <i>Kwok</i>; <i>Liebovich</i>.) A notice that could be served on "
               "any tenant in the building, on any day, is not notice of anything. Counsel's own explanation, \u201cthe way that staff was treated,\u201d is not a fact; it is an opinion "
               "from someone who was not there."))
    F.append(P("3. The proof of service is not true", h2))
    F.append(P("The proof of service says Jerome Bradford served the notice, and William Landrum declares to it. The evidence is that Mr. Bradford was not there. Plaintiff's own "
               "resident advisor, Dwayne, on video, says the papers were delivered by accident. Plaintiff had every record that could have proved its account: key-fob logs, camera "
               "footage, timesheets, the text message that told someone to go serve the notice. It was asked for in discovery and by subpoena. It produced none of it. The Court is "
               "entitled to infer that the records would not have helped plaintiff. (Evid. Code, § 412.) And the Court may disbelieve all of a witness who has sworn falsely in part. "
               "(Evid. Code, § 780; CACI No. 107.) Mr. Landrum is the person I had a disagreement with. He wrote the notice. He signed the proof. He is the \u201cstaff.\u201d"))
    F.append(P("4. The timing tells the Court why", h2))
    F.append(P("Look at the calendar. From July 20 to October 14, 2026 this Court issued twenty orders and responses on my requests for accommodation. On September 8 I filed a formal "
               "administrative complaint. Before that, I complained to the Department of Public Health about cockroaches, and I organized a tenants' union. Then the notice came. "
               "The statute says a notice within 180 days of those acts is presumed retaliatory and the landlord must prove a real reason. (Civ. Code, § 1942.5.) The real reason "
               "offered is an anonymous staff complaint that no one wrote down before the notice issued."))
    F.append(P("5. What plaintiff's evidence is", h2))
    F.append(P("Plaintiff's evidence of my conduct is what Mr. Landrum says unidentified staff said. That is hearsay. (Evid. Code, § 1200.) There is no incident report, no "
               "warning letter, no grievance response, no notice to cure. In a supportive-housing program with case managers and clinicians on site, the absence of a single "
               "contemporaneous writing is not an oversight; it is the evidence."))
    F.append(P("6. The conditions", h2))
    F.append(P("Exhibits 1 through 71 are dated photographs of the unit, the glue traps, the sink, the bites on my service dog, and my own injuries, with hospital records from "
               "November 26 and December 9, 2025. Management's letters show they knew. The Department of Public Health opened a case. That is the tenancy plaintiff now says "
               "I disrupted."))
    F.append(P("7. Counsel", h2))
    F.append(P("The complaint was signed by Mr. Zanghi. He is leaving the case. Mr. Torres cannot inherit a declaration of service he did not sign and that is contradicted by "
               "his client's own staff, and simply proceed on it. If plaintiff believes it has grounds, the law gives it a path: dismiss, serve a notice that says what happened "
               "and is served the way the statute requires, and file a new verified complaint signed by the lawyer who will stand before the Court. What the law does not allow "
               "is judgment on this notice and this proof."))
    F.append(P("8. What I ask", h2))
    F.append(P("Judgment for defendant. A finding that the notice is insufficient and service unproved. A finding of retaliation under section 1942.5, with fees and costs. "
               "And a direction that if plaintiff proceeds, it does so on a new notice, truthfully served. I have appeared by Zoom under this Court's orders because I am under "
               "medical orders to rest; I thank the Court for the accommodation. Thank you."))
    F.append(P("Objections to have ready", h2))
    for t in ["Hearsay (Evid. Code § 1200) to any account of what staff said.", "Lack of personal knowledge (Evid. Code § 702) to Landrum on service.",
              "Lack of foundation / business-records (Evid. Code § 1271) to any after-the-fact incident report.",
              "Relevance and Evid. Code § 352 to any characterization of defendant's mental health; medical content is confidential (CRC 1.100(c)(4)).",
              "Secondary evidence (Evid. Code § 1521) if plaintiff offers a copy of the notice that differs from the one served."]:
        F.append(P("\u2022&nbsp;&nbsp;" + t, num))
    return rl_pdf(F, path, "Closing Argument")


# ======================================================================= TAB: TABLE OF CONTENTS (as its own tab; the detailed Bates TOC follows it)
def toc_intro(path, tabs):
    F = caption("TABLE OF CONTENTS")
    rows = [["Tab", "Contents", "Use at trial"]]
    for t in tabs:
        rows.append([t[0], Paragraph(t[1], cellb), Paragraph(t[2], cell)])
    F.append(grid(rows, [0.5 * inch, 3.4 * inch, 2.5 * inch]))
    F.append(Spacer(1, 10))
    F.append(P("A detailed index with Bates ranges follows this page. The Solano County MC-410 and accommodation papers are kept in a separate binder and are not included here. "
               "Tab L is confidential under California Rules of Court, rule 1.100(c)(4), and Civil Code section 56 et seq.; it is to be lodged under seal and removed from any copy served on plaintiff.", small))
    return rl_pdf(F, path, "Table of Contents")


if __name__ == "__main__":
    os.system(f"cd {HERE} && python3 build_notice_torres.py")
    print("documents")
    soc = statement_of_case(os.path.join(TMP, "m_soc.pdf"))
    fraud = fraud_analysis(os.path.join(TMP, "m_fraud.pdf"))
    pa = points_authorities(os.path.join(TMP, "m_pa.pdf"))
    wl = witness_list(os.path.join(TMP, "m_wl.pdf"))
    el = evidence_list(os.path.join(TMP, "m_el.pdf"))
    vl = video_list(os.path.join(TMP, "m_vl.pdf"))
    ca = closing_argument(os.path.join(TMP, "m_ca.pdf"))
    med_ex = medical_exhibit(os.path.join(TMP, "medical_exhibit.pdf"))

    print("MC-410 (SF)")
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", "CUD-26-682107",
                       "Superior Court of California, County of San Francisco – Dept. 606 (Hon. Stephen M. Murphy)",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further hearings in this case.", "Defendant", "Unlawful detainer", "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    m = fitz.open(); m.insert_pdf(fitz.open(mc_sf[0])); m.insert_pdf(fitz.open(mc_sf[1])); mcp = os.path.join(TMP, "mc_sf_merged.pdf"); m.save(mcp); m.close()

    sub_items = []
    for w in WITNESSES:
        print("subpoena", w["tag"])
        parts = make_subpoena(w)
        m = fitz.open()
        for p in parts:
            m.insert_pdf(fitz.open(p))
        mp = os.path.join(TMP, f"m_subp_{w['tag']}.pdf"); m.save(mp); m.close()
        sub_items.append((f"Civil Subpoena (Duces Tecum) – {w['name']}", mp))
    dir_rows = [["Witness", "Capacity", "Service address"]] + [[Paragraph(w["name"], cell), Paragraph(w["role"], cell), Paragraph(w["addr"], cell)] for w in WITNESSES]
    svc = rl_pdf([P("SUBPOENA SERVICE DIRECTORY AND SERVICE LOG", h1),
                  P("Case No. CUD-26-682107, Dept. 606, trial call November 2, 2026, 9:00 a.m. Subpoenas must be issued by the clerk before service and personally served with witness "
                    "fees tendered on demand (Code Civ. Proc., §§ 1985, 1987; Gov. Code, § 68093). Serve each subpoena with its Attachment 3 and file the proof of service with Dept. 606.", small),
                  Spacer(1, 8), grid(dir_rows, [2.0 * inch, 2.1 * inch, 2.15 * inch]), Spacer(1, 12), P("Service log", h2),
                  grid([["Witness", "Date/time served", "Served by", "Fees", "Proof filed"]] + [[w["name"].split(",")[0], "", "", "", ""] for w in WITNESSES],
                       [2.05 * inch, 1.15 * inch, 1.15 * inch, 0.95 * inch, 0.95 * inch])], os.path.join(TMP, "m_service_dir.pdf"))

    ada_items = [(f"Ex. CR-1.{i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]

    TABS = [
        ("A", "Table of Contents", "Orientation; detailed Bates index follows."),
        ("B", "Statement of the Case", "Opening; hand to the Court at trial call."),
        ("C", "Fraud Analysis: line-by-line review of the three-day notice, proof of service, and complaint", "Cross-examination of Landrum and Bradford; demonstrative."),
        ("D", "Memorandum of Points and Authorities (notice, service, retaliation, hearsay, habitability, substitution of counsel and refiling, remote appearance, sanctions)", "Legal argument; file with trial brief."),
        ("E", "Witness List with reasons for calling each witness", "Trial management; subpoena follow-up."),
        ("F", "Evidence List (documentary and photographic) with purpose and authentication", "Marking exhibits."),
        ("G", "Video and Audio Exhibit List (two suites, 13 recordings) with transmission log", "Publication of clips; foundation."),
        ("H", "Filings and Service: Notice to Counsel (Oct. 31, 2026); Service Directory; seven SUBP-002 subpoenas with Attachment 3; MC-410 (SF)", "Serve and file."),
        ("I", "San Francisco Superior Court rule 1.100 orders and responses, July-October 2026 (20 documents)", "Protected-activity timeline."),
        ("J", "Evidence Exhibit Binder: Exhibits 1-78 (photographs, notices, agency records, BBS complaints)", "Exhibits for admission."),
        ("K", "Related Administrative Complaints (Board of Behavioral Sciences)", "Protected complaints."),
        ("L", "CONFIDENTIAL Medical Exhibit (John Muir Health ED, Oct. 30, 2026)", "Lodge under seal; remove from served copies."),
        ("M", "Closing Argument (outline) and objections checklist", "Delivery."),
    ]
    toc_i = toc_intro(os.path.join(TMP, "m_toc_intro.pdf"), TABS)

    cover = cover_page(os.path.join(TMP, "m_cover.pdf"), ["ALL-IN-ONE TRIAL BINDER"],
                       ["<i>Swords to Plowshares v. Donald Ernest Gillson, Ed.D.</i>", "Case No. CUD-26-682107 (related: CCH-26-589086, CCH-26-589728)",
                        "Superior Court of California, County of San Francisco", "Department 606 – Hon. Stephen M. Murphy – Trial call November 2, 2026, 9:00 a.m."],
                       "Tabs A–M. Tab L is confidential (CRC 1.100(c)(4)). The Solano County MC-410 / accommodation papers are in a separate binder.")
    sections = [
        ("A", "Table of Contents", [("Table of Contents (tab summary)", toc_i)]),
        ("B", "Statement of the Case", [("Statement of the Case", soc)]),
        ("C", "Fraud Analysis – Line-by-Line Review", [("Fraud Analysis: three-day notice, proof of service, complaint", fraud)]),
        ("D", "Memorandum of Points and Authorities", [("Points and Authorities", pa)]),
        ("E", "Witness List", [("Witness List and expected testimony", wl)]),
        ("F", "Evidence List", [("Evidence List", el)]),
        ("G", "Video and Audio Exhibit List", [("Video List with transmission log", vl)]),
        ("H", "Filings and Service", [("Notice to Francisco Torres, Esq., Oct. 31, 2026", os.path.join(ART, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf")),
                                      ("Subpoena service directory and log", svc)] + sub_items + [("MC-410 Request for Accommodations (SF, Dept. 606) with attachment", mcp)]),
        ("I", "Rule 1.100 Orders and Responses (SF Superior Court)", ada_items),
        ("J", "Evidence Exhibit Binder – Exhibits 1-78", [("Evidence Exhibit Binder (65 pp.)", os.path.join(ART, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
        ("K", "Related Administrative Complaints", [("BBS Complaint 2002026002097 – Kolby Losik", os.path.join(ART, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
                                                    ("BBS Complaint 2002026002098 – Mark Villalobos", os.path.join(ART, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))]),
        ("L", "CONFIDENTIAL Medical Exhibit", [("John Muir Health ED record (Oct. 30, 2026) and wristband photographs – CONFIDENTIAL", med_ex)]),
        ("M", "Closing Argument", [("Closing Argument outline and objections checklist", ca)]),
    ]
    out = os.path.join(ART, "Gillson_All-In-One_Trial_Binder_CUD-26-682107.pdf")
    n = assemble(out, "GTB", cover, sections, "Gillson – All-in-One Trial Binder – CUD-26-682107 – Tab L confidential (CRC 1.100(c)(4))")
    print("pages", n)
    compress_scans(out)
    old = os.path.join(ART, "Gillson_Master_Trial_Binder_CUD-26-682107.pdf")
    if os.path.exists(old):
        os.remove(old)
    print("done")
