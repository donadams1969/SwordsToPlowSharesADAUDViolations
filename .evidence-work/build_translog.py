"""
Transmission log: e-mail service record of defendant's opening papers and notices,
Oct. 29 - Nov. 1, 2026, compiled from the Sent folder of donny@18fu.ai.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from build_allinone import caption, P, h2, rl, signature, body, TMP

ROWS = [
    # (date/time PST, to, cc / forward, attachment, subject line / document transmitted)
    ("Nov. 1, 2026, 8:28 AM", "Department 606 (department606@sftc.org)", "Fw: Reasonable Accommodation Request", "Attachments",
     "Supplemental Notice of Active Monitoring, Digital Telemetry, and Evidentiary Logs (calindex.vercel.app)"),
    ("Nov. 1, 2026, 8:00 AM", "Joy Guandique, ADA Coordinator (jguandique@sftc.org); cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "None",
     "Notice of Lodgment of Digital Case Repository and Intellectual Property Protections; Notice of Hard-Copy Service via Rapid Legal"),
    ("Nov. 1, 2026, 7:54 AM", "Joy Guandique; cc Torres; Dept. 606", "Opening Statement & Application for Reasonable Accommodation and Emergency Vesco Judicial Access", "None",
     "Opening Statement and Application for Reasonable Accommodation (Tab A-1)"),
    ("Nov. 1, 2026, 7:39 AM", "Joy Guandique; cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "None",
     "Notice of Plaintiff's Failure to Serve Mandatory Statement of the Case and Pretrial Materials (Tab A-4)"),
    ("Nov. 1, 2026, 7:15 AM", "Joy Guandique; cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "None",
     "Notice of Legal Objection re Continuing ADA Accommodations (rule 1.100); Challenge to Five-Day Notice Requirement"),
    ("Nov. 1, 2026, 7:09 AM", "Joy Guandique; cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "Attachments",
     "Notice of Lodgment of Medical Evidence: Vesco Medical Stay, Bed Rest through Nov. 4, 2026, Solano County Conflict (Nov. 11, 2026)"),
    ("Nov. 1, 2026, 7:06 AM", "Joy Guandique; cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "None",
     "Notice of Objection and Reservation of Rights re Unauthorized Disclosure or Weaponization of Protected Medical Records"),
    ("Nov. 1, 2026, 7:03 AM", "Solano Superior Court (courthr@solano.courts.ca.gov)", "Fw: Reasonable Accommodation Request", "Attachments",
     "Forward of 7:00 AM notice (below) to Solano County Superior Court"),
    ("Nov. 1, 2026, 7:00 AM", "Joy Guandique; cc Torres; Dept. 606", "Re: Reasonable Accommodation Request", "Attachments",
     "Notice of Active Federal Investigations and Incorporation into VA Blue Button Report (with VA report attached)"),
    ("Oct. 31, 2026", "Francisco G. Torres (ftorres@ztalaw.com)", "Emergency Motion in Limine and Motion to Disqualify Counsel (rule 3.7; rule 1.100; CCP \u00a7 2023.030)", "None",
     "Motion in Limine / disqualification papers transmitted to plaintiff's counsel"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Re: Urgent Emergency Notice of Unauthorized System Probing, Backend Intrusion, and Digital Trespass", "None",
     "Judicial and Forensic Traffic Analytics Correlation Report (telemetry vs. docket timeline)"),
    ("Oct. 31, 2026", "Francisco G. Torres; Dept. 606", "Urgent Emergency Notice of Unauthorized System Probing, Backend Intrusion, and Digital Trespass", "None",
     "Emergency notice and declaration re IP probing and telemetry interception"),
    ("Oct. 31, 2026", "Department 606", "Re: Formal Evidentiary Notice ... Exhibits V-01 through V-07", "None",
     "Formal Notice of Government Tort Claim, Judicial Disqualification, and ADA/Constitutional Safeguards"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Re: Reasonable Accommodation Request", "None",
     "Addendum to Master Trial Record: Malicious Prosecution, Bad-Faith Threats, and Elder/Dependent Adult Protection"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Re: Reasonable Accommodation Request", "None",
     "Notice re Absence of Written ADA Guidance and Communications Protocols, Department-to-Department Shuffling, Pending Complaints"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Re: Reasonable Accommodation Request", "None",
     "Response and Clarification re Oral Directive Concerning Communications; Notice of Pending MC-410 and Administrative Investigations"),
    ("Oct. 31, 2026", "Don Abrahms (ADA/complaint channel)", "Re: Reasonable Accommodation Request Meet and Confer via Email only", "None",
     "Request for Judicial Notice (Evid. Code \u00a7\u00a7 452, 453) of Aug. 27, 2026 order (Haines, J.) and docket; Memorandum"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Notice of Fraudulent Service, Retaliation, Hearsay Defenses, and Medical Documentation Chronology", "None",
     "Notice re three-day-notice defects, third-person misrepresentation, retaliation, medical confinement; Zoom-only appearance"),
    ("Oct. 31, 2026, 11:25 AM", "Francisco G. Torres; cc Dept. 606; fwd. Solano Superior Court", "Re: Swords v Gillson - Site Inspection", "None",
     "Notice of Fraudulent Service, Hearsay Defenses, and Medical Documentation Chronology (signature/timestamp challenge to three-day notice)"),
    ("Oct. 31, 2026", "Francisco G. Torres", "Re: Swords v Gillson - Site Inspection", "None",
     "Chronological deep-dive and statement analysis of the three-day notice correspondence"),
    ("Oct. 29, 2026, 4:50 PM / 4:52 PM", "Francisco G. Torres; cc R. Gibson and J. Timms (HSA/APS); J. Guandique; fwd. Don Abrahms", "Re: Reasonable Accommodation Request Meet and Confer via Email only", "None",
     "Formal Supplemental Notice re Active Adult Protective Services Investigation and Inclusion of APS Workers Gibson and Timms"),
    ("Oct. 29, 2026", "ADA Coordinator / complaint channel", "Official ADA and Judicial Misconduct Complaint", "None",
     "ADA compliance grievance, rule 1.100 violation report, and complaint regarding judicial and professional misconduct"),
]


def build(path):
    f = caption("DEFENDANT'S TRANSMISSION LOG: E-MAIL SERVICE RECORD OF OPENING PAPERS, NOTICES, AND ACCOMMODATION REQUESTS "
                "(OCTOBER 29 \u2013 NOVEMBER 1, 2026); DECLARATION OF SERVICE BY ELECTRONIC MAIL")
    f.append(P("Defendant Donald Ernest Gillson, Ed.D., in pro per, submits this log of the electronic transmissions by which the opening papers in Tab A, "
               "the accommodation requests, and the related notices were served on the Court's ADA Coordinator, Department 606, and plaintiff's counsel of "
               "record, Francisco G. Torres (Zanghi Torres Adams LLP), from the account donny@18fu.ai. Times are Pacific. The native messages, with headers "
               "and attachments, are preserved in the Sent folder and will be produced on request (Evid. Code, \u00a7\u00a7 1400\u20131401, 1552, 1553)."))
    hdr = ["Date / time", "To / cc", "Thread or subject line", "Att.", "Document transmitted"]
    data = [[Paragraph(f"<b>{h}</b>", body) for h in hdr]] + [[Paragraph(c, body) for c in r] for r in ROWS]
    t = Table(data, colWidths=[0.95 * inch, 1.45 * inch, 1.6 * inch, 0.55 * inch, 1.95 * inch], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8EE")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    f += [t, Spacer(1, 10)]
    f.append(P("Declaration of service", h2))
    f.append(P("I, Donald Ernest Gillson, declare: I am the defendant in this action and over the age of 18. On the dates and at the times shown above I "
               "transmitted each listed document by electronic mail from donny@18fu.ai to the addresses shown, which are the e-mail addresses of record for "
               "plaintiff's counsel (ftorres@ztalaw.com), the Court's ADA Coordinator (jguandique@sftc.org), and Department 606 (department606@sftc.org). "
               "No electronic message was returned as undeliverable. Electronic service on counsel is made under Code of Civil Procedure section 1010.6 and "
               "California Rules of Court, rule 2.251; transmissions to the Court were made as rule 1.100 accommodation requests and for lodgment with the "
               "Department. Hard copies of the trial binders are being served through Rapid Legal as stated in the Notice of Lodgment (Tab A-2). I declare under "
               "penalty of perjury under the laws of the State of California that the foregoing is true and correct."))
    f += signature()
    return rl(f, path, "Transmission Log")


if __name__ == "__main__":
    print(build(os.path.join(TMP, "translog.pdf")))
