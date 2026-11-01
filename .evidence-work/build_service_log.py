"""Declaration re Electronic Service Log - transmissions of Oct. 29 - Nov. 1, 2026 on the 'Reasonable Accommodation Request' thread."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph as P, Spacer, Table, TableStyle
import build_allinone as A

h2 = A.h2

ROWS = [
    ("Oct. 29, 2026, 4:50-4:52 PM", "F. Torres (ZTA); cc R. Gibson and J. Timms (SF HSA/APS); C. J. Guandique (ADA Coordinator); fwd. to Dept. 606",
     "Re: Reasonable Accommodation Request - Meet and Confer via Email only - Formal Supplemental Notice re Active APS Investigation"),
    ("Oct. 31, 2026", "Department606@sftc.org; counsel of record", "Fw: Swords v. Gillson - Site Inspection (three transmissions)"),
    ("Oct. 31, 2026", "Department606@sftc.org; counsel of record", "Notice of Fraudulent Service, Retaliation, Hearsay Defenses, and Medical Documentation Chronology"),
    ("Oct. 31, 2026", "Department606@sftc.org; counsel of record", "Re: Formal Evidentiary Notice and Trial Exhibit Intent with Descriptors: Exhibits V-01 through V-07 (audio-visual recordings, Google Drive)"),
    ("Oct. 31, 2026", "Department606@sftc.org; counsel of record", "Re: Urgent Emergency Notice of Unauthorized System Probing, Backend Intrusion, and Digital Trespass"),
    ("Oct. 31, 2026", "Department606@sftc.org; ADA Coordinator; counsel of record", "Re: Reasonable Accommodation Request (six transmissions on the thread)"),
    ("Oct. 31, 2026", "Department606@sftc.org", "Official ADA Compliance Grievance, Cal. Rules of Court rule 1.100 Violation Report, and Formal Complaint regarding Judicial and Professional Misconduct"),
    ("Nov. 1, 2026 (a.m.)", "Counsel of record for Swords to Plowshares; Department 606", "Official Legal and Administrative Notice - Notice of Active Federal Investigations and Incorporation into Official Federal Medical Records (VA Blue Button report)"),
    ("Nov. 1, 2026 (a.m.)", "Department 606; counsel of record", "Re: Reasonable Accommodation Request - Objection to Medical Privacy Intrusion; Notice of Lodgment of Medical Records (conditionally under seal)"),
    ("Nov. 1, 2026 (a.m.)", "Department 606; counsel of record", "Re: Reasonable Accommodation Request - Objection to Five-Day Notice and Request for Order Shortening Time / Continuance"),
    ("Nov. 1, 2026, 8:28 AM", "Department 606 and two others (counsel of record; ADA Coordinator) - 2 attachments (analytics screenshots)",
     "Fw: Reasonable Accommodation Request - Supplemental Notice of Active Monitoring, Digital Telemetry, and Evidentiary Logs (calindex.vercel.app)"),
]


def build(path):
    f = A.caption("DECLARATION OF DONALD ERNEST GILLSON RE ELECTRONIC SERVICE LOG (OCTOBER 29 - NOVEMBER 1, 2026); NOTICE THAT ALL "
                  "PRETRIAL NOTICES IN TAB A WERE TRANSMITTED TO DEPARTMENT 606, THE ADA COORDINATOR, AND COUNSEL OF RECORD")
    f.append(P("I, Donald Ernest Gillson, declare:", A.body))
    f.append(P("1. I am the defendant in this action and appear in propria persona. I have personal knowledge of the facts stated here and could testify to them.", A.body))
    f.append(P("2. Between October 29 and November 1, 2026, I transmitted the notices, objections, and applications collected in Tab A of this binder, and the "
               "notices described in Tabs D through G, by e-mail from my account (donny@18fu.ai) to Department 606 (Department606@sftc.org), the Court's ADA "
               "Coordinator (C. Joy Guandique, jguandique@sftc.org), and plaintiff's counsel of record Francisco G. Torres (ftorres@ztalaw.com) at Zanghi Torres "
               "Adams LLP, on the existing e-mail thread titled \"Reasonable Accommodation Request\" on which counsel had previously corresponded with me. "
               "The Sent folder of that account records the following transmissions:", A.body))
    data = [[P("<b>Date / time</b>", A.small), P("<b>Recipients</b>", A.small), P("<b>Subject / instrument</b>", A.small)]]
    for d, r, s in ROWS:
        data.append([P(d, A.small), P(r, A.small), P(s, A.small)])
    t = Table(data, colWidths=[1.25 * inch, 2.2 * inch, 3.05 * inch], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EAF2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    f += [Spacer(1, 6), t, Spacer(1, 8)]
    f.append(P("3. Each transmission was sent from my account and none was returned as undeliverable. Where a message is described as a forward (\"Fw:\"), the "
               "forwarded message is the instrument identified in the subject line and is reproduced in this binder. The two attachments to the 8:28 AM "
               "transmission of November 1, 2026 are the analytics screenshots described in the Supplemental Notice of Active Monitoring (Tab A).", A.body))
    f.append(P("4. Electronic service on counsel is made under Code of Civil Procedure section 1010.6 on the thread counsel has used to correspond with me; "
               "transmission to Department 606 and the ADA Coordinator is made as the Court's designated channel for rule 1.100 communications. Native .eml "
               "copies with full headers are preserved and will be produced on request; the hard-copy set is being delivered by Rapid Legal as stated in the "
               "Notice of Lodgment (Tab A).", A.body))
    f.append(P("I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct. Executed on "
               f"{A.DATED} at Solano County, California.", A.body))
    f += A.signature()
    return A.rl(f, path, "Declaration re Electronic Service Log")


if __name__ == "__main__":
    print(build(os.path.join(A.TMP, "service_log.pdf")))
