import os, shutil, glob, io, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

HERE = os.path.dirname(os.path.abspath(__file__))
ART = "/vercel/share/artifacts"
TMP = os.path.join(HERE, "tmp"); os.makedirs(TMP, exist_ok=True)
FORMS = os.path.join(HERE, "forms")

NAME = "Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson)"
ADDR1 = "1030 Girard Road, Unit 301A"
ADDR2 = "San Francisco, CA 94129"
PHONE = "(408) 384-1376"
EMAIL = "donny@18fu.ai"

# ------------------------------------------------------------------ styles
body = ParagraphStyle("b", fontName="Times-Roman", fontSize=11, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
small = ParagraphStyle("s", parent=body, fontSize=9.5, leading=12)
h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=20, leading=25, alignment=TA_CENTER, spaceAfter=14)
h2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=13, leading=17, spaceBefore=10, spaceAfter=5)
cen = ParagraphStyle("c", parent=body, alignment=TA_CENTER)
tab = ParagraphStyle("tab", fontName="Times-Bold", fontSize=42, leading=50, alignment=TA_CENTER)
tabsub = ParagraphStyle("tabsub", fontName="Times-Roman", fontSize=15, leading=20, alignment=TA_CENTER)
num = ParagraphStyle("n", parent=body, leftIndent=24, firstLineIndent=-18, spaceAfter=4)


def rl_pdf(flow, path, title=""):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=inch, rightMargin=1.25 * inch, topMargin=inch, bottomMargin=inch, title=title)
    doc.build(flow)
    return path


def P(t, s=body):
    return Paragraph(t, s)


# ------------------------------------------------------------------ form filling
def fill_form(template, values, out_path, dpi=170):
    """values: {suffix: value}. Fills AcroForm widgets whose field name ends with suffix, then flattens by rasterizing."""
    doc = fitz.open(template)
    used = set()
    for page in doc:
        for w in page.widgets():
            for suf, val in values.items():
                if w.field_name.endswith(suf):
                    if w.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        w.field_value = w.on_state() if val else "Off"
                    else:
                        w.field_value = str(val)
                        w.text_fontsize = 0  # auto-size so text never runs past the field box
                    w.update(); used.add(suf)
    missing = set(values) - used
    if missing:
        print("  unmatched fields:", missing)
    flat = fitz.open()
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        np_ = flat.new_page(width=page.rect.width, height=page.rect.height)
        np_.insert_image(np_.rect, pixmap=pix)
    flat.save(out_path); flat.close(); doc.close()
    return out_path


# ------------------------------------------------------------------ accommodation content
ACCOMS = [
    "Use of N.E.W.T. assistive cognitive software on my own device for typed input only, all audio and recording disabled; 5-10 minutes of setup time before the matter is called; brief input pauses on request.",
    "A 15-minute rest break after about 45 minutes of proceedings; brief symptom-related pauses on request; slower verbal pacing; repetition or clarification when I ask.",
    "All court notices, orders, and ADA communications emailed to donny@18fu.ai (in addition to mail) in searchable electronic format; short numbered written instructions where feasible.",
    "Remote appearance by Zoom or the court's video platform for all hearings; connection details emailed at least two court days ahead; extra time to operate platform controls (hand tremor).",
    "Oral reference to me as \"Dr. Gillson\"; legal name may remain in the caption.",
    "Presence of my task-trained psychiatric service dog, Jaxx, with floor space at counsel table.",
    "Separate seating from opposing parties and their representatives while waiting; separate tables; all in-court communication directed through the Court, clerk, or bailiff.",
    "Access to the courtroom assistive listening system (service-connected bilateral hearing loss).",
    "Permission to read slowly from a written statement or outline.",
    "Confidential handling of this request and all medical material under rule 1.100(c)(4).",
]
VA_DATES = "Confirmed VA appointments to avoid: Oct 22 (3:00 pm tel.), Oct 26 (2:00 pm tel.), Oct 27 (9:00 am Martinez VA; 2:00 pm SF VA), Nov 10, 2026 (2:00 pm SF VA)."
MED = ("Complex PTSD, traumatic brain injury, bipolar I disorder, ADHD, chronic tremor disorder (Parkinsonism vs. essential tremor), "
       "service-connected bilateral hearing loss; 90% VA service-connected. "
       "VA ED visit 9/17/2026 and urgent care 9/29/2026 for worsening tremor; neuropsychological testing scheduled 10/27/2026. "
       "On 10/30/2026 I was treated at John Muir Health Concord Emergency Department after a fall (CT head and CT cervical spine; "
       "acute cervical strain) and placed off work through 11/3/2026, return no earlier than 11/4/2026 (Vertelney, M.D.), the maximum "
       "an emergency physician can write. I was directed to follow up at Travis Air Force Base (David Grant USAF Medical Center) on or "
       "about 11/1/2026, where an extension of approximately two weeks is anticipated. The After Visit Summary and work-status note "
       "are attached as a confidential exhibit. "
       "See below.")


def mc410_attachment(path, court_label, case_no, extra_items, when_text):
    flow = [P(f"<b>MC-410 ATTACHMENT – ITEMS 3, 4, AND 5</b><br/>{court_label}<br/>Case No. {case_no}<br/>Applicant: {NAME}", cen), Spacer(1, 12)]
    flow.append(P("<b>Item 3. When and where the accommodation is needed</b>", h2))
    flow.append(P(when_text, body))
    flow.append(P(VA_DATES, body))
    flow.append(P("<b>Item 4. Accommodations requested</b>", h2))
    for i, a in enumerate(ACCOMS + extra_items, 1):
        flow.append(P(f"{i}.&nbsp;&nbsp;{a}", num))
    flow.append(P("Each item above has been granted or implemented by the San Francisco Superior Court in Case Nos. CUD-26-682107 "
                  "(Depts. 501 and 606), CCH-26-589086, and CCH-26-589728 (Dept. 505) by written rule 1.100 orders dated between "
                  "July 20 and October 14, 2026. Copies are included in the exhibit section of this binder.", body))
    flow.append(P("<b>Item 5. Why the accommodation is needed – impairment (CONFIDENTIAL – rule 1.100(c)(4))</b>", h2))
    flow.append(P(MED, body))
    flow.append(P("Functional effect: under stress, concentration, recall, and sequencing degrade; spoken instructions are processed less "
                  "reliably than written ones; sustained participation beyond about 45 minutes produces fatigue and tremor; hand tremor slows "
                  "typing and operation of screen controls; hearing loss makes overlapping speech hard to follow; confrontational proximity and "
                  "interruption are PTSD triggers. Bed-rest orders currently preclude in-person attendance.", body))
    flow.append(Spacer(1, 10))
    flow.append(P("I understand the court may need to contact me for more information. I prefer written contact by email.", small))
    return rl_pdf(flow, path, "MC-410 Attachment")


def make_mc410(tag, county, court_street, court_city, case_no, court_label, extra_items, when_text, filed_as, case_type, when_short):
    form_vals = {
        "List1[0].LI1[0].NameInfo[0]": NAME,
        "List1[0].LI1[0].Address[0]": ADDR1,
        "List1[0].LI1[0].Address1[0]": court_city if False else ADDR2,
        "List1[0].LI1[0].Phone[0]": PHONE,
        "List1[0].LI1[0].Email[0]": EMAIL,
        "CaptionP1Right_sf[0].TextField6[0]": f"Superior Court of California, County of {county}, {court_street}, {court_city}",
        "CaptionP1Right_sf[0].CaseNumber_ft[0]": case_no,
        "List2[0].LI1[0].CheckParty[0]": True,
        "List2[0].LI1[0].Name[0]": filed_as,
        "CaptionP1Right_sf[0].CaseNumber_ft1[0]": case_type,
        "List3[0].LI1[0].TextField4[0]": when_short,
        "List4[0].LI1[0].Medical-Condition[0]": "See Attachment, Item 4 (" + str(len(ACCOMS) + len(extra_items)) + " items): Zoom, assistive software, breaks, email notice, service dog.",
        "List5[0].LI1[0].TextField4[0]": "See Attachment, Item 5 (confidential): PTSD, TBI, tremor, hearing loss; 90% VA; bed rest.",
        "List5[0].LI1[0].CheckBox3[0]": True,
        "SignSub[0].NameInfo[0]": NAME,
        "SignSub[0].Email[0]": EMAIL,
        "SignSub[0].Phone[0]": PHONE,
        "SignSub[0].DateTimeField1[0]": "October 31, 2026",
        "SignSub[0].Name[0]": "/s/ Dr. Donny Gillson, Ed.D.  (e-signed; ORCID 0009-0007-0768-5486)",
        "Page2[0].SignSub[0].YourName_ft[0]": "/s/ Dr. Donny Gillson, Ed.D.  (e-signed; ORCID 0009-0007-0768-5486)",
        "Page2[0].HeaderSub[0].NameInfo[0]": NAME,
        "Page2[0].HeaderSub[0].CaseNumber_ft[0]": case_no,
    }
    f1 = fill_form(os.path.join(FORMS, "mc410.pdf"), form_vals, os.path.join(TMP, f"mc410_{tag}.pdf"))
    att = mc410_attachment(os.path.join(TMP, f"mc410_{tag}_att.pdf"), court_label, case_no, extra_items, when_text)
    return [f1, att]


# ------------------------------------------------------------------ subpoenas (SUBP-002) for CUD-26-682107, Dept. 606
SF_COURT = dict(county="San Francisco", street="400 McAllister Street", city="San Francisco, CA 94102", branch="Civic Center Courthouse")
TRIAL = dict(date="November 2, 2026", time="9:00 a.m.", dept="606")

CAT_NOTICE = [
    "The original signed three-day notice served on or about ____________, 2026 regarding Unit 301A, and every draft, version, and copy of it, with native electronic files and metadata (creation date, author, last-modified date).",
    "The original proof of service for that notice and every draft or version of it; any declaration, log, text message, or email describing when, where, how, and by whom the notice was served, including any communication involving William Landrum or Jerome Bradford on the date of claimed service.",
    "Building access-control, key-fob, visitor-log, timekeeping, payroll, or scheduling records showing the presence or absence of William Landrum and Jerome Bradford at 1030 Girard Road on the date of claimed service.",
    "Video recordings or still images from common-area cameras at 1030 Girard Road for the two-hour window surrounding the time of claimed service, and any retention or deletion log for that footage.",
    "Every written warning, incident report, grievance response, notice to cure, or staff complaint concerning Dr. Gillson created before the three-day notice issued, and the identity of each staff member who authored or is named in it.",
    "All communications between Swords to Plowshares staff and the San Francisco Housing Authority, HUD-VASH, or SSVF program staff concerning Dr. Gillson's tenancy, including any account of the dispute between William Landrum and Dr. Gillson.",
]
CAT_HABIT = [
    "All maintenance requests, work orders, plumbing and sewage backflow remediation records, pest-control service logs, and contractor invoices for 1030 Girard Road and Unit 301A from November 1, 2025 to the present.",
    "All advance notices of water shutoffs or utility interruptions issued to residents of 1030 Girard Road in the same period.",
    "All correspondence with the San Francisco Department of Public Health, the Presidio Trust, or the United States Park Police concerning conditions at 1030 Girard Road in the same period.",
]
CAT_LEDGER = [
    "The complete tenant ledger for Unit 301A from January 1, 2026 to the present, showing rent charges, payments, credits, HUD-VASH or SSVF subsidy receipts, and any late fees or adjustments.",
]
CAT_ADA = [
    "All communications between Zanghi Torres Adams LLP and Swords to Plowshares staff concerning Dr. Gillson's requests for disability accommodation (in the tenancy or in court), his service dog, his use of assistive technology, or his remote appearances, from June 1, 2026 to the present.",
    "All communications between Zanghi Torres Adams LLP or Swords to Plowshares and the Superior Court's ADA Coordinator concerning Dr. Gillson.",
    "All documents reflecting the preparation, delivery, and contents of the box of documents deposited on Dr. Gillson in Department 505, including any index, cover letter, proof of service, and internal instruction regarding that delivery.",
    "All communications with William Landrum, Jerome Bradford, or any Swords to Plowshares employee concerning the preparation, timing, or service of the three-day notice.",
]

WITNESSES = [
    dict(tag="landrum", short="William Landrum, 1030 Girard Rd., SF 94129", name="William Landrum", role="Assistant Property Manager, Swords to Plowshares (Girard Road Supportive Housing)",
         addr="1030 Girard Road, Presidio of San Francisco, CA 94129", items=CAT_NOTICE + CAT_HABIT,
         why="Mr. Landrum is the declarant or witness on the proof of service of the three-day notice, is the person with whom the underlying dispute occurred, and prepared or caused the notice to issue. His testimony and records are necessary to establish how and when the notice was served, what staff complaints (if any) existed before it issued, and the condition of the premises."),
    dict(tag="bradford", short="Jerome Bradford, 1030 Girard Rd., SF 94129", name="Jerome Bradford", role="Property / Operations Staff, Swords to Plowshares",
         addr="1030 Girard Road, Presidio of San Francisco, CA 94129", items=CAT_NOTICE[:4] + CAT_HABIT[:1],
         why="Mr. Bradford is identified as the person who executed and/or served the three-day notice. His testimony is necessary to establish whether he was present at the premises at the date and time stated on the proof of service, and his records are necessary to corroborate or refute that account."),
    dict(tag="torres", short="Francisco G. Torres, Esq., 625 Market St., 4th Fl., SF 94105", name="Francisco G. Torres, Esq.", role="Partner, Zanghi Torres Adams LLP; counsel for plaintiff",
         addr="625 Market Street, 4th Floor, San Francisco, CA 94105-3306", items=CAT_ADA + [CAT_NOTICE[0], CAT_NOTICE[1]],
         why="Mr. Torres is counsel of record and has personal knowledge of the preparation and service of the three-day notice and of the handling of defendant's accommodation requests. The records sought are business records and communications, not attorney work product concerning litigation strategy; to the extent privilege is claimed, a log is requested."),
    dict(tag="zanghi", short="John P. Zanghi, Esq., 625 Market St., 4th Fl., SF 94105", name="John P. Zanghi, Esq.", role="Partner, Zanghi Torres Adams LLP; lead counsel for plaintiff",
         addr="625 Market Street, 4th Floor, San Francisco, CA 94105-3306", items=CAT_ADA,
         why="Mr. Zanghi is lead counsel of record, was served with the Court's rule 1.100 orders, and directed the delivery of documents to defendant in Department 505. His records are necessary on the accommodation and retaliation defenses."),
    dict(tag="stp", short="Custodian of Records, Swords to Plowshares, 401 Van Ness Ave. #313, SF 94102", name="Custodian of Records, Swords to Plowshares (attn: Michael Blecker, Executive Director)", role="Plaintiff / housing provider",
         addr="401 Van Ness Avenue, Suite 313, San Francisco, CA 94102", items=CAT_NOTICE + CAT_HABIT + CAT_LEDGER,
         why="Swords to Plowshares is the plaintiff and the custodian of the tenancy file, ledger, maintenance records, and staff communications on which the notice and the defenses depend. Plaintiff served no responses to defendant's written discovery; these records are therefore sought by trial subpoena."),
    dict(tag="dph", short="Custodian of Records, SF Dept. of Public Health, 49 S. Van Ness Ave. #600, SF 94103", name="Custodian of Records, San Francisco Department of Public Health, Environmental Health Branch (Healthy Housing)", role="Non-party public agency",
         addr="49 South Van Ness Avenue, Suite 600, San Francisco, CA 94103", items=[
             "The complete file for 311 / Environmental Health complaint Case No. 101003004371 concerning 1030 Girard Road, including inspection reports, photographs, notices of violation, correspondence with the property owner or manager, and closure records.",
             "Any other inspection or complaint records for 1030 Girard Road from November 1, 2025 to the present."],
         why="The Department's inspection records are independent public records of the condition of the premises during the tenancy and are relevant to the habitability and retaliation defenses."),
    dict(tag="ada", short="Custodian of Records, SF Superior Court ADA Coordinator, 400 McAllister St. Rm 205", name="Custodian of Records, Superior Court of California, County of San Francisco, ADA Coordinator (Joy Guandique)", role="Court administrative office",
         addr="400 McAllister Street, Room 205, San Francisco, CA 94102", items=[
             "The non-confidential portions of the rule 1.100 accommodation file for Dr. Donny Gillson in Case Nos. CUD-26-682107, CCH-26-589086, and CCH-26-589728: each request received, each written response or order issued, the dates of each, and any communication from plaintiff's counsel concerning those requests.",
             "Any record of transmittal of the Court's accommodation orders to plaintiff's counsel."],
         why="The accommodation file establishes the dates of defendant's protected activity relative to the three-day notice and the notice given to plaintiff's counsel of the Court's orders. Defendant waives confidentiality only as to the dates and dispositions, not the medical content."),
]


def subp_attachment(path, w):
    flow = [P("<b>ATTACHMENT 3 TO CIVIL SUBPOENA (DUCES TECUM) – SUBP-002</b><br/>Swords to Plowshares v. Gillson, Case No. CUD-26-682107<br/>"
              "Superior Court of California, County of San Francisco, Dept. 606", cen), Spacer(1, 8)]
    flow.append(P(f"<b>Witness:</b> {w['name']}<br/><b>Capacity:</b> {w['role']}<br/><b>Service address:</b> {w['addr']}", body))
    flow.append(P("<b>Documents, electronically stored information, and other things to be produced</b>", h2))
    for i, it in enumerate(w["items"], 1):
        flow.append(P(f"{i}.&nbsp;&nbsp;{it}", num))
    flow.append(P("<b>Instructions.</b> Produce records in the form in which they are ordinarily kept. Electronic records (email, text messages, "
                  "video, access logs) shall be produced in native format with metadata, or as searchable PDF with a load file. If any item is "
                  "withheld on a claim of privilege, identify it by date, author, recipient, and subject in a log served with the production. "
                  "\u201cDr. Gillson\u201d and \u201cdefendant\u201d mean Donald Ernest Gillson, also known as Dr. Donny Gillson, Ed.D., tenant of Unit 301A. "
                  "\u201cThree-day notice\u201d means the notice to quit or perform on which the complaint in this action is based.", body))
    flow.append(P("<b>Good cause / materiality (Code Civ. Proc., § 1985, subd. (b); Evid. Code, § 1560)</b>", h2))
    flow.append(P(w["why"], body))
    flow.append(P("The records are not in defendant's possession. Plaintiff served no responses to defendant's special interrogatories or demands for "
                  "production, so these records cannot be obtained through party discovery before trial. The records go directly to the sufficiency "
                  "and service of the notice (Code Civ. Proc., §§ 1161, 1162), the habitability defense (Civ. Code, § 1941.1), and the retaliation defense "
                  "(Civ. Code, § 1942.5).", body))
    flow.append(Spacer(1, 10))
    flow.append(P("Dated: October 31, 2026", body))
    flow.append(P("<b>/s/ Dr. Donny Gillson, Ed.D.</b><br/>Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson), Defendant in pro per<br/>"
                  "ORCID iD: https://orcid.org/0009-0007-0768-5486<br/>"
                  "Electronically signed October 31, 2026 through the declarant's ADA cognitive assistive digital-communications application; "
                  "conformed /s/ signature per Cal. Rules of Court, rule 2.257(b).", body))
    return rl_pdf(flow, path, "Attachment 3")


def make_subpoena(w):
    vals = {
        "AttyPartyInfo[0].TextField1[0]": f"{NAME}\n{ADDR1}, {ADDR2}",
        "AttyPartyInfo[0].Name[0]": "Defendant, in pro per",
        "AttyPartyInfo[0].Phone[0]": PHONE,
        "AttyPartyInfo[0].Email[0]": EMAIL,
        "CourtInfo[0].CrtCounty[0]": SF_COURT["county"],
        "CourtInfo[0].CrtStreet[0]": SF_COURT["street"],
        "CourtInfo[0].CrtMailingAdd[0]": SF_COURT["street"],
        "CourtInfo[0].CrtCityZip[0]": SF_COURT["city"],
        "CourtInfo[0].CrtBranch[0]": SF_COURT["branch"],
        "TitlePartyName[0].Party1[0]": "Swords to Plowshares",
        "TitlePartyName[0].Party2[0]": "Donald Ernest Gillson, Ed.D. (Dr. Donny Gillson)",
        "CaseNumber[0].CaseNumber[0]": "CUD-26-682107",
        "People[0].FillText1[0]": w["short"] + " – see Attachment 3 for address",
        "List3[0].Lia[0].subp1[0]": True,
        "Lia[0].HearingDate_dt[0]": TRIAL["date"],
        "Lia[0].HearingTime_dt[0]": TRIAL["time"],
        "Lia[0].Checkbox1[0]": True,
        "Lia[0].HearingDept_ft1[0]": TRIAL["dept"],
        "Lib[0].HearingAddress[0]": f"{SF_COURT['street']}, {SF_COURT['city']}",
        "List4[0].Lia[0].FillText18[0]": NAME,
        "List4[0].Lib[0].FillText19[0]": PHONE,
        "Sign[0].SigDate[0]": "October 31, 2026",
        "Sign[0].SigName[0]": "/s/ Dr. Donny Gillson, Ed.D.  (e-signed; ORCID 0009-0007-0768-5486)",
        "Production[0].RB2Choices1[0]": True,
        "Li1[0].limited1[0]": True,
        "Li1[0].TextField89[0]": "",
        "Li1[0].limited1[5]": True,
        "Li1[0].TextField90[0]": "See Attachment 3",
        "Li2[0].Ch1[0]": True,
        "Li2[0].FillText17[0]": "See Attachment 3, Documents to be produced.",
        "Li3[0].Ch2[0]": True,
        "Li3[0].FillText18[0]": "See Attachment 3, Good cause / materiality.",
        "Page3[0].List1[0].Lia[0].FillText1[0]": "",
    }
    f = fill_form(os.path.join(FORMS, "subp002.pdf"), vals, os.path.join(TMP, f"subp_{w['tag']}.pdf"))
    att = subp_attachment(os.path.join(TMP, f"subp_{w['tag']}_att.pdf"), w)
    return [f, att]


# ------------------------------------------------------------------ pages: cover, toc, tabs
def tab_page(path, letter_, title, sub=""):
    flow = [Spacer(1, 2.6 * inch), P(f"TAB {letter_}", tab), Spacer(1, 12), P(title, ParagraphStyle("tt", parent=tabsub, fontName="Times-Bold", fontSize=18, leading=24))]
    if sub:
        flow += [Spacer(1, 8), P(sub, tabsub)]
    return rl_pdf(flow, path)


def cover_page(path, title_lines, case_lines, note):
    flow = [Spacer(1, 1.4 * inch)]
    for t in title_lines:
        flow.append(P(t, h1))
    flow.append(Spacer(1, 18))
    for t in case_lines:
        flow.append(P(t, ParagraphStyle("cl", parent=cen, fontSize=12.5, leading=17)))
    flow.append(Spacer(1, 30))
    flow.append(P(f"Submitted by {NAME}<br/>{ADDR1}, {ADDR2}<br/>{PHONE} | {EMAIL}", cen))
    flow.append(Spacer(1, 30))
    flow.append(P(note, ParagraphStyle("nt", parent=small, alignment=TA_CENTER)))
    flow.append(Spacer(1, 10))
    flow.append(P("Prepared October 31, 2026", cen))
    return rl_pdf(flow, path)


def toc_page(path, rows):
    flow = [P("TABLE OF CONTENTS", h1), Spacer(1, 6)]
    cell = ParagraphStyle("cell", fontName="Times-Roman", fontSize=9.5, leading=11.5)
    data = [["Tab", "Document", "Bates range"]] + [[r[0], Paragraph(r[1].strip(), cell), Paragraph(r[2], cell)] for r in rows]
    t = Table(data, colWidths=[0.5 * inch, 4.5 * inch, 1.5 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Times-Bold", 10.5), ("FONT", (0, 1), (-1, -1), "Times-Roman", 10),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black), ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    flow.append(t)
    return rl_pdf(flow, path)


ADA_EXHIBITS = [
    ("20260720_CUD_response_to_requests.pdf", "SF Sup. Ct., Dept. 501 – Response to ADA Requests (CUD-26-682107), July 20, 2026"),
    ("20260722_CUD_response_to_requests.pdf", "SF Sup. Ct. – Response to ADA Requests (CUD-26-682107), July 22, 2026"),
    ("20260806_CUD_order_re_ADA_requests.pdf", "SF Sup. Ct. – Order re ADA Requests (CUD-26-682107), Aug. 6, 2026"),
    ("20260814a_CUD_response_to_requests.pdf", "SF Sup. Ct., Dept. 501 (Feng, J.) – Response to ADA Requests, Aug. 14, 2026"),
    ("20260814b_CUD_response_to_requests.pdf", "SF Sup. Ct. – Response to ADA Requests (second), Aug. 14, 2026"),
    ("20260827_CUD_response_to_requests.pdf", "SF Sup. Ct. – Response to ADA Requests, Aug. 27, 2026"),
    ("20260831_CUD_two_responses.pdf", "SF Sup. Ct. – Two Responses to ADA Requests, Aug. 31, 2026"),
    ("20260908a_CUD_response_to_0902_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 2, issued Sept. 8, 2026"),
    ("20260908b_CUD_response_to_0908_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 8, issued Sept. 8, 2026"),
    ("20260908c_response_to_attachment_B_admin_complaint.pdf", "SF Sup. Ct. – Response to Attachment B, Formal Administrative Complaint received Sept. 8, 2026"),
    ("20260910_CUD_response_to_0910_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 10, 2026"),
    ("20260918a_CUD_CCH589086_response_to_0917_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 17 (CUD & CCH-26-589086), Sept. 18, 2026"),
    ("20260918b_CUD_CCH589086_response_to_0917_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 17 (second), Sept. 18, 2026"),
    ("20260922_CUD_response_to_0917_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 17, issued Sept. 22, 2026"),
    ("20260924a_CUD_response_to_0918_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 18, issued Sept. 24, 2026"),
    ("20260924b_CUD_response_to_0918_request.pdf", "SF Sup. Ct. – Response to ADA Request of Sept. 18 (second), Sept. 24, 2026"),
    ("20261008a_CCH589728_response_to_1002_request.pdf", "SF Sup. Ct., Dept. 505 (Maffei, J.) – Response to ADA Request of Oct. 2 (CCH-26-589728), Oct. 8, 2026"),
    ("20261008b_CCH589728_response_to_1006_request.pdf", "SF Sup. Ct., Dept. 505 – Response to ADA Request of Oct. 6 (CCH-26-589728), Oct. 8, 2026"),
    ("20261014a_CUD_response_to_1009_request.pdf", "SF Sup. Ct. – Response to ADA Request of Oct. 9 (CUD-26-682107), Oct. 14, 2026"),
    ("20261014b_CUD_response_to_1009_request.pdf", "SF Sup. Ct. – Response to ADA Request of Oct. 9 (second), Oct. 14, 2026"),
]


MED_PHOTOS = [
    ("20261030_170531.jpg", "Oct. 30, 2026, 5:05 p.m.", "Declarant on a gurney in the John Muir Health Concord Emergency Department corridor, awaiting evaluation after the fall."),
    ("20261030_211221.jpg", "Oct. 30, 2026, 9:12 p.m.", "John Muir Health patient wristband: GILLSON, DONALD E; MRN 26013962; CSN 2157776516; DOB 08/21/69."),
    ("20261030_211227.jpg", "Oct. 30, 2026, 9:12 p.m.", "VA Martinez Outpatient Clinic wristband (Admit/Print 30-Oct-26, DOB 8/21/69) worn with red ALLERGY band."),
    ("20261030_211232.jpg", "Oct. 30, 2026, 9:12 p.m.", "VA Martinez OPC wristband, close view: DONALD ERNEST; Allergies: No; Martinez OPC; red ALLERGY band."),
    ("20261031_122427.jpg", "Oct. 31, 2026, 12:24 p.m.", "Both wristbands still worn the following day: VA Martinez OPC band (Print 30-Oct-26) beside the Oct. 18, 2026 VA band."),
    ("20261031_122435.jpg", "Oct. 31, 2026, 12:24 p.m.", "Reverse of the bands showing VA print stamps dated 10/18/2026 11:08-11:09 and the Martinez OPC band."),
    ("20261031_122448.jpg", "Oct. 31, 2026, 12:24 p.m.", "John Muir Health wristband still worn Oct. 31, 2026 (MRN 26013962; CSN 2157776516)."),
]


def medical_exhibit(path):
    """Confidential exhibit: ED After Visit Summary + work-status note, then captioned wristband photographs."""
    med = os.path.join(HERE, "medical")
    cover = rl_pdf([
        Spacer(1, 1.2 * inch),
        P("CONFIDENTIAL MEDICAL EXHIBIT", h1),
        P("Cal. Rules of Court, rule 1.100(c)(4); Civ. Code, § 56 et seq.", cen), Spacer(1, 18),
        P("<b>Part 1.</b> John Muir Health, Concord Emergency Department – After Visit Summary and work-status note, "
          "October 30, 2026 (Haley Vertelney, M.D.), reproduced as highlighted excerpts of the operative lines; the full record is held and will be produced on request. Diagnosis: acute strain of neck muscle after a fall; CT head and CT cervical "
          "spine performed. Off work through November 3, 2026; may return November 4, 2026. Follow up at Travis Air Force Base "
          "(David Grant USAF Medical Center, 707-424-1110) in 2 days, around November 1, 2026.", body),
        P("<b>Part 2.</b> Seven photographs taken October 30-31, 2026 on the declarant's phone (original file names and "
          "capture timestamps shown) documenting the emergency department visit and the hospital identification bands.", body),
        Spacer(1, 12),
        P("Index", h2),
        Table([["No.", "File", "Captured", "Description"]] + [[str(i + 1), Paragraph(f, small), Paragraph(t, small), Paragraph(d, small)] for i, (f, t, d) in enumerate(MED_PHOTOS)],
              colWidths=[0.4 * inch, 1.5 * inch, 1.4 * inch, 2.95 * inch],
              style=TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5), ("FONT", (0, 1), (-1, -1), "Times-Roman", 9),
                                ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")])),
    ], os.path.join(TMP, "med_cover.pdf"))
    out = fitz.open()
    out.insert_pdf(fitz.open(cover))
    # ED record: only the operative lines (diagnosis, work status, follow-up), highlighted; full record held and produced on request
    import snip
    ed_snip = snip.snippet_pdf(os.path.join(med, "JohnMuir_ED_AVS_2026-10-30.pdf"), os.path.join(TMP, "med_ed_snip.pdf"),
                               "CONFIDENTIAL - John Muir Health ED After Visit Summary, Oct. 30, 2026 - operative language only", "ED record", kw_re=snip.MED_RE)
    out.insert_pdf(fitz.open(ed_snip))
    # Photographs: four to a page
    from PIL import Image, ImageOps
    slots = [fitz.Rect(54, 80, 300, 400), fitz.Rect(312, 80, 558, 400), fitz.Rect(54, 420, 300, 740), fitz.Rect(312, 420, 558, 740)]
    for i, (fn, ts, desc) in enumerate(MED_PHOTOS):
        if i % 4 == 0:
            pg = out.new_page(width=612, height=792)
            pg.insert_textbox(fitz.Rect(54, 44, 558, 70), f"Photographs {i + 1}-{min(i + 4, len(MED_PHOTOS))} of {len(MED_PHOTOS)} - emergency department visit, Oct. 30-31, 2026",
                              fontsize=10, fontname="hebo")
        r = slots[i % 4]
        im = ImageOps.exif_transpose(Image.open(os.path.join(med, fn))).convert("RGB")
        im.thumbnail((1000, 1000))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True)
        pg.insert_image(fitz.Rect(r.x0, r.y0, r.x1, r.y1 - 58), stream=buf.getvalue(), keep_proportion=True)
        pg.insert_textbox(fitz.Rect(r.x0, r.y1 - 56, r.x1, r.y1), f"{i + 1}. {fn} - {ts}. {desc}", fontsize=7.5, fontname="tiro")
    out.save(path, garbage=3, deflate=True)
    out.close()
    return path


def compress_scans(path):
    """Downsample embedded scans so the merged binder stays well under 100 MB while remaining legible."""
    d = fitz.open(path)
    d.rewrite_images(dpi_threshold=160, dpi_target=130, quality=70, lossy=True, lossless=True)
    tmp = path + ".tmp"
    d.save(tmp, garbage=4, deflate=True)
    d.close()
    os.replace(tmp, path)
    print("compressed", os.path.basename(path), round(os.path.getsize(path) / 1048576, 1), "MB")


def assemble(out_path, prefix, cover, sections, confidential_note):
    """sections: list of (tab_letter, title, [pdf paths], [(label, path) for toc sub-rows])"""
    # first pass: build to count pages for TOC
    def build(toc_path):
        doc = fitz.open()
        toc = []
        bates = 1
        rows = []
        def add(path, bookmark=None, level=1):
            nonlocal bates
            src = fitz.open(path)
            start = len(doc)
            doc.insert_pdf(src)
            if bookmark:
                toc.append([level, bookmark, start + 1])
            first = bates
            bates += len(src)
            src.close()
            return first, bates - 1
        add(cover, "Cover")
        if toc_path:
            add(toc_path, "Table of Contents")
        for letter_, title, items in sections:
            tp = tab_page(os.path.join(TMP, f"tab_{prefix}_{letter_}.pdf"), letter_, title)
            s, _ = add(tp, f"Tab {letter_} – {title}")
            rows.append([f"{letter_}", title, ""])
            for label, path in items:
                a, b = add(path, label, 2)
                rows.append(["", f"    {label}", f"{prefix}-{a:04d} – {prefix}-{b:04d}"])
        # Bates stamp
        for i, page in enumerate(doc):
            r = page.rect
            page.insert_text((r.width - 2.1 * inch, r.height - 0.3 * inch), f"{prefix}-{i+1:04d}", fontsize=8, fontname="helv", color=(0, 0, 0))
            page.insert_text((0.5 * inch, r.height - 0.3 * inch), confidential_note, fontsize=7, fontname="helv", color=(0.25, 0.25, 0.25))
        doc.set_toc(toc)
        return doc, rows
    d0, rows = build(None)
    d0.close()
    tocp = toc_page(os.path.join(TMP, f"toc_{prefix}.pdf"), rows)
    # second pass with TOC; TOC page count may shift numbering by its own length, so rebuild rows and regenerate once more
    d1, rows = build(tocp)
    n_toc = len(fitz.open(tocp))
    d1.close()
    tocp = toc_page(os.path.join(TMP, f"toc_{prefix}.pdf"), rows)
    if len(fitz.open(tocp)) != n_toc:
        d1, rows = build(tocp); d1.close(); tocp = toc_page(os.path.join(TMP, f"toc_{prefix}.pdf"), rows)
    d2, _ = build(tocp)
    d2.save(out_path, garbage=3, deflate=True)
    n = len(d2); d2.close()
    return n


if __name__ == "__main__":
    ada_items = [(f"Ex. {i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]
    print("medical exhibit")
    med_ex = medical_exhibit(os.path.join(TMP, "medical_exhibit.pdf"))
    med_item = ("CONFIDENTIAL Exhibit – John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)
    # standalone copy for lodging with the ADA Coordinator
    shutil.copy(med_ex, os.path.join(ART, "Gillson_Confidential_Medical_Exhibit_ED_2026-10-30.pdf"))

    # ---------------- Binder 1: San Francisco master binder (CUD-26-682107)
    print("MC-410 (SF)")
    mc_sf = make_mc410("sf", "San Francisco", "400 McAllister Street", "San Francisco, CA 94102", "CUD-26-682107",
                       "Superior Court of California, County of San Francisco – Dept. 606 (Hon. Stephen M. Murphy)",
                       ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask that the November 2, 2026 trial call and all further proceedings be conducted with me appearing by Zoom, or be continued to a date after those orders are lifted and after the October 27 neuropsychological evaluation results are available. The emergency department record is attached as a confidential exhibit."],
                       "Trial call November 2, 2026, 9:00 a.m., Dept. 606, and all further hearings in this case.", "Defendant", "Unlawful detainer", "Trial call Nov. 2, 2026, 9:00 a.m., Dept. 606, and all further hearings.")
    subs = []
    for w in WITNESSES:
        print("subpoena", w["tag"])
        subs.append((f"Civil Subpoena (Duces Tecum) – {w['name']}", make_subpoena(w)))
    # merge each subpoena form + attachment into one file
    sub_items = []
    for label, parts in subs:
        m = fitz.open()
        for p in parts:
            m.insert_pdf(fitz.open(p))
        mp = os.path.join(TMP, f"merged_{label[:30].replace(' ', '_').replace('/', '')}.pdf")
        m.save(mp); m.close()
        sub_items.append((label, mp))
    # service directory page
    cell = ParagraphStyle("dcell", fontName="Times-Roman", fontSize=9, leading=11)
    dir_rows = [["Witness", "Capacity", "Service address"]] + [[Paragraph(w["name"], cell), Paragraph(w["role"], cell), Paragraph(w["addr"], cell)] for w in WITNESSES]
    t = Table(dir_rows, colWidths=[2.0 * inch, 2.1 * inch, 2.15 * inch], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5), ("FONT", (0, 1), (-1, -1), "Times-Roman", 9),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    svc = rl_pdf([P("SUBPOENA SERVICE DIRECTORY AND SERVICE LOG", h1),
                  P("Case No. CUD-26-682107, Dept. 606, trial call November 2, 2026, 9:00 a.m. Subpoenas must be issued by the clerk (or signed by an attorney) "
                    "before service and personally served with witness fees tendered on demand (Code Civ. Proc., §§ 1985, 1987; Gov. Code, § 68093). "
                    "Serve each subpoena with its Attachment 3. Complete the proof of service on page 3 of each SUBP-002 and file it with Dept. 606.", small),
                  Spacer(1, 8), t, Spacer(1, 12),
                  P("Service log", h2),
                  Table([["Witness", "Date/time served", "Served by", "Fees tendered", "Proof filed"]] + [[w["name"].split(",")[0], "", "", "", ""] for w in WITNESSES],
                        colWidths=[2.05 * inch, 1.15 * inch, 1.15 * inch, 0.95 * inch, 0.95 * inch],
                        style=TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5), ("FONT", (0, 1), (-1, -1), "Times-Roman", 9),
                                          ("GRID", (0, 0), (-1, -1), 0.25, colors.grey), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white]),
                                          ("TOPPADDING", (0, 1), (-1, -1), 9), ("BOTTOMPADDING", (0, 1), (-1, -1), 9)]))],
                 os.path.join(TMP, "service_dir.pdf"))

    cover1 = cover_page(os.path.join(TMP, "cover_sf.pdf"),
                        ["MASTER TRIAL BINDER"],
                        ["<i>Swords to Plowshares v. Donald Ernest Gillson, Ed.D.</i>", "Case No. CUD-26-682107 (related: CCH-26-589086, CCH-26-589728)",
                         "Superior Court of California, County of San Francisco", "Department 606 – Hon. Stephen M. Murphy – Trial call November 2, 2026, 9:00 a.m."],
                        "Tabs A–B are for filing and service. Tab C (MC-410) goes to the ADA Coordinator; its Attachment Item 5 is confidential under rule 1.100(c)(4). "
                        "Tabs D–F are exhibits for the Court's and the parties' reference.")
    sections1 = [
        ("A", "Notice to Counsel re Service, Retaliation, Hearsay, and Medical Chronology",
         [("Notice to Francisco Torres, Esq., Oct. 31, 2026", os.path.join(ART, "Gillson_Notice_to_Torres_Fraudulent_Service_Retaliation.pdf"))]),
        ("B", "Civil Subpoenas (Duces Tecum) – SUBP-002 with Attachment 3",
         [("Service directory and service log", svc)] + sub_items),
        ("C", "Request for Accommodations – MC-410 (San Francisco, Dept. 606)",
         [("MC-410 with Attachment (Items 3-5)", (lambda: (lambda m: (m.insert_pdf(fitz.open(mc_sf[0])), m.insert_pdf(fitz.open(mc_sf[1])), m.save(os.path.join(TMP, "mc_sf_merged.pdf")), os.path.join(TMP, "mc_sf_merged.pdf"))[-1])(fitz.open()))()), med_item]),
        ("D", "San Francisco Superior Court Rule 1.100 Orders and Responses (July–October 2026)", ada_items),
        ("E", "Evidence Exhibit Binder – Conditions at 1030 Girard Road (photographs and notices)",
         [("Gillson Evidence Exhibit Binder (previously compiled)", os.path.join(ART, "Gillson_Evidence_Exhibit_Binder.pdf"))]),
        ("F", "Related Administrative Complaints",
         [("BBS Complaint 2002026002097 – Kolby Losik", os.path.join(ART, "BBS_Complaint_2002026002097_Kolby_Losik.pdf")),
          ("BBS Complaint 2002026002098 – Mark Villalobos", os.path.join(ART, "BBS_Complaint_2002026002098_Mark_Villalobos.pdf"))]),
    ]
    n1 = assemble(os.path.join(ART, "Gillson_Master_Trial_Binder_CUD-26-682107.pdf"), "GTB", cover1, sections1,
                  "Gillson – Master Trial Binder – CUD-26-682107 – Tab C Attachment Item 5 and Tab D medical content confidential (CRC 1.100(c)(4))")
    print("binder 1 pages", n1)
    compress_scans(os.path.join(ART, "Gillson_Master_Trial_Binder_CUD-26-682107.pdf"))

    # ---------------- Binder 2: Solano County (separate, per instruction)
    print("MC-410 (Solano)")
    mc_sol = make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)",
                        "Superior Court of California, County of Solano – Civil Harassment (Code Civ. Proc., § 527.6)",
                        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask to appear by Zoom at every hearing in this matter until those orders are lifted. The emergency department record is attached as a confidential exhibit."],
                        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings.")
    m = fitz.open(); m.insert_pdf(fitz.open(mc_sol[0])); m.insert_pdf(fitz.open(mc_sol[1])); mcsp = os.path.join(TMP, "mc_sol_merged.pdf"); m.save(mcsp); m.close()
    cover2 = cover_page(os.path.join(TMP, "cover_sol.pdf"),
                        ["ACCOMMODATION BINDER", "(Solano County)"],
                        ["<i>Gillson v. Landrum, Torres &amp; Zanghi</i>", "Petition for Civil Harassment Restraining Orders (Code Civ. Proc., § 527.6)",
                         "Superior Court of California, County of Solano", "Case No. ____________ – Dept. ______"],
                        "Tab A is filed with the petition. Tab B goes to the Court's ADA Coordinator; Attachment Item 5 and the Declaration Parts B–C are confidential under rule 1.100(c)(4). "
                        "Tab C contains the San Francisco orders referenced in the application.")
    sections2 = [
        ("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Declaration; [Proposed] Order",
         [("Application, Declaration, Proposed Order, Routing Note", os.path.join(ART, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
        ("B", "Request for Accommodations – MC-410 (Solano County)",
         [("MC-410 with Attachment (Items 3-5)", mcsp), med_item]),
        ("C", "San Francisco Superior Court Rule 1.100 Orders and Responses (July–October 2026)", ada_items),
    ]
    n2 = assemble(os.path.join(ART, "Gillson_Solano_Accommodation_Binder.pdf"), "GSB", cover2, sections2,
                  "Gillson – Solano Accommodation Binder – Confidential in part (CRC 1.100(c)(4))")
    print("binder 2 pages", n2)
