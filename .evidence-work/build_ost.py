from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap, os

OUT = "/vercel/share/artifacts/Gillson_Solano_OST_and_Accommodation_Request.pdf"

W, H = letter
LM, RM, TM, BM = 1.35 * inch, 1.0 * inch, 0.9 * inch, 0.85 * inch
TEXT_W = W - LM - RM


def wrap_measured(text, font, size, max_w, first_indent="", next_indent=""):
    """Wrap by actual glyph width so no line crosses the right rule."""
    words = text.split()
    lines, cur, prefix = [], "", first_indent
    for w in words:
        trial = (cur + " " + w) if cur else w
        if pdfmetrics.stringWidth(prefix + trial, font, size) <= max_w:
            cur = trial
        else:
            lines.append(prefix + cur)
            cur, prefix = w, next_indent
    if cur:
        lines.append(prefix + cur)
    return lines
LEAD = 24  # double-spaced pleading lines
LINES = 28
FONT = "Times-Roman"
BOLD = "Times-Bold"
ITAL = "Times-Italic"
FS = 12

CASE_NO = "____________________"
FOOTERS = {}

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("Ex Parte Application for Order Shortening Time and Rule 1.100 Accommodation Request")
c.setAuthor("Dr. Donny Gillson, Ed.D.")

state = {"page": 0, "line": 0, "footer": ""}


def pleading_frame():
    # line numbers and rules
    c.setFont("Times-Roman", 10)
    y0 = H - TM
    for i in range(1, LINES + 1):
        y = y0 - (i - 1) * LEAD
        c.drawRightString(LM - 0.25 * inch, y - 3, str(i))
    c.setLineWidth(0.8)
    c.line(LM - 0.12 * inch, H - 0.5 * inch, LM - 0.12 * inch, 0.5 * inch)
    c.line(LM - 0.08 * inch, H - 0.5 * inch, LM - 0.08 * inch, 0.5 * inch)
    c.line(W - RM + 0.08 * inch, H - 0.5 * inch, W - RM + 0.08 * inch, 0.5 * inch)
    # footer
    c.setFont("Times-Roman", 8)
    c.line(LM, 0.66 * inch, W - RM, 0.66 * inch)
    foot = state["footer"]
    while pdfmetrics.stringWidth(foot, "Times-Roman", 8) > TEXT_W - 0.6 * inch and len(foot) > 10:
        foot = foot[:-1]
    c.drawString(LM, 0.54 * inch, foot)
    c.drawRightString(W - RM, 0.54 * inch, f"- {state['page']} -")
    c.drawString(LM, 0.40 * inch, "Confidential in part, CRC 1.100(c)(4)  |  Gillson v. Landrum, Torres & Zanghi (Solano)")


def new_page():
    if state["page"] > 0:
        c.showPage()
    state["page"] += 1
    state["line"] = 0
    pleading_frame()


def y_for(line):
    return H - TM - line * LEAD


def ensure(n=1):
    if state["line"] + n > LINES:
        new_page()


def put(text, font=FONT, size=FS, x=None, align="left", bold=False):
    ensure(1)
    y = y_for(state["line"])
    xx = LM if x is None else x
    f = BOLD if bold else font
    # shrink any single line that would cross the right rule
    avail = (W - RM) - (xx if align == "left" else LM)
    while size > 8 and pdfmetrics.stringWidth(text, f, size) > avail:
        size -= 0.5
    if pdfmetrics.stringWidth(text, f, size) > avail:
        # still too long at minimum size: wrap onto following lines
        lines = wrap_measured(text, f, size, avail)
        for k, ln in enumerate(lines):
            if k:
                ensure(1)
                y = y_for(state["line"])
            c.setFont(f, size)
            c.drawString(xx, y, ln)
            state["line"] += 1
        return
    c.setFont(f, size)
    if align == "center":
        c.drawCentredString((LM + W - RM) / 2, y, text)
    elif align == "right":
        c.drawRightString(W - RM, y, text)
    else:
        c.drawString(xx, y, text)
    state["line"] += 1


def blank(n=1):
    for _ in range(n):
        ensure(1)
        state["line"] += 1


def para(text, indent=True, font=FONT, size=FS, width=88, bold=False):
    f = BOLD if bold else font
    for ln in wrap_measured(text, f, size, TEXT_W, "      " if indent else "", ""):
        put(ln, font=font, size=size, bold=bold)


def heading(text):
    ensure(2)
    put(text, bold=True)


def numbered(items, start=1, width=84):
    n = start
    for it in items:
        for ln in wrap_measured(it, FONT, FS, TEXT_W, f"      {n}.  ", "            "):
            put(ln)
        n += 1


def caption(doc_title_lines, footer):
    state["footer"] = footer
    new_page()
    # attorney block
    for t in [
        "DR. DONNY GILLSON, ED.D. (Donald Ernest Gillson)",
        "Mailing address: 1030 Girard Road, Unit 301A, San Francisco, CA 94129",
        "Telephone: (408) 384-1376   |   Email: donny@18fu.ai",
        "Petitioner, In Propria Persona",
    ]:
        put(t)
    blank(1)
    put("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, align="center")
    put("COUNTY OF SOLANO", bold=True, align="center")
    blank(1)
    # two-column caption box
    top = y_for(state["line"]) + 14
    left_lines = [
        "DR. DONNY GILLSON, ED.D.,",
        "          Petitioner,",
        "",
        "     v.",
        "",
        "WILLIAM LANDRUM;",
        "FRANCISCO TORRES; and",
        "JOHN P. ZANGHI,",
        "          Respondents.",
    ]
    right_lines = [f"Case No. {CASE_NO}", ""] + doc_title_lines + [
        "",
        "[Cal. Rules of Court, rules 1.100, 3.1200–3.1207,",
        "3.1300(b); Code Civ. Proc., §§ 527.6, 1005(b)]",
        "",
        "Hearing Date: ______________  Time: ________",
        "Dept.: ______   Judicial Officer: ______________",
    ]
    mid = LM + 2.9 * inch
    col_x = mid + 0.15 * inch
    col_w = W - RM - col_x
    # re-wrap the right column by measured width so nothing crosses the right rule
    n_title = len(doc_title_lines)
    wrapped_right, right_bold = [], []
    for i, ln in enumerate(right_lines):
        is_bold = 2 <= i < 2 + n_title
        f = BOLD if is_bold else FONT
        pieces = wrap_measured(ln, f, 11, col_w) if ln.strip() else [""]
        wrapped_right += pieces
        right_bold += [is_bold] * len(pieces)
    right_lines = wrapped_right
    rows = max(len(left_lines), len(right_lines))
    for i in range(rows):
        ensure(1)
        y = y_for(state["line"])
        if i < len(left_lines):
            c.setFont(FONT, FS)
            c.drawString(LM, y, left_lines[i])
        if i < len(right_lines):
            c.setFont(BOLD if right_bold[i] else FONT, 11)
            c.drawString(col_x, y, right_lines[i])
        c.setFont(FONT, FS)
        c.drawString(mid, y, ")")
        state["line"] += 1
    bottom = y_for(state["line"]) + 14
    c.line(LM, bottom, mid, bottom)
    blank(1)


# ---------------------------------------------------------------------------
# DOCUMENT 1: EX PARTE APPLICATION
# ---------------------------------------------------------------------------
caption(
    [
        "EX PARTE APPLICATION FOR ORDER",
        "SHORTENING TIME; REQUEST FOR",
        "DISABILITY ACCOMMODATIONS UNDER",
        "RULE 1.100; MEMORANDUM; DECLARATION",
        "OF DR. DONNY GILLSON; [PROPOSED] ORDER",
    ],
    "EX PARTE APPLICATION FOR OST AND RULE 1.100 ACCOMMODATION REQUEST",
)

put("TO THE COURT, THE CLERK, THE COURT'S ADA COORDINATOR, AND ALL PARTIES:", bold=True)
para(
    "Petitioner Dr. Donny Gillson, Ed.D. (also appearing in court records as Donald Ernest Gillson), "
    "in propria persona, applies ex parte for (1) an order shortening time on the notice and lead-time "
    "requirements that would otherwise apply to the disability-accommodation request set out below, and "
    "(2) a determination of that accommodation request under California Rules of Court, rule 1.100, so that "
    "the granted measures are in place before the first hearing in this civil harassment restraining order "
    "proceeding (Code Civ. Proc., § 527.6) against Respondents William Landrum, Francisco Torres, and John P. Zanghi."
)
para(
    "This application addresses access to the court only. It does not ask the Court to decide any "
    "contested fact concerning the Respondents' conduct, and nothing in it is offered as evidence on the "
    "merits of the petition. The medical information in the supporting declaration is submitted as "
    "confidential accommodation material under rule 1.100(c)(4); Petitioner has not executed a written waiver."
)

heading("I.  RELIEF REQUESTED")
numbered([
    "An order shortening time under rule 3.1300(b) and Code of Civil Procedure section 1005, subdivision (b), "
    "permitting this accommodation request to be heard and determined on the shortened schedule set out in the "
    "proposed order, and waiving the five-court-day lead time of rule 1.100(c)(3) for good cause.",
    "An order granting the accommodations listed in Part III for the first hearing in this matter and for all "
    "further proceedings in this case, or, for any item denied in whole or in part, a written statement of "
    "reasons under rule 1.100(e)(2) and the alternative the Court will provide.",
    "A direction that the Court's ADA Coordinator transmit the written determination to Petitioner by email at "
    "donny@18fu.ai in a searchable electronic format, with the implementation instructions for each granted item.",
    "To the extent the Court determines that any Respondent is a person \u201cinvolved in the accommodation process\u201d "
    "within the meaning of Vesco v. Superior Court (2013) 221 Cal.App.4th 275, an order limiting any disclosure "
    "to the specific item affecting that Respondent and keeping the balance of the medical material confidential.",
])

heading("II.  GOOD CAUSE FOR SHORTENING TIME")
para(
    "Rule 1.100(c)(3) asks that accommodation requests be made at least five court days before the "
    "accommodation is needed, but it expressly allows the Court to waive that requirement. Rule 3.1300(b) "
    "permits the Court to prescribe shorter notice on a showing of good cause. Good cause exists here:"
)
numbered([
    "Restraining-order proceedings under section 527.6 move on a compressed statutory calendar. The hearing "
    "is set within approximately 21 to 25 days of filing, and a temporary order may issue or be considered "
    "without notice. Waiting for the ordinary noticed-motion schedule would place the accommodation decision after "
    "the very hearing at which the accommodations are needed.",
    "Petitioner has recently relocated to Solano County and is presenting these needs to this Court for the "
    "first time. The same functional limitations have already been evaluated and accommodated by the San Francisco "
    "Superior Court in related matters (Case Nos. CUD-26-682107, CCH-26-589086, and CCH-26-589728) through a series of "
    "written rule 1.100 orders issued between July and October 2026. Petitioner is asking this Court to adopt "
    "parallel measures, not to design new ones.",
    "Petitioner is under active VA care. Confirmed appointments on October 22 and 26 (telephone), October 27 "
    "(in person, Martinez VA neuropsychology at 9:00 a.m. and San Francisco VA at 2:00 p.m.), and November 10, 2026 "
    "(in person, San Francisco VA) should be known to the Court before any hearing date is fixed, so that the "
    "calendar does not collide with medical care.",
    "Petitioner is presently under medical orders to rest. On October 30, 2026, Petitioner was treated in the John Muir "
    "Health Concord Emergency Department after a fall and was placed off work through November 3, 2026 (return no earlier "
    "than November 4, 2026), with directed follow-up at Travis Air Force Base (David Grant USAF Medical Center) on or about "
    "November 1, 2026, where an extension of approximately two weeks is anticipated. Any hearing set in that window must "
    "permit remote appearance. (Declaration, Part B, item 4; Exhibit lodged with the ADA Coordinator.)",
    "The accommodations requested are procedural and low-cost. Deciding them early avoids delay on the hearing "
    "day and avoids the need for a continuance later.",
])
para(
    "Notice of this ex parte application is being given to the Respondents as required by rules 3.1203 and "
    "3.1204, limited to the fact, date, time, and place of the application and the relief sought. The "
    "confidential medical declaration is lodged with the ADA Coordinator and is not served on the Respondents "
    "unless the Court orders disclosure under Vesco. (See Declaration, Part C.)"
)

heading("III.  ACCOMMODATIONS REQUESTED (RULE 1.100)")
para(
    "Each item below corresponds to a measure previously granted or implemented in the San Francisco matters. "
    "The prior ruling is noted in brackets so the Court can see what has already been found workable."
)
numbered([
    "Assistive cognitive technology. Permission to use the N.E.W.T. cognitive-prosthetic software on Petitioner's "
    "own device for manual (typed) input during proceedings, with all audio capture and recording disabled; a brief "
    "5-to-10-minute setup window before the matter is called; and short input pauses on request. Petitioner will "
    "announce before using the device and remains responsible for every statement he makes. "
    "[Granted, SF Dept. 501, July 20 and Oct. 14, 2026; SF Dept. 505, Oct. 7, 2026.]",
    "Breaks and pacing. A 15-minute rest break after approximately 45 minutes of uninterrupted proceedings, "
    "brief symptom-related pauses on request without public medical discussion, slower verbal pacing, and repetition "
    "or clarification when Petitioner says he needs it. [Granted, SF Dept. 501, Sept. 8 and Oct. 14, 2026; Dept. 505, Oct. 7, 2026.]",
    "Written communication. Court notices, orders, scheduling and ADA communications sent by email to donny@18fu.ai "
    "in addition to any mailed copy, in searchable PDF or readable electronic text; short, numbered written instructions "
    "where feasible. [Granted, SF Dept. 501, Aug. 14, 2026 (Feng, J.); Dept. 505, Oct. 7, 2026.]",
    "Remote appearance option. Authorization to appear by Zoom or other court video platform for any hearing at which "
    "remote appearance is compatible with the proceeding, with the connection information emailed in advance; and, if "
    "Petitioner appears remotely, reasonable time to operate platform controls because of hand tremor. "
    "[Granted for the Oct. 8, 2026 hearing, SF Dept. 505; remote law-and-motion appearance permitted, SF Dept. 501.]",
    "Preferred name. Oral reference to Petitioner as \u201cDr. Gillson\u201d or \u201cDr. Donny Gillson.\u201d The legal name may remain in "
    "the caption; use of the first name \u201cDonald\u201d aloud is a reported PTSD trigger. [Granted, SF Depts. 501 and 505, Oct. 2026.]",
    "Service animal. Presence of Jaxx, Petitioner's task-trained psychiatric service dog, with floor space at counsel "
    "table and reasonable relief breaks. [Recognized in all SF orders as requiring no separate accommodation.]",
    "Physical separation and court-directed communication. Separate seating in the gallery from the Respondents and "
    "their representatives while waiting; separate tables during the hearing; all in-court communication directed "
    "through the Court, clerk, or bailiff rather than face-to-face; and coordination with the Sheriff for orderly "
    "ingress and egress. This item is especially important in a proceeding whose subject is the Respondents' alleged "
    "conduct toward Petitioner. [Granted, SF Dept. 501, Sept. 8, 2026; Dept. 505, Oct. 7, 2026.]",
    "Assistive listening device. Access to the courtroom's assistive listening system for in-person hearings "
    "(Petitioner has service-connected bilateral hearing loss). [Granted, SF Dept. 501, Aug. 13, 2026; Dept. 505, Oct. 7, 2026.]",
    "Written outline. Permission to read slowly from a written hearing statement or speaking outline. "
    "[No separate accommodation required; permitted in all SF orders.]",
    "Calendar coordination. That the hearing not be set on October 22, 26, or 27, or November 10, 2026, or, if it "
    "must be, that it be set at a time that does not overlap the confirmed VA appointments listed in the declaration.",
    "Confidential handling. That this request, the supporting declaration, and the medical excerpts be kept in the "
    "confidential accommodation file under rule 1.100(c)(4) and not placed in the public case file.",
])

heading("IV.  MEMORANDUM OF POINTS AND AUTHORITIES")
para(
    "Rule 1.100 implements the Americans with Disabilities Act (42 U.S.C. § 12101 et seq.) and Civil Code section 51 "
    "et seq. in the California courts. The rule directs that requests be granted unless the applicant fails to satisfy "
    "the rule, the accommodation would create an undue financial or administrative burden, or it would fundamentally "
    "alter the nature of the service, program, or activity. (Rule 1.100(f).) The Court must respond in writing and, if "
    "it denies any part of a request, must state the reasons. (Rule 1.100(e)(2).)"
)
para(
    "A request for a modest scheduling adjustment or procedural accommodation is evaluated under rule 1.100, not "
    "solely under ordinary continuance standards. (In re Marriage of James M. & Christine J.C. (2008) 158 Cal.App.4th 1261, "
    "1273\u20131274.) Where a requested accommodation would affect an opposing party, that party is entitled to notice and an "
    "opportunity to be heard on that item, but the court controls the scope of disclosure of the applicant's medical "
    "information. (Vesco v. Superior Court, supra, 221 Cal.App.4th at pp. 280\u2013282.) Only items 4, 7, and 10 above touch "
    "the Respondents' participation in any way, and each can be addressed without disclosing the medical declaration."
)
para(
    "The ex parte and shortening-time rules fit this request. Rule 3.1202(c) requires an affirmative factual showing "
    "of irreparable harm, immediate danger, or other statutory basis for relief without full notice; here, the statutory "
    "basis is the compressed section 527.6 timetable combined with rule 1.100(c)(3)'s express waiver authority. "
    "Rule 3.1300(b) authorizes the Court to shorten notice for good cause. The declaration below supplies the facts."
)
para(
    "Petitioner respectfully asks that the Court enter the proposed order, or set this matter for a brief rule 1.100 "
    "determination at the earliest available date on shortened notice."
)
blank(1)
put("Dated: October ___, 2026", x=LM)
put("Respectfully submitted,", x=LM + 3.4 * inch)
blank(1)
put("/s/ Dr. Donny Gillson, Ed.D.", x=LM + 3.4 * inch)
put("DR. DONNY GILLSON, ED.D.", x=LM + 3.4 * inch)
put("Petitioner, In Propria Persona", x=LM + 3.4 * inch)

# ---------------------------------------------------------------------------
# DOCUMENT 2: DECLARATION
# ---------------------------------------------------------------------------
caption(
    [
        "DECLARATION OF DR. DONNY GILLSON, ED.D.",
        "IN SUPPORT OF EX PARTE APPLICATION",
        "FOR ORDER SHORTENING TIME AND",
        "RULE 1.100 ACCOMMODATION REQUEST",
        "(PARTS B AND C CONFIDENTIAL)",
    ],
    "DECLARATION OF DR. DONNY GILLSON – RULE 1.100",
)
put("I, Dr. Donny Gillson, Ed.D., declare:", bold=True)
heading("A.  Identity, notice, and timing (not confidential)")
numbered([
    "I am the Petitioner in this action and appear in propria persona. I have personal knowledge of the facts stated "
    "here and could testify to them.",
    "I am a 90% service-connected disabled U.S. Navy veteran. I have relocated to Solano County and now receive portions "
    "of my medical care through VA facilities in this region, including the Martinez VA Medical Center.",
    "I filed, or am concurrently filing, a petition for a civil harassment restraining order under Code of Civil "
    "Procedure section 527.6 against William Landrum, Francisco Torres, and John P. Zanghi. Because section 527.6 hearings "
    "are set roughly three weeks from filing, there is not time to bring this accommodation request on the ordinary "
    "noticed-motion schedule.",
    "On the date of this declaration, I gave notice of this ex parte application to each Respondent, or to counsel "
    "where counsel has appeared, stating the date, time, and location of the application and the relief sought. I did "
    "not serve the confidential medical portions of this declaration on any Respondent. The details of the notice given "
    "are set out in Part C. If the Court finds that notice could not be given, I ask the Court to so find under rule 3.1204(b).",
    "The San Francisco Superior Court has issued written rule 1.100 orders addressing the same functional limitations "
    "in Case Nos. CUD-26-682107 (Dept. 501, Hon. Charles F. Haines; Hon. Samuel F. Feng), CCH-26-589086, and CCH-26-589728 "
    "(Dept. 505, Hon. Phoebe H. Maffei). Those orders are dated July 20, August 6, 13, 14, 27, and 31, September 8, 10, "
    "17, and 24, and October 7 and 14, 2026. I can lodge copies with the ADA Coordinator on request. Mr. Zanghi is counsel "
    "of record for the plaintiff in CUD-26-682107 and was served with the October 14, 2026 order in that matter.",
    "My confirmed VA appointments are: October 22, 2026, 3:00 p.m. (telephone); October 26, 2026, 2:00 p.m. (telephone); "
    "October 27, 2026, 9:00 a.m. in person at Martinez VA (neuropsychology, Building 22) and 2:00 p.m. in person at San "
    "Francisco VA Medical Center; and November 10, 2026, 2:00 p.m. in person at San Francisco VA Medical Center.",
])

heading("B.  Functional limitations (CONFIDENTIAL – rule 1.100(c)(4))")
numbered([
    "My VA records document complex PTSD, traumatic brain injury, bipolar I disorder, ADHD, and a chronic tremor "
    "disorder evaluated as Parkinsonism versus essential tremor, together with service-connected bilateral hearing loss. "
    "I take prescribed medication for these conditions.",
    "On September 17, 2026, I was seen in the Palo Alto VA Emergency Department for worsening chronic tremors and hand "
    "and foot cramping following a medication interruption. On September 29, 2026, a VA urgent-care clinician recorded "
    "tremors \u201cabove baseline\u201d attributed to stress, worst in my right upper extremity, and ordered an updated EMG.",
    "The August 6, 2026 VA psychiatry note records memory concerns, defers cognitive screening, and recommends "
    "consideration of formal neuropsychological testing. That testing is scheduled for October 27, 2026. Results are pending.",
    "On October 30, 2026, I fell and was treated in the John Muir Health Concord Emergency Department (Haley Vertelney, M.D.). "
    "CT scans of my head and cervical spine were performed; the diagnosis was acute strain of the neck muscles. Dr. Vertelney "
    "placed me off work through November 3, 2026, stating that I may return to work on November 4, 2026, which she explained is "
    "the maximum period an emergency physician can write. She directed me to follow up at Travis Air Force Base (David Grant "
    "USAF Medical Center, 707-424-1110) on or about November 1, 2026, and advised that any further period of rest would be "
    "ordered there. I anticipate an extension of approximately two weeks. A true copy of the After Visit Summary and work-status "
    "note is lodged with the ADA Coordinator as a confidential exhibit to this declaration and is not served on the Respondents.",
    "In practical terms: under courtroom stress my concentration, recall, and ability to sequence information degrade; "
    "I process spoken instructions less reliably than written ones; sustained participation beyond about 45 minutes "
    "produces fatigue and tremor; hand tremor slows typing, handwriting, and operation of screen controls; and hearing "
    "loss makes overlapping speech difficult to follow. Confrontational proximity, interruption, and perceived ridicule "
    "are specific PTSD triggers.",
    "I use N.E.W.T., a software tool on my own device, as a cognitive prosthetic to organize information and pace tasks. "
    "The August 2026 psychiatry note records my reported use of this software. I use it by typing; I do not record "
    "proceedings with it.",
    "Jaxx is my task-trained psychiatric service dog. He accompanies me to medical appointments and has accompanied me "
    "to every court appearance in the San Francisco matters without incident.",
    "Each accommodation listed in Part III of the application addresses one of the limitations above. None asks the "
    "Court to alter the substance of the proceeding, and each has been implemented in San Francisco without reported burden.",
])

heading("C.  Notice of ex parte application (rule 3.1204(b))")
para("I gave notice as follows (complete before filing):", indent=False)
for ln in [
    "     William Landrum:   Date/time: ______________  Method: ______________  Response: ______________",
    "     Francisco Torres:  Date/time: ______________  Method: ______________  Response: ______________",
    "     John P. Zanghi:    Date/time: ______________  Method: ______________  Response: ______________",
    "     (Mr. Zanghi: Zanghi Torres Adams LLP, jzanghi@ztalaw.com, if notice by email is used.)",
]:
    put(ln, size=11)
para(
    "I told each person that I would appear ex parte at the Superior Court of California, County of Solano, on the "
    "date and time stated on the caption page, to request an order shortening time on a disability-accommodation request "
    "under rule 1.100, and that the accommodation items affecting them are seating separation, court-directed "
    "communication, and the remote-appearance option. I did not disclose the medical content of this declaration."
)
blank(1)
para(
    "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct.",
    indent=False,
)
put("Executed on October ___, 2026, at ______________________, Solano County, California.")
blank(1)
put("/s/ Dr. Donny Gillson, Ed.D.", x=LM + 3.4 * inch)
put("DR. DONNY GILLSON, ED.D.", x=LM + 3.4 * inch)

# ---------------------------------------------------------------------------
# DOCUMENT 3: PROPOSED ORDER
# ---------------------------------------------------------------------------
caption(
    [
        "[PROPOSED] ORDER SHORTENING TIME",
        "AND ORDER RE: RULE 1.100",
        "DISABILITY ACCOMMODATION REQUEST",
        "(CONFIDENTIAL)",
    ],
    "[PROPOSED] ORDER SHORTENING TIME AND RULE 1.100 ORDER",
)
para(
    "The ex parte application of Petitioner Dr. Donny Gillson, Ed.D. for an order shortening time and for "
    "disability accommodations under California Rules of Court, rule 1.100, came before the Court. Having considered "
    "the application, the confidential declaration lodged with the ADA Coordinator, and the notice given, and good "
    "cause appearing, THE COURT ORDERS:"
)
numbered([
    "The five-court-day lead time of rule 1.100(c)(3) is waived. Time is shortened under rule 3.1300(b) so that the "
    "accommodation request is determined by this order, or, if the box below is checked, at a hearing on "
    "_______________, 2026, at ________ a.m./p.m. in Department ______. Any written response by a Respondent limited "
    "to items 4, 7, and 10 shall be filed and served by _______________, 2026.",
    "Petitioner may use the N.E.W.T. software on his own device for manual input only, with all audio capture and "
    "recording disabled, and shall announce before using it. Petitioner may have up to ten minutes to set up before "
    "the matter is called. No recording of proceedings is permitted.",
    "If any session exceeds 45 uninterrupted minutes, the Court will take a 15-minute recess. Petitioner shall notify "
    "the Court when he requires an additional pause, repetition, or clarification.",
    "The Clerk and ADA Coordinator shall send all court-generated notices, orders, and accommodation communications "
    "in this case to donny@18fu.ai, in addition to any mailed copy, in the electronic format in which they are available.",
    "Petitioner may appear by the Court's video platform for:  \u2610 all hearings   \u2610 law-and-motion hearings only   "
    "\u2610 the hearing on _______________. Connection information shall be emailed to Petitioner at least two court days "
    "before the hearing.",
    "Petitioner shall be addressed on the record as \u201cDr. Gillson.\u201d The legal name shall remain in the caption.",
    "Petitioner's service dog, Jaxx, may accompany him in the courtroom.",
    "While waiting for the matter to be called, Petitioner and the Respondents (and their representatives) shall sit "
    "in separate sections of the gallery as directed by the bailiff. During the hearing the parties shall remain at "
    "separate tables. All communications shall be directed to the Court; the parties shall not address one another "
    "except through examination conducted under the Court's control.",
    "The courtroom assistive listening system shall be made available to Petitioner on request to the clerk.",
    "Petitioner may read from a written hearing statement or outline and shall read slowly enough for all participants to follow.",
    "The hearing on the petition shall not be set on October 22, 26, or 27, or November 10, 2026, without first "
    "confirming that the time does not conflict with Petitioner's scheduled VA appointments.",
    "The application, the declaration lodged with the ADA Coordinator, and all medical excerpts shall be maintained "
    "in the confidential accommodation file under rule 1.100(c)(4) and shall not be placed in the public case file. "
    "Disclosure to any Respondent is limited to the portions of this order and the application that describe items "
    "5, 8, and 11 of this order.",
    "The following items are DENIED in whole or in part for the reasons stated: ________________________________________ "
    "______________________________________________________________. Instead the Court will provide: ___________________ "
    "______________________________________________________________.",
    "This order applies to  \u2610 the hearing on _______________ only   \u2610 all proceedings in this case until further order.",
])
blank(1)
put("IT IS SO ORDERED.", bold=True)
blank(1)
put("Dated: _______________, 2026", x=LM)
blank(1)
put("______________________________________", x=LM + 3.0 * inch)
put("Judge / Commissioner of the Superior Court", x=LM + 3.0 * inch)
put("County of Solano", x=LM + 3.0 * inch)

# ---------------------------------------------------------------------------
# DOCUMENT 4: FILING AND ROUTING NOTE (plain page, not a pleading)
# ---------------------------------------------------------------------------
caption(
    ["ROUTING AND FILING NOTE", "(NOT A COURT FORM – FOR THE", "ADA COORDINATOR AND CLERK)"],
    "ROUTING NOTE – RULE 1.100 ACCOMMODATION PACKET",
)
para("This packet contains:", indent=False)
numbered([
    "Ex Parte Application for Order Shortening Time and Rule 1.100 Accommodation Request, with Memorandum (public, "
    "except that the medical information is incorporated only by reference to the confidential declaration).",
    "Declaration of Dr. Donny Gillson. Part A is public. Parts B and C are confidential accommodation material under "
    "rule 1.100(c)(4) and should be lodged with the ADA Coordinator, not filed in the public case file.",
    "[Proposed] Order Shortening Time and Rule 1.100 Order.",
    "Judicial Council form MC-410 (Disability Accommodation Request), completed to match Part III of the application. "
    "The MC-410 should be delivered to the ADA Coordinator with this packet. If the Court prefers the MC-410 as the "
    "operative request, items 1 through 11 of Part III are the items 3 and 4 content for that form.",
    "Attachment to Form MC-410: Request for Cross-County Coordination (San Francisco and Solano Counties) among the "
    "two courts' ADA Coordinators, both counties' Adult Protective Services agencies, and Insight Housing, with a "
    "limited authorization for the exchange of accommodation and safety-planning information. Confidential under "
    "rule 1.100(c)(4) except for the contact roster.",
])
para(
    "Delivery: the public documents (items 1, 2 Part A, and 3) are filed with the Civil Clerk, Superior Court of "
    "California, County of Solano, Hall of Justice, 600 Union Avenue, Fairfield, CA 94533, with the section 527.6 "
    "petition. Item 2 Parts B and C and items 4 and 5 are delivered to the Court's ADA Coordinator at the same address. "
    "Please confirm the correct department and the ADA Coordinator's direct email before filing; Petitioner asks the "
    "clerk to note the department on the caption page.",
    indent=False,
)
para(
    "Notice to Respondents: the ex parte notice given under rule 3.1204 is limited to the date, time, place, and "
    "relief sought. No medical material is served on any Respondent unless the Court orders disclosure under "
    "Vesco v. Superior Court (2013) 221 Cal.App.4th 275.",
    indent=False,
)
para(
    "Petitioner contact for accommodation communications: donny@18fu.ai; (408) 384-1376. Written communication is "
    "preferred.",
    indent=False,
)

# ---------------------------------------------------------------------------
# DOCUMENT 5: ATTACHMENT TO FORM MC-410 - CROSS-COUNTY COORDINATION
# ---------------------------------------------------------------------------
caption(
    [
        "ATTACHMENT TO FORM MC-410 (ITEMS 3 AND 4):",
        "REQUEST FOR CROSS-COUNTY COORDINATION",
        "AMONG THE SAN FRANCISCO AND SOLANO",
        "SUPERIOR COURTS, ADULT PROTECTIVE",
        "SERVICES, AND INSIGHT HOUSING",
        "(CONFIDENTIAL IN PART)",
    ],
    "MC-410 ATTACHMENT – CROSS-COUNTY COORDINATION (SF / SOLANO)",
)
put("TO THE ADA COORDINATOR, SUPERIOR COURT OF CALIFORNIA, COUNTY OF SOLANO:", bold=True)
para(
    "This attachment continues item 3 (accommodation requested) and item 4 (impairment and need) of Judicial Council "
    "form MC-410 submitted by Petitioner Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson). It asks the Court, through its "
    "ADA Coordinator, to coordinate the accommodations granted in this case with the agencies and persons who are already "
    "involved in Petitioner's accommodation, protection, and housing in San Francisco County and in Solano County, so that "
    "Petitioner is not required to re-establish the same accommodations, re-explain the same disability, or re-open the same "
    "safety planning in each county separately."
)
para(
    "The request is made under California Rules of Court, rule 1.100(a)(3) and (e), which charge the ADA Coordinator with "
    "receiving and determining accommodation requests and permit the Court to consult with the applicant and others on the "
    "most workable accommodation; under the Americans with Disabilities Act, title II (42 U.S.C. § 12131 et seq.; 28 C.F.R. "
    "§ 35.130(b)(7)); and under the Elder Abuse and Dependent Adult Civil Protection Act (Welf. & Inst. Code, § 15600 et seq.), "
    "which contemplates coordination among adult protective services agencies and the courts for a dependent adult."
)

heading("I.  PERSONS AND AGENCIES WITH WHOM COORDINATION IS REQUESTED")
numbered([
    "C. Joy Guandique, ADA Coordinator, Superior Court of California, County of San Francisco, Civic Center Courthouse, "
    "400 McAllister Street, San Francisco, CA 94102. Ms. Guandique's office administered the rule 1.100 determinations in "
    "Case Nos. CUD-26-682107 (Dept. 501), CCH-26-589086, and CCH-26-589728 (Dept. 505) listed in Part A of the Declaration.",
    "Adult Protective Services, City and County of San Francisco, Department of Disability and Aging Services, "
    "P.O. Box 7988, San Francisco, CA 94120-7988. Petitioner's APS case was closed by letter dated December 5, 2025 and has "
    "since been reopened; the assigned protective service workers are Jeffrey Tims and Regina Gibson.",
    "Adult Protective Services, County of Solano, Department of Health and Social Services, Fairfield, California. "
    "Petitioner now resides in Solano County and asks that the Solano APS program be made aware of the open San Francisco "
    "case and of the hearing dates in this matter so that any Solano intake, welfare check, or safety plan is coordinated "
    "with San Francisco rather than duplicated.",
    "Insight Housing (formerly Berkeley Food & Housing Project), veteran housing and supportive-services provider, as to its "
    "programs serving San Francisco County and Solano County. Petitioner has sought or is receiving housing assistance through "
    "Insight Housing following his displacement from 1030 Girard Road, San Francisco, and asks that the housing provider be "
    "included in scheduling and safety coordination so that court dates, housing appointments, and VA care do not conflict.",
    "ADA Coordinator, Superior Court of California, County of Solano, Hall of Justice, 600 Union Avenue, Fairfield, CA 94533, "
    "as the receiving and coordinating office for this request.",
])

heading("II.  COORDINATION MEASURES REQUESTED")
numbered([
    "Recognition of the San Francisco determinations. That the Solano ADA Coordinator request from Ms. Guandique copies of "
    "the written rule 1.100 determinations issued in the San Francisco matters between July 20 and October 14, 2026, and that "
    "this Court treat those determinations as the starting point for the accommodations listed in Part III of the application, "
    "so that the same measures are implemented in both counties without a new showing in each.",
    "Single accommodation file. That the two courts' ADA Coordinators maintain a shared, confidential accommodation record "
    "for Petitioner under rule 1.100(c)(4), limited to the accommodation determinations and implementation instructions, so "
    "that a change in one county (for example, a newly granted remote-appearance order) is known to the other.",
    "Adult Protective Services notice and attendance. That the Clerk or ADA Coordinator notify San Francisco APS "
    "(Mr. Tims / Ms. Gibson) and Solano APS of each hearing date and any temporary order in this case; that an APS worker "
    "from either county be permitted to attend hearings and to sit with Petitioner as a support person; and that the Court "
    "receive, through the ADA Coordinator, any APS safety-plan information that bears on courtroom separation, ingress and "
    "egress, or remote appearance (Part III, items 4 and 7).",
    "Housing-provider coordination. That Insight Housing be identified to the Court as Petitioner's housing-services contact "
    "in both counties; that hearing notices and scheduling communications be copied to the Insight Housing case manager "
    "designated below so that housing placements, intake appointments, and transportation can be arranged around court dates; "
    "and that the Court consider, under rule 1.100, that Petitioner's present domicile is a vessel at 2000 Glen Cove Marina, "
    "Vallejo, without reliable heat, water, or mail delivery, when fixing hearing times and service methods.",
    "Calendar coordination across counties. That the Solano ADA Coordinator and Ms. Guandique exchange hearing dates in "
    "CUD-26-682107, CCH-26-589086, CCH-26-589728, and this matter, and the VA appointment dates listed in Declaration Part A, "
    "so that Petitioner is not set to appear in two courthouses, or in court and at a VA facility, on the same day.",
    "Single point of contact. That each agency designate one named contact for Petitioner's matter, listed in the roster in "
    "Part IV, and that all coordination communications to Petitioner be in writing by email to donny@18fu.ai, consistent with "
    "the written-communication accommodation already granted.",
    "Scope limitation. Coordination under this attachment is limited to accommodation, scheduling, safety-planning, and "
    "housing-logistics information. Nothing in this attachment authorizes release of Petitioner's medical records, VA "
    "treatment notes, or the confidential portions of the Declaration to any Respondent or to any person not listed in Part I.",
])

heading("III.  LIMITED AUTHORIZATION FOR EXCHANGE OF ACCOMMODATION INFORMATION")
para(
    "I, Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson), date of birth ______________, authorize the ADA Coordinators of "
    "the Superior Courts of California for the Counties of San Francisco and Solano, Adult Protective Services of the City "
    "and County of San Francisco, Adult Protective Services of the County of Solano, and Insight Housing to exchange among "
    "themselves the following information about me for the purpose of coordinating court accommodations, hearing schedules, "
    "and safety planning: (a) the fact and content of court accommodation determinations under rule 1.100; (b) hearing dates, "
    "times, departments, and remote-appearance information; (c) the identity and contact information of my assigned APS "
    "workers and housing case manager; and (d) my current mailing and email contact information."
)
para(
    "This authorization does not extend to medical or psychological records, VA treatment records, or the confidential "
    "portions of my rule 1.100 declaration, which may be disclosed only by a separate written release or court order. "
    "It expires one year from the date signed or on written revocation, whichever is first. A copy is as valid as the original.",
    indent=False,
)
blank(1)
put("Dated: October ___, 2026", x=LM)
put("/s/ Dr. Donny Gillson, Ed.D.", x=LM + 3.4 * inch)
put("DR. DONNY GILLSON, ED.D., Petitioner", x=LM + 3.4 * inch)

heading("IV.  COORDINATION ROSTER (COMPLETE BEFORE DELIVERY)")
para("Petitioner asks each office to confirm or correct its entry and return the roster by email to donny@18fu.ai.", indent=False)
for ln in [
    "Office / Agency                              Named contact       Telephone        Email",
    "-------------------------------------------  ------------------  ---------------  -------------------",
    "SF Superior Court - ADA Coordinator          C. Joy Guandique    _______________  ___________________",
    "Solano Superior Court - ADA Coordinator      __________________  _______________  ___________________",
    "SF Adult Protective Services (DAS)           Jeffrey Tims        _______________  ___________________",
    "SF Adult Protective Services (DAS)           Regina Gibson       _______________  ___________________",
    "Solano County Adult Protective Services      __________________  _______________  ___________________",
    "Insight Housing - San Francisco program      __________________  _______________  ___________________",
    "Insight Housing - Solano County program      __________________  _______________  ___________________",
    "Petitioner                                   Dr. Donny Gillson   (408) 384-1376   donny@18fu.ai",
]:
    put(ln, font="Courier", size=7.6)
blank(1)
para(
    "Petitioner asks that the Solano ADA Coordinator (1) acknowledge receipt of this attachment in writing, (2) initiate "
    "contact with Ms. Guandique and with both APS offices within five court days, and (3) report the coordination status "
    "to Petitioner by email, so that any gap can be raised with the Court before the first hearing.",
    indent=False,
)
blank(1)
put("Dated: October ___, 2026", x=LM)
put("Respectfully submitted,", x=LM + 3.4 * inch)
blank(1)
put("/s/ Dr. Donny Gillson, Ed.D.", x=LM + 3.4 * inch)
put("DR. DONNY GILLSON, ED.D.", x=LM + 3.4 * inch)
put("Petitioner, In Propria Persona", x=LM + 3.4 * inch)

c.save()
print("wrote", OUT, "pages:", state["page"])
