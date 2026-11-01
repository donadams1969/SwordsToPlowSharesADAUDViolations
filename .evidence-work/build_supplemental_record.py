"""
SUPPLEMENTAL TRIAL MANAGEMENT RECORD AND EVIDENTIARY STATUS - dated November 1, 2026.
Companion to the Lead Memorandum (Tab A) and Lead Opening Statement.
Statements the record cannot yet prove (subpoena service, who visited a web page, page counts) are framed as
contentions or as items to be confirmed, not as established fact.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP

sbody = ParagraphStyle("srbody", parent=body, fontSize=12, leading=16.5, spaceAfter=7)
sh2 = ParagraphStyle("srh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6, textTransform="uppercase", keepWithNext=1)
sbul = ParagraphStyle("srbul", parent=sbody, leftIndent=26, firstLineIndent=-14, spaceAfter=5)

TITLE = ("SUPPLEMENTAL TRIAL MANAGEMENT RECORD AND EVIDENTIARY STATUS: SUBPOENAED WITNESSES, "
         "PROTECTED REMOTE TESTIMONY, ESI PRESERVATION, AND TRIAL-CALL READINESS<br/>"
         "[Related Matters: CCH-26-589086 | CCH-26-589728]")


def bullets(f, items):
    for t in items:
        f.append(P("\u2022&nbsp;&nbsp;" + t, sbul))


def build(path):
    f = caption(TITLE)
    f.append(P("<b>Presiding:</b> Hon. Stephen M. Murphy, Department 606. <b>Trial call:</b> November 2, 2026, 9:00 a.m. "
               "<b>Date of this record:</b> November 1, 2026. <b>Defendant in pro per:</b> Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson). "
               "<b>Accommodated channel:</b> donny@18fu.ai | (408) 384-1376 (Cal. Rules of Court, rule 1.100).", sbody))

    f.append(P("I. Witnesses and Protected Remote Testimony", sh2))
    f.append(P("Defendant gives the Court notice of the following witnesses for trial: <b>Calvin Whitaker</b>, <b>David Wellingford</b>, and other current or former "
               "Swords to Plowshares employees and witnesses identified in Defendant's witness list and subpoena filings. Defendant expects their testimony to address "
               "habitability conditions, the handling of his accommodation requests and complaints, and the events leading to the nuisance notice, at 1029 and 1030 Girard Road.", sbody))
    bullets(f, [
        "<b>Subpoena status.</b> Defendant has requested subpoenas through the court's process and is arranging service through his process server. "
        "Proof of service for each witness will be lodged with the Court. Where service on a given witness is not complete by the time of the call, Defendant will say so on the record and ask for "
        "the Court's direction rather than represent that the witness is bound to appear.",
        "<b>Remote testimony.</b> To the extent a witness is unable to appear in person, or fears retaliation for testifying, Defendant requests that the Court permit testimony by "
        "video, and requests that any in camera or protective arrangement be set by the Court after hearing from the witness and Plaintiff. Defendant does not ask the Court to receive "
        "unsworn accounts: he asks that testimony be sworn and subject to cross-examination.",
        "<b>Other evidence.</b> Defendant will separately offer the signed declarations and recorded statements of resident members of the Veterans Tenant Union, "
        "subject to the Court's rulings on foundation, hearsay, and authentication.",
    ])
    f.append(P("Defendant contends that any retaliation or threat of retaliation against a witness for testifying is relevant to bad-faith displacement and to the credibility of the retaliation defense "
               "(Civ. Code, \u00a7 1942.5). He will offer evidence of it if it occurs and does not ask the Court to assume it.", sbody))

    f.append(P("II. Digital Repository and ESI Preservation", sh2))
    f.append(P("Defendant maintains an online repository of his evidentiary materials at calindex.vercel.app. Links to it were included in filings and correspondence served on Plaintiff's counsel and "
               "others. The site's analytics, as Defendant reads them, show access from both mobile and desktop devices, with roughly 14 percent of recorded visits from Windows/desktop systems.", sbody))
    bullets(f, [
        "<b>What the telemetry shows.</b> It shows that the links were opened from desktop as well as mobile devices. Defendant does not contend that the analytics, by themselves, identify "
        "who visited. Desktop visits could come from any person or entity that received a link, and from Defendant's own devices.",
        "<b>Why it is offered.</b> Defendant offers it only as circumstantial context: the links were distributed to counsel and related parties, and some access followed distribution. "
        "If Plaintiff or its counsel dispute having reviewed the materials, Defendant asks only that they say so on the record. He does not ask the Court to find monitoring on this data alone.",
        "<b>Preservation.</b> The analytics export, access logs, and the repository's version history are preserved in their native form, and Defendant requests that Plaintiff and its counsel likewise "
        "preserve any records of their receipt and review of the transmitted links and materials. Defendant will provide the export to the Court and the parties on request.",
    ])

    f.append(P("III. Trial-Call Readiness (November 2, 2026, 9:00 a.m.)", sh2))
    f.append(P("Defendant is prepared to proceed with the following, subject to the accommodations ordered under rule 1.100:", sbody))
    for n, t in enumerate([
        "<b>The trial binder set.</b> The binders lodged with the Court organize the exhibits, motions, and records on which Defendant relies, including the habitability evidence "
        "(including the pest infestation at 1030 Girard Road, Room 320), the adult protective services reports, and VA clinical records. Medical and VA records are lodged in the confidential "
        "binder under rule 1.100(c)(4) and are not described in this public filing beyond the fact of their existence.",
        "<b>Emergency filings and accommodation rights.</b> Defendant's emergency filings were made to protect his health and housing and to seek rule 1.100 accommodation. Under "
        "<i>Vesco v. Superior Court</i> (2013) 221 Cal.App.4th 275, requests for disability accommodation are analyzed under rule 1.100, not the ordinary good-cause standard. "
        "Defendant contends that these filings were made in good faith. He recognizes that whether any filing was proper is a matter for the Court to decide, and he asks only that it be "
        "decided on the record and with the findings rule 1.100 requires.",
        "<b>Request for complex or coordinated handling.</b> Defendant contends that this matter, with its related proceedings (CCH-26-589086 and CCH-26-589728), its pending requests for federal "
        "administrative review (the VA Regional Office in Oakland and the VA and HUD Offices of Inspector General), and its funding-records issues, goes beyond a routine summary proceeding. "
        "He asks the Court to consider whether the possession question should be heard together with, or after, those issues, and to hear him on that request at the call.",
    ], 1):
        f.append(P(f"{n}. {t}", sbody))

    f.append(P("IV. Requested Orders", sh2))
    f.append(P("Defendant respectfully requests that Department 606:", sbody))
    for n, t in enumerate([
        "<b>SET</b> a procedure at the trial call for the testimony of the witnesses identified above, including remote appearance and any protective measures the Court finds appropriate;",
        "<b>NOTE</b> the preservation of the analytics and access records described in Part II and direct that Plaintiff and its counsel preserve their own records of receipt and review of the transmitted materials;",
        "<b>RULE</b> on Defendant's rule 1.100 requests, with the findings the rule requires, before proceeding to trial on possession; and",
        "<b>CONSIDER</b> the request for coordinated handling and a stay described in Part III and in the Lead Memorandum.",
    ], 1):
        f.append(P(f"{n}. {t}", sbody))

    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Supplemental Trial Management Record and Evidentiary Status")


if __name__ == "__main__":
    out = os.path.join(TMP, "supplemental_record.pdf")
    build(out); print(out)
