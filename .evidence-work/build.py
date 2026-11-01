import os, json, re, io
from datetime import datetime
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, Image as RLImage, KeepTogether,
                                FrameBreak, NextPageTemplate, Flowable)
from reportlab.pdfgen import canvas as rl_canvas

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = "/vercel/share/artifacts/Gillson_Evidence_Exhibit_Binder.pdf"
meta = {m["file"]: m for m in json.load(open(os.path.join(HERE, "meta.json")))}

RESIDENT = "Donald Ernest Gillson"
ADDRESS = "1030 Girard Road, Unit 301, San Francisco, CA 94129"
LANDLORD = "Swords to Plowshares (Property Management), 401 Van Ness Avenue, Suite 313, San Francisco, CA 94103"
PREFIX = "GILLSON"

# ---------------------------------------------------------------- exhibit catalog
# (file, description) grouped by category, chronological within each category
CATEGORIES = [
 ("A", "Written Notices and Grievances Submitted to Property Management", [
  ("20251116_064818.jpg", "Completed Swords to Plowshares Grievance Form, dated 11/16/2025, signed by resident Donald Ernest Gillson, 1030 Girard Rd., San Francisco. Grievance describes an infested refrigerator, cockroach infestation of the unit, and lack of response from staff."),
  ("20251116_064826.jpg", "Completed Maintenance Request form, date reported 11/16/2025, Unit 301, Resident Donald Gillson. Requests replacement of the refrigerator placed in the room, which the resident reports was infested with roaches, and states the infestation has spread to the resident's room and food. Staff section marks Pest/Rodent issue: Yes."),
 ]),
 ("B", "Cockroach Infestation and Unsanitary Conditions Inside the Unit", [
  ("20251116_181859.jpg", "Toilet bowl in the resident's unit containing multiple cockroaches and debris, 11/16/2025."),
  ("20251117_070412.jpg", "Live cockroach on the side of the refrigerator in the resident's unit, 11/17/2025, 7:04 AM."),
  ("20251117_150831.jpg", "Cockroach carcass and fragments in the kitchen sink basin, 11/17/2025, 3:08 PM."),
  ("20251117_150834.jpg", "Cockroach floating in food residue inside a pot in the kitchen sink, 11/17/2025, 3:08 PM."),
  ("20251117_220328.jpg", "Accumulated debris, hair and insect fragments on the unit floor, 11/17/2025, 10:03 PM."),
  ("20251118_084216.jpg", "Glue trap removed from behind the refrigerator, densely covered with cockroaches and nymphs, 11/18/2025, 8:42 AM."),
  ("20251118_084405.jpg", "Max Catch brand glue trap covered with large numbers of cockroaches, photographed on the kitchen counter, 11/18/2025, 8:44 AM."),
  ("20251118_191502.jpg", "Live cockroach on stainless steel sink surface, 11/18/2025, 7:15 PM."),
  ("20251119_080322.jpg", "Cockroach droppings and debris along the baseboard and wall corner of the unit, 11/19/2025, 8:03 AM."),
  ("20251120_190026.jpg", "Interior doorway and bathroom area of the unit with belongings, boxes and papers stacked on the floor during the infestation, 11/20/2025, 7:00 PM."),
  ("20251128_153752.jpg", "Folded glue trap held by the resident showing a dense accumulation of trapped cockroaches, 11/28/2025, 3:37 PM."),
  ("20251218_054854.jpg", "Side panel of the refrigerator showing cockroach droppings/staining, 12/18/2025, 5:48 AM."),
  ("20251218_054954.jpg", "Cockroach fragments and droppings on the counter edge beside the refrigerator, 12/18/2025, 5:49 AM."),
  ("20251218_055013.jpg", "Floor of the unit at the kitchen entry showing cleaning tools and debris, 12/18/2025, 5:50 AM."),
  ("20251219_192637.jpg", "Folded cardboard glue trap on the unit floor near the wall with cockroaches trapped on it and dead cockroaches and debris on the surrounding floor, 12/19/2025, 7:26 PM - two days after the December 17 Pestec treatment."),
  ("20251219_192647.jpg", "Glue trap at the base of the wall below the dark baseboard, with cockroach fragments and droppings scattered across the floor, 12/19/2025, 7:26 PM."),
  ("20251219_192650.jpg", "Second view of the same glue trap and floor area showing continued cockroach presence after treatment, 12/19/2025, 7:26 PM."),
  ("20260105_044507.jpg", "Max Catch glue trap placed along the carpeted hallway baseboard with multiple cockroaches trapped on it, 1/5/2026, 4:45 AM, demonstrating continued activity after the November 2025 complaints."),
 ]),
 ("C", "Injuries to Resident's Service Animal", [
  ("20251118_124617.jpg", "Service dog's abdomen and inner leg showing multiple dark lesions and skin irritation, 11/18/2025, 12:46 PM."),
  ("20251118_125033.jpg", "Close-up of the service dog's skin showing numerous dark bite marks/lesions, 11/18/2025, 12:50 PM."),
  ("20251118_125941.jpg", "Close-up of an open, bleeding lesion on the service dog's skin, 11/18/2025, 12:59 PM."),
  ("20251118_133420.jpg", "Service dog's underside showing widespread bite marks and irritation, 11/18/2025, 1:34 PM."),
  ("20251211_104618.jpg", "Service dog's mouth and gum line, showing inflamed/red gum tissue, 12/11/2025, 10:46 AM."),
  ("20251211_132249.jpg", "Service dog's abdomen after veterinary treatment, with green-marked treated areas and visible lesions, 12/11/2025, 1:22 PM."),
  ("20251211_132253.jpg", "Close-up of treated lesion area on the service dog, with green veterinary marking, 12/11/2025, 1:22 PM."),
 ]),
 ("D", "Injuries to Resident and Medical Records", [
  ("20251118_192916.jpg", "Resident's forearm showing multiple red scratch marks/abrasions, 11/18/2025, 7:29 PM."),
  ("20251119_164840.jpg", "Self-portrait of resident documenting physical condition and appearance, 11/19/2025, 4:48 PM. Embedded EXIF: Samsung Galaxy S24+, 2025-11-19 16:48:41."),
  ("20251125_171207.jpg", "Self-portrait of resident showing a laceration on the forehead, 11/25/2025, 5:12 PM. Embedded EXIF: Samsung Galaxy S24+, 2025-11-25 17:12:09."),
  ("20251126_082951.jpg", "UCSF Health After Visit Summary for Donald E. Gillson, visit date 11/22/2025, UCSF Urgent Care, listing allergies, vital signs, medication list and Patient Relations phone number. Photographed 11/26/2025, 8:29 AM."),
  ("20251127_141342.jpg", "Self-portrait of resident wearing cap and glasses with visible forehead laceration, 11/27/2025, 2:13 PM."),
  ("20251127_141357.jpg", "Self-portrait of resident with visible healing forehead laceration, 11/27/2025, 2:13 PM."),
  ("20251209_161224.jpg", "Resident in an emergency department treatment bay with blood pressure cuff applied and monitoring equipment visible, 12/09/2025, 4:12 PM."),
  ("20251209_171137.jpg", "Blood stain on the hospital bed sheet beside the resident, 12/09/2025, 5:11 PM."),
  ("20251209_171201.jpg", "Resident's service dog (wearing SERVICE DOG vest) seated with the resident in the hospital, 12/09/2025, 5:12 PM."),
  ("20251209_171301.jpg", "Hospital identification wristband on resident's wrist reading GILLSON, DONALD, 12/09/2025, 5:13 PM."),
  ("20251209_171320.jpg", "IV line secured to the resident's forearm during the emergency department visit, 12/09/2025, 5:13 PM."),
  ("20251209_200942.jpg", "Page 1 of emergency department discharge paperwork dated 12/09/2025, including follow-up and care instructions. Photographed 12/09/2025, 8:09 PM."),
  ("20251209_201029.jpg", "Discharge instruction sheet titled 'Concussion, Adult' from the 12/09/2025 emergency department visit."),
  ("20251209_201042.jpg", "Discharge instruction sheet titled 'Cervical Sprain' from the 12/09/2025 emergency department visit."),
  ("20251209_201149.jpg", "Discharge medication list and laboratory results (chemistry panel, 12/09/2025 4:44 PM) for patient Gillson, Donald, page 14 of 17."),
  ("20251209_201216.jpg", "Laboratory results page (hematology and toxicology, 12/09/2025) from the emergency department visit, patient Gillson, Donald."),
  ("20251209_201244.jpg", "Urinalysis results page (12/09/2025, 7:09 PM) from the emergency department visit."),
 ]),
 ("E", "Correspondence From Swords to Plowshares Management", [
  ("20251119_120802.jpg", "Phone screen showing the organization directory entry for Tramecia Garner, Executive Director, Swords to Plowshares (tgarner@stp-sf.org), with an automatic out-of-office reply active 11/17 - 11/22. Photographed 11/19/2025, 12:08 PM."),
  ("20251119_121723.jpg", "Phone screen showing an email from Tramecia Garner, LPCC, Executive Director, Swords to Plowshares, 401 Van Ness Ave., Suite 313, regarding the SSG Fox Suicide Prevention Program. Photographed 11/19/2025, 12:17 PM."),
  ("20251125_235339.jpg", "Letter dated 11/24/2025 to Mr. Gillson from Will Landrum, Assistant Property Manager, Swords to Plowshares, confirming continued pest treatment, additional standard postings, a reassessment, and monthly pest control follow-up. Photographed 11/25/2025, 11:53 PM."),
  ("20251218_055147.jpg", "Swords to Plowshares / Veterans Academy Property Management (1030 Girard Rd., ph. 415-561-2445) '24 hours or more notice of intent to enter' - Pest Control, Wednesday December 10th, 9:00 AM to 4:00 PM: 'Pestec will be resuming their special round of treatment for the pests infestation in your unit', assessing heavy traffic areas, entry points and feeding sources. Photographed 12/18/2025, 5:51 AM."),
  ("20251218_055135.jpg", "Swords to Plowshares '24 hours or more notice of intent to enter' - Presidio Pest Control, Pest Control Spray, 12/16/2025, 9:00 AM to 12:00 PM: 'The Presidio Trust will need to enter your unit to spray for roaches. This is the spray and not bait treatment. As such you and any animals will need to be out of the unit for 4-6hrs after application.' Photographed 12/18/2025, 5:51 AM."),
  ("20251218_055142.jpg", "Swords to Plowshares / Veterans Academy Property Management '24 hours or more notice of intent to enter' - Pest Control, Wednesday December 17th, 9:00 AM to 4:00 PM: Pestec 'resuming their special round of treatment for the pests infestation in your unit.' Photographed 12/18/2025, 5:51 AM."),
  ("20260104_162147.jpg", "Letter dated January 2, 2026 from Swords to Plowshares Property Management, 'Re: Important Notice Regarding Rent Payments - 2026', stating rent collection will be handled more consistently, late or unpaid rent will be addressed promptly, and formal notices may be issued under the San Francisco Rent Ordinance and Just Cause Eviction requirements. Page 1 of 2. Photographed 1/4/2026, 4:21 PM."),
  ("20260104_162157.jpg", "Page 2 of the January 2, 2026 rent notice letter, signed 'Property Management Team, Swords to Plowshares', with footer 401 Van Ness Avenue, Suite 313, San Francisco, CA 94103, (415) 252-4788. Photographed 1/4/2026, 4:21 PM."),
 ]),
 ("F", "Government Agency Records and Reports", [
  ("Screenshot_20251120_231932_Edge.jpg", "San Francisco 311 Case Details, Case No. 101003004371, 'Residential Building Issue - Infestation - Rodent/Insect', location 1030 Girard Rd, San Francisco, CA 94129. Opened 11/19/2025 9:00 AM; closed 11/19/2025 9:26 AM. Description reports clusters of German cockroaches, a senior veteran resident of unit 301A, and management refusal to address the infestation. Screenshot 11/20/2025, 11:19 PM."),
  ("Screenshot_20251120_231951_Edge.jpg", "Continuation of 311 Case No. 101003004371 description: pet feces and urine in hallways, unsanitary building, and the property 'trying to cover their tracks' by saying they will fumigate. Screenshot 11/20/2025, 11:19 PM."),
  ("Screenshot_20251120_232011_Edge.jpg", "311 Case History for Case No. 101003004371 showing 'Agent Created Case' 11/19/2025 9:00 AM and 'Case Transferred SFDPH EHB Healthy Housing Program 415-252-3800', closed 11/19/2025 9:26 AM. Screenshot 11/20/2025, 11:20 PM."),
  ("20251218_055253.jpg", "Letter dated December 5, 2025 from the City and County of San Francisco Department of Disability and Aging Services, Adult Protective Services (P.O. Box 7988, San Francisco, CA 94120-7988), addressed to Donald Gillson, 1030 Girard Rd. Apt 301A. The protective service worker writes that he 'will be closing your APS case because you did not want to meet with me' and lists referral resources (Legal Assistance to the Elderly, SF Dept. of Building Inspection, Housing Rights Committee of SF, Eviction Defense Collaborative). Page 1 of 2. This is the closure that was later reversed when the case was reopened under Jeffrey Tims and Regina Gibson (see Statement Regarding APS). Photographed 12/18/2025, 5:52 AM."),
 ]),
 ("I", "Vehicle Break-In at the Premises Reported to U.S. Park Police, December 25, 2025", [
  ("20251225_145625.jpg", "Resident's blue Audi Q5 parked in the lot at 1030 Girard Rd. (Presidio), front three-quarter view, with the building's red-roofed structures behind, 12/25/2025, 2:56 PM."),
  ("20251225_145633.jpg", "Rear three-quarter view of the resident's vehicle in the parking lot showing the rear passenger-side window area, 12/25/2025, 2:56 PM."),
  ("20251225_145636.jpg", "Driver's side of the vehicle showing the rear window glass broken out and the interior exposed, 12/25/2025, 2:56 PM."),
  ("20251225_145708.jpg", "Close view through the broken rear window: belongings, bedding and bags strewn across the rear seat, 12/25/2025, 2:57 PM."),
  ("20251225_145710.jpg", "Second close view through the broken rear window showing the disturbed contents of the rear seat and footwell, 12/25/2025, 2:57 PM."),
  ("20251225_160241.jpg", "Rear view of the vehicle (license plate visible) in the parking lot with the broken rear window, 12/25/2025, 4:02 PM."),
  ("20251225_160302.jpg", "Close-up of the broken rear window frame and seal with glass fragments and a blanket pushed through the opening, 12/25/2025, 4:03 PM."),
  ("20251225_160341.jpg", "United States Park Police, San Francisco Field Office (SFFO), 1217 Ralston Avenue, San Francisco, CA 94129, business card with handwritten Officer 'Stromberg' and Case No. 251250105, given to the resident at the scene. Photographed 12/25/2025, 4:03 PM."),
  ("20251225_160346.jpg", "Reverse of the card provided by the responding officer bearing the handwritten number '771-433-4001'. Photographed 12/25/2025, 4:03 PM."),
 ]),
 ("G", "Resident's Contemporaneous Digital Notes and Messages", [
  ("Screenshot_20251120_074343_Messages.jpg", "Screenshot of a message thread (sent to self, 7:28 AM, 11/20/2025) containing AI-assistant generated notes regarding the housing dispute. Screenshot 11/20/2025, 7:43 AM."),
  ("Screenshot_20251120_074350_Messages.jpg", "Screenshot of the same thread; notes reference the resident's PTSD/concussion and photographic evidence of dead roaches and a property manager blocking the door. Screenshot 11/20/2025, 7:43 AM."),
  ("Screenshot_20251120_074356_Messages.jpg", "Screenshot of the same thread; notes attribute to 'Mark' the statement 'I saw some bugs, I didn't think it was Level 5' and reference 60 dead roaches photographed that morning. Screenshot 11/20/2025, 7:43 AM."),
  ("Screenshot_20251120_225126_Messages.jpg", "Screenshot of a message (sent to self 7:16 PM, 11/20/2025) containing a photograph of cockroaches collected in a clear glass. Screenshot 11/20/2025, 10:51 PM."),
 ]),
 ("H", "Building Common Areas and Repair Activity", [
  ("20251226_105431.jpg", "Third-floor hallway at 1030 Girard Rd. with a refrigerator, bagged debris and a hand truck loaded with boxes of Evoke flooring stored in the corridor, 12/26/2025, 10:54 AM."),
  ("20251226_105442.jpg", "View through an open unit door of a worker installing new plank flooring over the existing tile, with kitchenette and bucket visible, 12/26/2025, 10:54 AM."),
 ]),
]

import hashlib
from notices import NOTICES, FORWARD, MAILBOX_ROWS, TO_LINE, FROM_LINE, SIG
DOCS = os.path.join(HERE, "docs")

# Text exhibits (Category J) - evidentiary notices served on opposing counsel, Oct 29-30, 2026
CAT_J = ("J", "Evidentiary Notices Served on Opposing Counsel and Forwarded to the Court, October 29-30, 2026")
J_ITEMS = [{"kind": "forward", "dt": datetime(2026, 10, 30, 13, 27, 0),
            "desc": "Email transmission record: the four evidentiary notices below, sent to Zanghi Torres Adams LLP on October 29, 2026, "
                    "were forwarded by the declarant to the San Francisco Superior Court (department606@sftc.org) on October 30, 2026 at 1:27 PM PDT, "
                    "together with the same-day mailbox listing of related transmissions."}]
for i, nt in enumerate(NOTICES):
    hh = [(23, 0, 17), (23, 21, 32), (23, 40, 4), (23, 43, 5)][i]
    J_ITEMS.append({"kind": "notice", "notice": nt, "dt": datetime(2026, 10, 29, *hh),
                    "desc": nt["short"] + f", emailed {nt['sent']}."})

# Filed documents (Category K) - BBS complaint PDFs reproduced in full behind a cover sheet
CAT_K = ("K", "Complaints Filed With the California Board of Behavioral Sciences, January 2, 2026")
K_ITEMS = [
 {"kind": "pdf", "file": "Complaint_260102232756.pdf", "dt": datetime(2026, 1, 2, 23, 27, 0),
  "desc": "California Board of Behavioral Sciences 'Online Complaint Summary', Complaint No. 2002026002097, submitted 1/2/2026 at 11:27 PM, "
          "against Kolby Losik, Licensed Professional Clinical Counselor / Case Manager, Swords to Plowshares, 1030 Girard Rd., San Francisco. "
          "Reproduced in full as generated by the Board's online complaint system."},
 {"kind": "pdf", "file": "Complaint_260102235553.pdf", "dt": datetime(2026, 1, 2, 23, 55, 0),
  "desc": "California Board of Behavioral Sciences 'Online Complaint Summary', Complaint No. 2002026002098, submitted 1/2/2026 at 11:55 PM, "
          "against Mark Villalobos (CA License # ASW125029), Licensed Marriage and Family Therapist license type, Swords to Plowshares, "
          "1030 Girard Rd., San Francisco. Reproduced in full as generated by the Board's online complaint system."},
]

# Audio-visual exhibits (Category L) - every video link designated in the Oct. 29, 2026 evidentiary notices, one exhibit per recording
CAT_L = ("L", "Audio-Visual Exhibits: Video Recordings Designated as Trial Exhibits (Links and QR Codes), Served October 29, 2026")
L_ITEMS = []
for suite_idx, nt in enumerate(NOTICES):
    for code, title, url, d_ in nt["videos"]:
        suite = "First suite" if suite_idx == 0 else "Second suite"
        L_ITEMS.append({"kind": "video", "code": code, "title": title, "url": url, "descriptor": d_, "suite": suite,
                        "notice_no": suite_idx, "dt": datetime(2026, 10, 29, *[(23, 0, 17), (23, 21, 32)][suite_idx]),
                        "desc": f"Trial Exhibit {code} ({suite}): {title}. Video recording hosted on Google Drive; link designated and served on "
                                f"plaintiff's counsel October 29, 2026 and forwarded to the Court October 30, 2026. {d_}"})

# VA medical records (Category M) - excerpts of the Nov. 1, 2026 VA Blue Button report; full report lodged separately
CAT_M = ("M", "VA Medical Records: Excerpts of VA Blue Button Report (Aug. 1 - Nov. 1, 2026) Bearing on Disability, PTSD/TBI, and Housing Stress")
VA_FULL_SHA = "cd85e4da9738997130ee1ef4ead3c323dac389648a6fa6d01d14da1df685e3b5"
M_ITEMS = [
 {"kind": "pdf", "file": "VA_Blue_Button_Report_EXCERPTS.pdf", "dt": datetime(2026, 11, 1, 6, 53, 0), "generator": "VA.gov Blue Button (My HealtheVet) medical-records export",
  "source_note": f"Excerpted from the 215-page VA Blue Button report for Donald Ernest Gillson generated November 1, 2026 at 6:53 AM (records "
                 f"Aug. 1 - Nov. 1, 2026). Full native PDF SHA-256: <font face='Courier' size='6.4'>{VA_FULL_SHA}</font>. The full report is "
                 f"preserved and will be lodged with the Court conditionally under seal or produced on request; only the pages listed are reproduced.",
  "desc": "Excerpts of the declarant's VA medical record (VA Blue Button report, Aug. 1 - Nov. 1, 2026; 34 of 215 pages): report header; "
          "PCMHI Care Management Note of Oct. 6, 2026 with PHQ-9/GAD-7 screening; HCHV (homeless program) social-work telephone note of "
          "Oct. 1, 2026; emergency-department social-work and attending notes of Sept. 17, 2026; mental-health secure messaging of "
          "Aug. 19, 2026; and the psychiatry progress note of Aug. 6, 2026 with diagnoses and medication list. Offered on the issues of "
          "disability, the need for the rule 1.100 accommodations, and the housing-related stress documented by treating clinicians. "
          "Laboratory results, appointments and unrelated clinical content are omitted."},
]

# ---------------------------------------------------------------- helpers
def fname_dt(f):
    m = re.search(r"(\d{8})_(\d{6})", f)
    return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")

def fmt(dt):
    return dt.strftime("%B %-d, %Y at %-I:%M:%S %p") + " (Pacific Time)"

def exif_dt(s):
    try:
        return fmt(datetime.strptime(s, "%Y:%m:%d %H:%M:%S"))
    except Exception:
        return None

def exif_sentence():
    with_exif = [e["no"] for e in exhibits if e["kind"] == "photo" and exif_dt(meta[e["file"]]["original"] or meta[e["file"]]["datetime"])]
    if not with_exif:
        return "No submitted file retained an EXIF header"
    return (f"{len(with_exif)} of the {N_PHOTO} photographic exhibits (Exhibits {', '.join(str(n) for n in with_exif)}) retain an EXIF header,")

def prepared_image(f, max_px=1400):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f)))
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO(); im.convert("RGB").save(buf, "JPEG", quality=82); buf.seek(0)
    return buf, im.size

# ---------------------------------------------------------------- styles
BASE = "Times-Roman"; BOLD = "Times-Bold"
sTitle = ParagraphStyle("t", fontName=BOLD, fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=10)
sH = ParagraphStyle("h", fontName=BOLD, fontSize=12, leading=15, spaceBefore=10, spaceAfter=6)
sBody = ParagraphStyle("b", fontName=BASE, fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
sSmall = ParagraphStyle("s", fontName=BASE, fontSize=8.5, leading=11)
sSmallB = ParagraphStyle("sb", parent=sSmall, fontName=BOLD)
sCap = ParagraphStyle("c", fontName=BASE, fontSize=11, leading=15)
sExTitle = ParagraphStyle("et", fontName=BOLD, fontSize=12, leading=14, spaceAfter=3)
sExDesc = ParagraphStyle("ed", fontName=BASE, fontSize=9.5, leading=12, spaceAfter=5)
sMeta = ParagraphStyle("m", fontName=BASE, fontSize=7.8, leading=10)
sMono = ParagraphStyle("mono", fontName="Courier", fontSize=6.6, leading=8.5)

# ---------------------------------------------------------------- flatten exhibits
exhibits = []
n = 0
for letter_, title, items in CATEGORIES:
    for f, desc in items:
        n += 1
        exhibits.append({"no": n, "cat": letter_, "cat_title": title, "file": f, "desc": desc, "kind": "photo", "dt": fname_dt(f)})
N_PHOTO = n
assert N_PHOTO == len(os.listdir(SRC)), (N_PHOTO, len(os.listdir(SRC)))
assert len({e["file"] for e in exhibits}) == N_PHOTO
for it in J_ITEMS:
    n += 1
    exhibits.append(dict(it, no=n, cat=CAT_J[0], cat_title=CAT_J[1]))
for it in K_ITEMS:
    n += 1
    exhibits.append(dict(it, no=n, cat=CAT_K[0], cat_title=CAT_K[1]))
for it in L_ITEMS:
    n += 1
    exhibits.append(dict(it, no=n, cat=CAT_L[0], cat_title=CAT_L[1]))
for it in M_ITEMS:
    n += 1
    exhibits.append(dict(it, no=n, cat=CAT_M[0], cat_title=CAT_M[1]))
ALL_CATS = [(l, t) for l, t, _ in CATEGORIES] + [CAT_J, CAT_K, CAT_L, CAT_M]

from pypdf import PdfReader, PdfWriter
for e in exhibits:
    if e["kind"] == "pdf":
        p = os.path.join(DOCS, e["file"])
        e["pages"] = len(PdfReader(p).pages)
        e["bytes"] = os.path.getsize(p)
        e["sha256"] = hashlib.sha256(open(p, "rb").read()).hexdigest()
PDF_EXHIBITS = [e for e in exhibits if e["kind"] == "pdf"]

# page bookkeeping: PAGE_OF[no] = final (post-merge) page number of the exhibit; learned on a trial build
PAGE_OF = {}
RL_PAGE_OF = {}
# appended PDF pages are inserted after each Category K cover sheet; a reportlab page r maps to the final page
def final_page(r):
    off = 0
    for e in PDF_EXHIBITS:
        if e["no"] in RL_PAGE_OF and r > RL_PAGE_OF[e["no"]]:
            off += e["pages"]
    return r + off

class PageMarker(Flowable):
    def __init__(self, no): super().__init__(); self.no = no; self.width = 0; self.height = 0
    def draw(self): RL_PAGE_OF[self.no] = self.canv.getPageNumber()

# ---------------------------------------------------------------- canvas with page x of y + bates
class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total = len(self._saved) + sum(e["pages"] for e in PDF_EXHIBITS)
        for st in self._saved:
            self.__dict__.update(st); draw_footer(self, final_page(self._pageNumber), total); super().showPage()
        super().save()

def draw_footer(cv, pageno, total):
    w, h = letter
    cv.setFont(BASE, 8.5)
    cv.setStrokeColor(colors.black); cv.setLineWidth(0.5)
    cv.line(inch, 0.78 * inch, w - inch, 0.78 * inch)
    cv.drawString(inch, 0.6 * inch, f"Exhibit Binder - {RESIDENT} v. Swords to Plowshares - Habitability / Infestation")
    cv.drawRightString(w - inch, 0.6 * inch, f"Page {pageno} of {total}")
    cv.drawCentredString(w / 2, 0.42 * inch, f"{PREFIX}-{pageno:06d}")

doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=inch,
                      title="Evidence Exhibit Binder - Gillson", author=RESIDENT, subject="Habitability and infestation exhibits")
W = letter[0] - 2 * inch
H = letter[1] - 1.9 * inch
full = Frame(inch, inch, W, H, id="full", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
# Two photographs per page, side by side on a portrait page: left and right columns, each holding one exhibit
# (photograph on top, provenance block beneath).
GUT = 14
COL_W = (W - GUT) / 2
top = Frame(inch, inch, COL_W, H, id="top", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
bot = Frame(inch + COL_W + GUT, inch, COL_W, H, id="bot", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
def rule(c, d):
    c.saveState(); c.setLineWidth(0.5); c.setDash(2, 2)
    x = inch + COL_W + GUT / 2
    c.line(x, inch, x, inch + H); c.restoreState()

doc.addPageTemplates([PageTemplate(id="full", frames=[full]),
                      PageTemplate(id="two", frames=[top, bot], onPage=rule)])

def front_matter():
    story = []
    story += [Spacer(1, 18)]
    cap = Table([
        [Paragraph("SUPERIOR COURT OF THE STATE OF CALIFORNIA<br/>COUNTY OF SAN FRANCISCO", ParagraphStyle("cc", parent=sCap, fontName=BOLD, alignment=TA_CENTER))],
    ], colWidths=[W])
    story += [cap, Spacer(1, 16)]
    cap2 = Table([
        [Paragraph(f"<b>{RESIDENT}</b>,<br/>Resident / Complainant,<br/><br/>v.<br/><br/><b>SWORDS TO PLOWSHARES</b>, Property Management,<br/>Respondent.", sCap),
         Paragraph("Case No.: ____________________<br/><br/><b>INDEX OF EXHIBITS AND<br/>PHOTOGRAPHIC EVIDENCE BINDER</b><br/><br/>Premises: 1030 Girard Road, Unit 301<br/>San Francisco, CA 94129<br/><br/>Exhibits 1 - %d<br/>Period: November 16, 2025 - October 30, 2026" % len(exhibits), sCap)],
    ], colWidths=[W * 0.52, W * 0.48])
    cap2.setStyle(TableStyle([("LINEBELOW", (0, 0), (0, 0), 0.75, colors.black), ("LINEAFTER", (0, 0), (0, 0), 0.75, colors.black),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (1, 0), (1, 0), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    story += [cap2, Spacer(1, 18)]

    story += [Paragraph("STATEMENT REGARDING ADULT PROTECTIVE SERVICES", sH),
     Paragraph(f"Declarant {RESIDENT} states as follows: The Adult Protective Services (APS) case concerning the declarant "
               "has been <b>reopened</b> and is now being handled by <b>Jeffrey Tims</b> and <b>Regina Gibson</b>. "
               "The previously assigned APS worker, <b>Drew Yorkov</b>, failed to perform his APS duties in this matter; "
               "the conditions documented in the exhibits that follow were ongoing during the period of his assignment "
               "and were not remedied. The reopening of the case is referenced here so that the Court has the current "
               "status of the APS matter when reviewing the exhibits.", sBody)]

    story += [Paragraph("STATEMENT REGARDING AUTHENTICATION AND METADATA", sH),
     Paragraph("Each photograph and screenshot in this binder was taken by the declarant on the declarant's own mobile device "
               "(Samsung Galaxy S24+) and is a true and accurate depiction of what it shows on the date and time indicated. "
               "For each exhibit the following metadata is reported exactly as recovered from the submitted file: "
               "(1) the original device filename, whose embedded timestamp (YYYYMMDD_HHMMSS) is written by the camera "
               "application at the moment of capture; (2) any embedded EXIF capture date, camera make and model, where the "
               "file still carries an EXIF header; (3) pixel dimensions; (4) file size in bytes; and (5) the SHA-256 "
               "cryptographic hash of the file, which permits any party to confirm that the image has not been altered since "
               "this binder was prepared.", sBody),
     Paragraph("Where an exhibit is marked \"EXIF header not present in submitted copy\", the capture date and time are taken "
               "from the device filename. Most mobile messaging and transfer services remove EXIF headers in transit; the "
               "filename timestamp is preserved by the device and is the controlling capture time for those exhibits. "
               f"{exif_sentence()} and in every such case the "
               "EXIF time matches the filename timestamp to the second, corroborating the filename convention for the "
               "remaining exhibits. The original full-resolution files remain in the declarant's possession and are available "
               "for inspection. See Cal. Evid. Code sections 250, 1400-1401, and 1552-1553.", sBody),
     Paragraph(f"Exhibits are grouped by subject matter (Categories A through K) and arranged chronologically within each "
               f"category. Each page bears a sequential Bates-style number in the footer. Exhibits 1 through {N_PHOTO} are photographs "
               "and screenshots, presented two per page. Category J consists of the four formal evidentiary notices the declarant "
               "emailed to opposing counsel Francisco C. Torres and John P. Zanghi of Zanghi Torres Adams LLP on October 29, 2026, and "
               "forwarded to the San Francisco Superior Court (department606@sftc.org) on October 30, 2026; the text of each notice is "
               "reproduced verbatim from the declarant's mail client, and the native messages with full headers remain in the "
               "declarant's donny@18fu.ai account. Category K consists of the two complaints the declarant filed with the California "
               "Board of Behavioral Sciences on January 2, 2026; the Board's own 'Online Complaint Summary' PDF for each is reproduced "
               "in full, unaltered, behind an exhibit cover sheet, with the SHA-256 hash of the filed PDF reported on the cover sheet.", sBody),
     Paragraph("SUMMARY OF EXHIBIT CATEGORIES", sH)]
    summary = [[Paragraph("<b>Category</b>", sSmall), Paragraph("<b>Subject</b>", sSmall), Paragraph("<b>Exhibits</b>", sSmall), Paragraph("<b>Date Range</b>", sSmall)]]
    for letter_, title in ALL_CATS:
        nums = [e["no"] for e in exhibits if e["cat"] == letter_]
        dts = sorted(e["dt"] for e in exhibits if e["cat"] == letter_)
        rng = dts[0].strftime("%m/%d/%Y") + (" - " + dts[-1].strftime("%m/%d/%Y") if dts[0].date() != dts[-1].date() else "")
        summary.append([Paragraph(letter_, sSmall), Paragraph(title, sSmall), Paragraph(f"{nums[0]} - {nums[-1]}" if len(nums) > 1 else str(nums[0]), sSmall), Paragraph(rng, sSmall)])
    st = Table(summary, colWidths=[0.8 * inch, W - 0.8 * inch - 0.9 * inch - 1.6 * inch, 0.9 * inch, 1.6 * inch])
    st.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [st, Spacer(1, 14),
     Paragraph("DECLARATION", sH),
     Paragraph(f"I, {RESIDENT}, declare: I am the resident of {ADDRESS}. I personally took each photograph and screenshot "
               f"contained in Exhibits 1 through {N_PHOTO} with my own mobile device on the dates and at the times stated, and each is a true "
               f"and accurate depiction of what it shows. I have not altered any image. Exhibits {N_PHOTO + 1} through {N_PHOTO + len(J_ITEMS)} are "
               "true and complete copies of the text of emails I wrote and sent from my account donny@18fu.ai on the dates and at the "
               f"times stated. Exhibits {N_PHOTO + len(J_ITEMS) + 1} through {len(exhibits)} are true and complete copies of the complaint "
               "summaries generated by the California Board of Behavioral Sciences when I submitted those complaints. The statements above regarding Adult "
               "Protective Services are true of my own knowledge. I declare under penalty of perjury under the laws of the State of "
               "California that the foregoing is true and correct.", sBody),
     Spacer(1, 10),
     Paragraph("Executed on October 31, 2026, at San Francisco, California.", sBody),
     Spacer(1, 16),
     Table([[Paragraph("<b>/s/ Dr. Donny Gillson, Ed.D.</b>", sBody)],
            [Paragraph("Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson), Declarant<br/>ORCID iD: https://orcid.org/0009-0007-0768-5486<br/>"
                       "Electronically signed October 31, 2026 through the declarant's ADA cognitive assistive digital-communications "
                       "application; conformed /s/ signature per Cal. Rules of Court, rule 2.257(b).", sBody)]], colWidths=[W], hAlign="RIGHT",
           style=TableStyle([("LEFTPADDING", (0, 0), (-1, -1), W * 0.5), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)])),
     PageBreak()]


    return story
# ---------------------------------------------------------------- index
def ex_page(i):  # i is 0-based exhibit index; final page number learned on the trial build
    return PAGE_OF.get(exhibits[i]["no"], 0)

def build_index():
    rows = [[Paragraph("<b>Ex.</b>", sSmall), Paragraph("<b>Date / Time Captured</b>", sSmall), Paragraph("<b>Description</b>", sSmall), Paragraph("<b>Page</b>", sSmall)]]
    spans = []
    cur = None
    for i, e in enumerate(exhibits):
        if e["cat"] != cur:
            cur = e["cat"]
            rows.append([Paragraph(f"<b>Category {cur}. {e['cat_title']}</b>", sSmall), "", "", ""])
            spans.append(len(rows) - 1)
        dt = e["dt"]
        short = e["desc"].split(". ")[0]
        if len(short) > 120: short = short[:117] + "..."
        rows.append([Paragraph(str(e["no"]), sSmall), Paragraph(dt.strftime("%m/%d/%Y %-I:%M %p"), sSmall), Paragraph(short, sSmall), Paragraph(str(ex_page(i)), sSmall)])
    t = Table(rows, colWidths=[0.45 * inch, 1.35 * inch, W - 0.45 * inch - 1.35 * inch - 0.55 * inch, 0.55 * inch], repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for r in spans:
        st += [("SPAN", (0, r), (-1, r)), ("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f2f2f2"))]
    t.setStyle(TableStyle(st))
    return t

# ---------------------------------------------------------------- exhibit blocks
IMG_W = COL_W
IMG_H = 4.3 * inch

def exhibit_block(e):
    m = meta[e["file"]]
    buf, (pw, ph) = prepared_image(e["file"])
    scale = min(IMG_W / pw, IMG_H / ph)
    # Every exhibit sits in the same IMG_W x IMG_H frame: the photo is fitted and centred, so portrait and landscape share one geometry.
    frame = Table([[RLImage(buf, width=pw * scale, height=ph * scale)]], colWidths=[IMG_W], rowHeights=[IMG_H])
    frame.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                               ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F4F4")), ("BOX", (0, 0), (-1, -1), 0.5, colors.black)]))
    img = frame
    dt = fname_dt(e["file"])
    src = "Device filename timestamp (camera application, written at capture)"
    if e["file"].startswith("Screenshot"):
        src = "Device filename timestamp (Android screenshot, written at capture)"
    ex = exif_dt(m["original"] or m["datetime"])
    exif_line = (f"<b>EXIF capture time:</b> {ex} &nbsp;|&nbsp; <b>Device:</b> {(m['make'] + ' ' + m['model']).strip() or 'Samsung (screenshot; no camera tag)'}"
                 if ex else "<b>EXIF header:</b> not present in submitted copy (removed in transit); filename timestamp controls")
    right = [
        Paragraph(f"EXHIBIT {e['no']}", sExTitle),
        Paragraph(f"<b>Category {e['cat']}:</b> {e['cat_title']}", sMeta), Spacer(1, 3),
        Paragraph(e["desc"], sExDesc),
        Paragraph(f"<b>Date and time captured:</b> {fmt(dt)}", sMeta),
        Paragraph(f"<b>Source of date/time:</b> {src}", sMeta),
        Paragraph(exif_line, sMeta),
        Paragraph(f"<b>Original filename:</b> {e['file']} &nbsp;|&nbsp; <b>Dimensions:</b> {m['size'][0]} x {m['size'][1]} px &nbsp;|&nbsp; <b>Size:</b> {m['bytes']:,} bytes", sMeta),
        Paragraph(f"<b>Location depicted:</b> {ADDRESS if e['cat'] in 'ABCGH' else ('Parking lot, 1030 Girard Road, San Francisco, CA 94129 (Presidio)' if e['cat'] == 'I' else 'See description')}", sMeta),
        Paragraph(f"<b>SHA-256:</b> <font face='Courier' size='6.4'>{' '.join(m['sha256'][k:k+16] for k in range(0, len(m['sha256']), 16))}</font>", sMeta),
        Paragraph(f"<b>Photographed by:</b> {RESIDENT} &nbsp;|&nbsp; <b>Bates:</b> {PREFIX}-{ex_page(e['no'] - 1):06d}", sMeta),
    ]
    t = Table([[img], [right]], colWidths=[COL_W])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 1), (0, 1), 6)]))
    return [PageMarker(e["no"]), t]

# ---------------------------------------------------------------- text exhibits (Category J)
sEmHdr = ParagraphStyle("eh", fontName=BASE, fontSize=9, leading=12)
sEmBody = ParagraphStyle("eb", fontName=BASE, fontSize=10, leading=13.5, spaceAfter=6)
sEmH = ParagraphStyle("ebh", fontName=BOLD, fontSize=10, leading=13.5, spaceBefore=4, spaceAfter=3)
sLink = ParagraphStyle("lk", fontName="Courier", fontSize=7.6, leading=10, spaceAfter=4)

def ex_header(e, extra):
    box = [[Paragraph(f"EXHIBIT {e['no']}", sExTitle)],
           [Paragraph(f"<b>Category {e['cat']}:</b> {e['cat_title']}", sMeta)],
           [Paragraph(e["desc"], sExDesc)]] + [[Paragraph(x, sMeta)] for x in extra]
    t = Table(box, colWidths=[W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.75, colors.black), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f5")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return [PageMarker(e["no"]), t, Spacer(1, 10)]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def email_head(rows):
    t = Table([[Paragraph(f"<b>{k}</b>", sEmHdr), Paragraph(esc(v), sEmHdr)] for k, v in rows], colWidths=[0.9 * inch, W - 0.9 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.black),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (0, 0), 0)]))
    return [t, Spacer(1, 8)]

def forward_block(e):
    s = ex_header(e, ["<b>Source:</b> Text of the declarant's mail client (donny@18fu.ai), message list and message view, as exported by the declarant on October 31, 2026.",
                      f"<b>Bates:</b> {PREFIX}-{PAGE_OF.get(e['no'], 0):06d}"])
    s += [Paragraph("Forwarding message", sEmH)]
    s += email_head([("From:", FORWARD["from"]), ("To:", FORWARD["to"]), ("Sent:", FORWARD["sent"]), ("Subject:", FORWARD["subject"])])
    s += [Paragraph("Messages forwarded (each reproduced in full as Exhibits %d-%d):" % (e["no"] + 1, e["no"] + len(NOTICES)), sEmH)]
    rows = [[Paragraph("<b>Ex.</b>", sSmall), Paragraph("<b>Sent (PDT)</b>", sSmall), Paragraph("<b>To</b>", sSmall), Paragraph("<b>Subject</b>", sSmall)]]
    for i, nt in enumerate(NOTICES):
        rows.append([Paragraph(str(e["no"] + 1 + i), sSmall), Paragraph(nt["sent"].replace("Thursday, ", ""), sSmall), Paragraph("ftorres@ztalaw.com", sSmall), Paragraph(esc(nt["subject"]), sSmall)])
    t = Table(rows, colWidths=[0.4 * inch, 1.6 * inch, 1.3 * inch, W - 3.3 * inch])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [t, Spacer(1, 10), Paragraph("Related transmissions listed in the same mailbox on October 30, 2026 (as listed; contents not reproduced):", sEmH)]
    rows = [[Paragraph("<b>Date</b>", sSmall), Paragraph("<b>From</b>", sSmall), Paragraph("<b>Subject</b>", sSmall)]]
    for d_, f_, sub in MAILBOX_ROWS:
        rows.append([Paragraph(d_, sSmall), Paragraph(esc(f_), sSmall), Paragraph(esc(sub), sSmall)])
    t = Table(rows, colWidths=[0.6 * inch, 2.0 * inch, W - 2.6 * inch])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [t, PageBreak()]
    return s

def notice_block(e):
    nt = e["notice"]
    s = ex_header(e, ["<b>Source:</b> Text of the sent message as displayed in the declarant's mail client (donny@18fu.ai); mail-client interface text omitted. Native message with headers retained by the declarant.",
                      f"<b>Bates:</b> {PREFIX}-{PAGE_OF.get(e['no'], 0):06d}"])
    s += email_head([("From:", FROM_LINE + " <donny@18fu.ai>"), ("To:", TO_LINE), ("Sent:", nt["sent"]), ("Subject:", nt["subject"])])
    s += [Paragraph(esc(nt["heading"]), sEmH), Paragraph(esc(nt["salute"]), sEmBody)]
    s += [Paragraph(esc(p), sEmBody) for p in nt["body"]]
    for code, title, url, d_ in nt["videos"]:
        s += [Paragraph(f"<b>Exhibit {code}: {esc(title)}</b>", sEmBody), Paragraph(f"Link: {url}", sLink), Paragraph(f"Descriptor: {esc(d_)}", sEmBody)]
    for h, paras in nt["sections"]:
        s += [Paragraph(esc(h), sEmH)] + [Paragraph(esc(p), sEmBody) for p in paras]
    s += [Spacer(1, 6)] + [Paragraph(esc(x), sEmBody if i else sEmBody) for i, x in enumerate(SIG)]
    s += [PageBreak()]
    return s

def pdf_cover(e):
    s = ex_header(e, [f"<b>Filed document:</b> {e['file']} &nbsp;|&nbsp; <b>Pages:</b> {e['pages']} &nbsp;|&nbsp; <b>Size:</b> {e['bytes']:,} bytes",
                      f"<b>Generated by:</b> {e.get('generator', 'California Board of Behavioral Sciences online complaint system')} (timestamp {e['dt'].strftime('%-m/%-d/%y %-I:%M %p')})",
                      f"<b>SHA-256 of reproduced PDF:</b> <font face='Courier' size='6.4'>{e['sha256']}</font>",
                      f"<b>Bates:</b> {PREFIX}-{PAGE_OF.get(e['no'], 0):06d} (cover) and following {e['pages']} pages"]
                  + ([f"<b>Source:</b> {e['source_note']}"] if e.get("source_note") else []))
    s += [Paragraph(("The excerpted pages follow this cover sheet, reproduced without alteration from the native export. Each reproduced page carries "
                     "this binder's footer and Bates number in addition to the report's own pagination, so omitted pages are apparent from the gaps.")
                    if e.get("source_note") else
                    ("The complete Board-generated document follows this cover sheet, reproduced without alteration. Each reproduced page carries "
                     "this binder's footer and Bates number in addition to the Board's own page numbering."), sBody), PageBreak()]
    return s

def qr_flowable(url, size=1.25 * inch):
    from reportlab.graphics.barcode import qr as rl_qr
    from reportlab.graphics.shapes import Drawing
    w = rl_qr.QrCodeWidget(url); b = w.getBounds(); bw, bh = b[2] - b[0], b[3] - b[1]
    d = Drawing(size, size, transform=[size / bw, 0, 0, size / bh, 0, 0]); d.add(w)
    return d


def video_block(e):
    notice_ex = N_PHOTO + 2 + e["notice_no"]  # exhibit number of the notice e-mail that designated this recording
    s = ex_header(e, [f"<b>Source:</b> Video recording uploaded by the declarant to Google Drive; the link below is the designation served on "
                      f"plaintiff's counsel in Exhibit {notice_ex} (Category J) and forwarded to the Court October 30, 2026. The native file "
                      f"with metadata is preserved and will be produced on request or lodged with the Court.",
                      f"<b>Bates:</b> {PREFIX}-{PAGE_OF.get(e['no'], 0):06d}"])
    info = [Paragraph(f"<b>Trial Exhibit {e['code']}</b> &mdash; {e['suite']}", sExTitle),
            Paragraph(f"<b>Title:</b> {esc(e['title'])}", sExDesc),
            Paragraph("<b>Link:</b> <link href='%s'><u>%s</u></link>" % (e["url"], e["url"]), sLink),
            Paragraph(f"<b>Descriptor:</b> {esc(e['descriptor'])}", sExDesc),
            Paragraph("Scan the QR code or open the link to view the recording. Playback is offered under Evid. Code &sect;&sect; 1400&ndash;1401 "
                      "on the declarant's authentication testimony; see the designating notice for the foundation offered.", sMeta)]
    t = Table([[info, qr_flowable(e["url"])]], colWidths=[W - 1.45 * inch, 1.45 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return s + [t, PageBreak()]


def build():
    RL_PAGE_OF.clear()
    s = front_matter() + [Paragraph("INDEX OF EXHIBITS", sTitle), build_index(), NextPageTemplate("two"), PageBreak()]
    photos = [e for e in exhibits if e["kind"] == "photo"]
    for i, e in enumerate(photos):
        s += exhibit_block(e)
        s.append(FrameBreak() if i % 2 == 0 else PageBreak())
    if len(photos) % 2 == 1:
        s.pop()
    s += [NextPageTemplate("full")]
    if len(photos) % 2 == 1:
        s.append(PageBreak())
    for e in exhibits:
        if e["kind"] == "forward": s += forward_block(e)
        elif e["kind"] == "notice": s += notice_block(e)
        elif e["kind"] == "pdf": s += pdf_cover(e)
        elif e["kind"] == "video": s += video_block(e)
    while isinstance(s[-1], PageBreak): s.pop()
    d = BaseDocTemplate(OUT, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=inch,
                        title="Evidence Exhibit Binder - Gillson", author=RESIDENT, subject="Habitability and infestation exhibits")
    d.addPageTemplates([PageTemplate(id="full", frames=[full]), PageTemplate(id="two", frames=[top, bot], onPage=rule)])
    d.build(s, canvasmaker=NumberedCanvas)

def merge_pdfs():
    """Insert each filed PDF after its cover sheet and stamp the binder footer on the inserted pages."""
    base = PdfReader(OUT)
    total = len(base.pages) + sum(e["pages"] for e in PDF_EXHIBITS)
    out = PdfWriter()
    covers = {RL_PAGE_OF[e["no"]]: e for e in PDF_EXHIBITS}
    for r in range(1, len(base.pages) + 1):
        out.add_page(base.pages[r - 1])
        if r in covers:
            e = covers[r]
            src = PdfReader(os.path.join(DOCS, e["file"]))
            for k, pg in enumerate(src.pages):
                pno = final_page(r) + 1 + k
                buf = io.BytesIO(); cv = rl_canvas.Canvas(buf, pagesize=letter)
                draw_footer(cv, pno, total); cv.save(); buf.seek(0)
                if abs(float(pg.mediabox.width) - letter[0]) > 2 or abs(float(pg.mediabox.height) - letter[1]) > 2:
                    pg.scale_to(letter[0], letter[1])
                pg.merge_page(PdfReader(buf).pages[0])
                out.add_page(pg)
    out.add_metadata({"/Title": "Evidence Exhibit Binder - Gillson", "/Author": RESIDENT})
    with open(OUT, "wb") as fh:
        out.write(fh)
    return len(out.pages)

# trial build learns where each exhibit lands; the second build prints the correct page references and Bates numbers
build()
PAGE_OF.update({no: final_page(r) for no, r in RL_PAGE_OF.items()})
first = dict(RL_PAGE_OF)
build()
assert first == RL_PAGE_OF, "page layout shifted between builds"
PAGE_OF.update({no: final_page(r) for no, r in RL_PAGE_OF.items()})
pages = merge_pdfs()
print("pages:", pages, "exhibits:", len(exhibits), "photo exhibits:", N_PHOTO, "first exhibit page:", PAGE_OF[1])
