from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

OUT = "/vercel/share/artifacts/Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf"

body = ParagraphStyle("body", fontName="Times-Roman", fontSize=11.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=8)
small = ParagraphStyle("small", parent=body, fontSize=10, leading=13)
h = ParagraphStyle("h", fontName="Times-Bold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=4)
title = ParagraphStyle("title", fontName="Times-Bold", fontSize=12.5, leading=16, alignment=TA_CENTER, spaceAfter=10)
num = ParagraphStyle("num", parent=body, leftIndent=22, firstLineIndent=-16, spaceAfter=5)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 8.5)
    canvas.drawString(inch, 0.55 * inch, "Gillson – Notice to F. Torres re CUD-26-682107 – October 31, 2026")
    canvas.drawRightString(letter[0] - inch, 0.55 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=0.9 * inch,
                        title="Notice of Fraudulent Service, Retaliation, Hearsay Defenses, and Medical Documentation Chronology",
                        author="Dr. Donny Gillson, Ed.D.")
S = []
P = lambda t, s=body: S.append(Paragraph(t, s))

P("DR. DONNY GILLSON, ED.D.<br/>1030 Girard Road, Unit 301A, San Francisco, CA 94129<br/>(408) 384-1376 &nbsp;|&nbsp; donny@18fu.ai", small)
S.append(Spacer(1, 10))
P("October 31, 2026", body)
P("<b>VIA EMAIL AND U.S. MAIL</b><br/>Francisco Torres, Esq.<br/>Zanghi Torres Adams LLP<br/>[address] <br/>[email]", body)
S.append(Spacer(1, 6))

hdr = Table([
    ["Re:", "Case No. CUD-26-682107, Superior Court of California, County of San Francisco"],
    ["", "Premises: 1030 Girard Road, Unit 301A, San Francisco, CA 94129"],
    ["", "Three-Day Notice dated ____________, 2026, and Proof of Service dated ____________, 2026"],
], colWidths=[0.45 * inch, 6.0 * inch])
hdr.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 11), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                         ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), 1)]))
S.append(hdr)
S.append(Spacer(1, 12))

P("NOTICE OF FRAUDULENT SERVICE, RETALIATION, HEARSAY DEFENSES,<br/>AND MEDICAL DOCUMENTATION CHRONOLOGY", title)

P("Mr. Torres:")
P("This letter is sent in my capacity as the defendant in the above matter and is intended for the court record. "
  "It addresses the service of the three-day notice on which the unlawful detainer complaint rests, the stated "
  "basis for the eviction, and the records I will rely on. Please direct any response in writing to the email "
  "address above, which the Court has ordered as my accommodated channel of communication.")

P("I.&nbsp;&nbsp;Scope of communication", h)
P("My prior cease-and-desist directive concerned harassing contact. It does not limit, and I do not waive, "
  "my right to correspond with counsel on the procedural and legal matters in this case. Communications "
  "regarding scheduling, service, discovery, and the court's orders should continue, in writing, through the "
  "email address above.")

P("II.&nbsp;&nbsp;The three-day notice: execution and service irregularities", h)
P("The three-day notice and its proof of service identify Jerome Bradford as the person who executed and/or served "
  "the notice and William Landrum as the person who witnessed or declared service, at the date and time stated on "
  "the proof of service. To my knowledge, Mr. Bradford was not present at the premises at that date and time. "
  "If that is correct, the proof of service does not reflect what occurred, and the notice fails the service "
  "requirements of Code of Civil Procedure section 1162 and the sufficiency requirements of section 1161. "
  "A defective notice cannot support an unlawful detainer judgment. (<i>Kwok v. Bergren</i> (1982) 130 Cal.App.3d 596, 599–600; "
  "<i>Liebovich v. Shahrokhkhany</i> (1997) 56 Cal.App.4th 511, 513.)")
P("The service account is also contradicted by your client's own staff. Resident advisor Dwayne, on video, describes the "
  "\u201caccidental\u201d delivery of unverified legal papers and management's disorganized service practices at the building "
  "(designated Trial Exhibit V-05, second suite, served on your office October 29, 2026), and separately describes management "
  "instructions and selective enforcement (Trial Exhibit V-03, second suite). A proof of service that recites personal service "
  "by Mr. Bradford at a stated time cannot be reconciled with a staff member's account of papers being left by accident.")
P("I therefore ask that your office produce, within five court days, the following records so that the service "
  "question can be resolved on documents rather than argument:")
for i, t in enumerate([
    "The original, signed three-day notice and the original proof of service, including any metadata if the documents were generated electronically.",
    "Any building access, key-fob, or visitor-log entries for Mr. Bradford and Mr. Landrum for the date of claimed service.",
    "Any camera footage or stills from the building's common areas for the one-hour window surrounding the claimed time of service, which I ask you to preserve immediately.",
    "Any text message, email, or work order showing when the notice was prepared and who was instructed to serve it.",
], 1):
    P(f"{i}.&nbsp;&nbsp;{t}", num)
P("If the records show that service occurred as declared, I will say so. If they do not, I will ask the Court to "
  "strike the notice and dismiss the complaint, and I reserve all remedies available for a false declaration of service, "
  "including under Code of Civil Procedure section 128.7 and Penal Code section 118. This letter is a preservation demand: "
  "please do not permit any of the items listed above to be deleted or overwritten.")

P("III.&nbsp;&nbsp;The stated basis for eviction is unsupported", h)
P("You have described the reason for the eviction as \u201cthe way that staff was treated.\u201d No contemporaneous written warning, "
  "incident report, or notice to cure was provided to me before the three-day notice issued, and none has been produced "
  "since. A statement attributed to unidentified staff, relayed by management, is hearsay (Evid. Code, § 1200) and will not "
  "be admissible to prove the conduct alleged. If a specific incident is claimed, please identify the date, the staff "
  "member, and the document that recorded it at the time.")
P("Two further points bear on this. First, the three-day notice is drafted in the third person and alleges generalized "
  "\u201cstaff harassment\u201d without naming any staff member, date, or incident. A notice that does not state the facts "
  "constituting the claimed breach with enough particularity for the tenant to respond is insufficient under Code of Civil "
  "Procedure section 1161, subdivision (3). Second, the only disagreement that actually occurred was a personal dispute "
  "between Mr. Landrum and me. Mr. Landrum is the person who prepared or caused the notice to issue. A manager who is himself "
  "the complaining party cannot convert a personal disagreement into an anonymous \u201cstaff\u201d complaint and then rely on "
  "his own account as the independent basis for eviction. I further understand that the account Mr. Landrum gave to the San "
  "Francisco Housing Authority omitted that context; I will request that agency's file.")

P("IV.&nbsp;&nbsp;Retaliation", h)
P("The notice followed closely on protected activity: my written requests for disability accommodation to the landlord "
  "and the Court, my administrative complaint of September 8, 2026, and my complaints regarding conditions and treatment "
  "at the premises. Civil Code section 1942.5 prohibits a landlord from serving a notice to quit or bringing an action to "
  "recover possession in retaliation for a tenant's exercise of rights under the law, and the Fair Employment and Housing "
  "Act (Gov. Code, § 12955, subd. (f)) prohibits retaliation against a person who has requested a reasonable accommodation. "
  "The sequence of events will be presented as an affirmative defense and, if warranted, as the basis for a cross-claim. "
  "I note this now so that the record reflects that you were on notice of the defense before the hearing.")

P("V.&nbsp;&nbsp;Medical documentation chronology", h)
P("I maintain a dated, indexed chronology of VA treatment records covering the entire period at issue. It establishes "
  "where I was, what care I was receiving, and my functional status on each relevant date. It will be used for two limited "
  "purposes: to rebut any behavioral allegation with contemporaneous clinical observation, and to document the timing of my "
  "accommodation requests relative to the notice. The medical content is confidential under California Rules of Court, "
  "rule 1.100(c)(4) and Civil Code section 56 et seq. It will be lodged with the Court under seal or offered in redacted form; "
  "it is not being provided to your office with this letter.")

P("VI.&nbsp;&nbsp;Court participation", h)
P("I am currently under medical orders to rest. On October 30, 2026, I was treated in the John Muir Health Concord "
  "Emergency Department after a fall (CT head and CT cervical spine; diagnosis of acute cervical strain) and was placed off "
  "work through November 3, 2026, with return no earlier than November 4, 2026, the maximum an emergency physician can write. "
  "The discharging physician directed follow-up at Travis Air Force Base (David Grant USAF Medical Center) on or about "
  "November 1, 2026 for further evaluation and extension of that period, which I anticipate will be approximately two weeks. "
  "I will participate in all hearings in this matter by Zoom and will "
  "not appear in person while those orders remain in effect. The Court has already authorized remote appearance for me under "
  "California Rules of Court, rule 1.100, and I am submitting the current medical status to the Court's ADA Coordinator so "
  "that the authorization covers each upcoming date. Please calendar accordingly and do not represent to the Court that I "
  "have declined to appear.")

P("VII.&nbsp;&nbsp;Removal of Mr. Zanghi from the case; the pleadings must be re-executed and the action re-noticed and refiled", h)
P("I understand that John P. Zanghi, who signed the complaint and the papers that followed it and who directed the delivery of "
  "documents to me in Department 505, has been or is being removed from this case. If that is so, the following applies.")
for i, t in enumerate([
    "A change of attorney is effective only when a substitution signed by the client and both attorneys, or a court order, is filed and "
    "notice is given to the adverse party (Code Civ. Proc., §§ 284, 285). Until that is done, Mr. Zanghi remains counsel of record and "
    "must be served with everything in this case. Please file and serve the substitution before any further paper is filed on plaintiff's behalf.",
    "Every pleading in this action must be signed by the attorney of record, and that signature is a certification to the Court that the "
    "factual contentions have evidentiary support (Code Civ. Proc., § 128.7, subds. (a), (b)). An unlawful detainer complaint must also be "
    "verified (Code Civ. Proc., § 1166, subd. (a)(1)). A successor attorney who intends to proceed on a complaint and a proof of service that "
    "he did not sign, and that are challenged as false, cannot simply adopt them. He must satisfy himself that the service account is true and, "
    "if he cannot, he may not advocate it (Bus. & Prof. Code, § 6068, subd. (d); Rules Prof. Conduct, rule 3.3).",
    "The three-day notice is a prerequisite to the action, and its defects cannot be cured by amendment. Where the notice is insufficient or "
    "was not served as section 1162 requires, the complaint must be dismissed and the landlord must serve a new, proper notice and file a new "
    "action (<i>Kwok v. Bergren</i> (1982) 130 Cal.App.3d 596, 599–600; <i>Liebovich v. Shahrokhkhany</i> (1997) 56 Cal.App.4th 511, 513–514; "
    "<i>Bevill v. Zoura</i> (1994) 27 Cal.App.4th 694, 697). An amended complaint filed by you on the existing notice would not fix the problem.",
    "Accordingly, if plaintiff wishes to proceed, the correct course is to dismiss this action, serve a new notice that states the facts of the "
    "claimed breach with particularity and is served and declared truthfully, and file a new verified complaint signed by the attorney who will "
    "actually appear. A new notice served now will itself be measured against the retaliation presumption in Civil Code section 1942.5, given "
    "the dates of my accommodation requests and my September 8, 2026 administrative complaint.",
], 1):
    P(f"{i}.&nbsp;&nbsp;{t}", num)
P("Please confirm in writing whether Mr. Zanghi remains counsel of record, and if not, when the substitution will be filed.")

P("VIII.&nbsp;&nbsp;Requested response", h)
P("Please respond in writing by <b>November 7, 2026</b> confirming (a) that the records in Part II have been preserved and "
  "when they will be produced, (b) whether your client maintains that service occurred as declared, and (c) the status of Mr. Zanghi "
  "as counsel of record. If I receive no "
  "response, I will raise each issue by motion and at the hearing, and I will ask the Court to draw the appropriate "
  "inference from the absence of the records.")
P("Nothing in this letter waives any right, defense, or remedy, all of which are expressly reserved.")
S.append(Spacer(1, 10))
P("Respectfully,")
S.append(Spacer(1, 10))
P("<b>/s/ Dr. Donny Gillson, Ed.D.</b><br/>Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson)<br/>Defendant, In Propria Persona<br/>"
  "ORCID iD: https://orcid.org/0009-0007-0768-5486<br/>"
  "Electronically signed October 31, 2026 through the declarant's ADA cognitive assistive digital-communications application; "
  "conformed /s/ signature per Cal. Rules of Court, rule 2.257(b).")
S.append(Spacer(1, 14))
P("cc:&nbsp;&nbsp;John P. Zanghi, Esq., Zanghi Torres Adams LLP (jzanghi@ztalaw.com)<br/>"
  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Clerk, Dept. 606, San Francisco Superior Court (for the file in CUD-26-682107)", small)

S.append(Spacer(1, 18))
P("<b>PROOF OF SERVICE</b>", h)
P("I am over 18 and a party to this action. On October 31, 2026, I served the foregoing Notice on the persons listed above "
  "by \u2612 email to the addresses shown (the accommodated written channel of record) &nbsp;\u2610 U.S. Mail &nbsp;\u2610 both. "
  "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct. "
  "Executed October 31, 2026, at San Francisco, California.", small)
S.append(Spacer(1, 8))
P("<b>/s/ Dr. Donny Gillson, Ed.D.</b> &nbsp;&nbsp; ORCID iD 0009-0007-0768-5486 &nbsp;&nbsp; Date: October 31, 2026 (e-signed)", small)

doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("ok")
