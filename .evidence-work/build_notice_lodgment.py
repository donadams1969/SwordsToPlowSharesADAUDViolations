"""
NOTICE OF LODGMENT OF DIGITAL CASE REPOSITORY AND INTELLECTUAL PROPERTY PROTECTIONS; NOTICE OF FORTHCOMING HARD-COPY SERVICE
Dated November 1, 2026. Opening paper (Tab A) in the San Francisco binder.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP, COURT, DEPT

nbody = ParagraphStyle("lgbody", parent=body, fontSize=12.5, leading=18, spaceAfter=8)
nh2 = ParagraphStyle("lgh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6)
URL = "https://calindex.vercel.app/"

TITLE = ("NOTICE OF LODGMENT OF DIGITAL CASE REPOSITORY AND INTELLECTUAL PROPERTY PROTECTIONS (CALINDEX.VERCEL.APP);<br/>"
         "NOTICE OF FORTHCOMING HARD-COPY PLEADING SERVICE VIA RAPID LEGAL")


def build(path):
    f = caption(TITLE)
    f.append(P(f"TO THE PRESIDING JUDGE (HON. STEPHEN M. MURPHY), {DEPT}, {COURT}, ALL PARTIES, AND COUNSEL OF RECORD:", nbody))
    f.append(P("PLEASE TAKE NOTICE that defendant Dr. Donny Gillson, Ed.D., appearing in pro per, provides formal notice of the creation, publication, and "
               f"lodging of the official digital case repository and summary website located at <link href='{URL}'><u>{URL}</u></link>, for Case No. "
               "CUD-26-682107 and related matters CCH-26-589086 and CCH-26-589728.", nbody))
    f.append(P("I. Lodgment of Digital Repository and Case Summary", nh2))
    f.append(P(f"1. <b>Comprehensive web-based framework.</b> The repository at <link href='{URL}'><u>{URL}</u></link> hosts the integrated statement of the "
               "case, indexed witness register, comprehensive exhibit manifest, the rule 1.100 accommodation (ADA/prosthetic-access) architecture, and the "
               "fiduciary and jurisdictional protections asserted in this action. Every document in the two trial binders and the Evidence Exhibit Binder "
               "is mirrored there in the same order, with the same tab letters and exhibit numbers, so that the Court and counsel may navigate the record "
               "electronically while the paper binders are the lodged originals.", nbody))
    f.append(P("2. <b>Accessibility and transparency.</b> The digital platform ensures transparent access to the public record, evidentiary exhibits, and "
               "statutory filings in alignment with electronic-accessibility standards (Gov. Code, \u00a7 11135; Cal. Rules of Court, rule 1.100), and is itself "
               "part of the reasonable accommodation requested: it allows defendant to present and retrieve the record without reliance on the oral processing "
               "his medical orders restrict. Nothing in the repository is offered in place of the lodged paper record; where the two differ, the paper binder "
               "controls.", nbody))
    f.append(P("II. Intellectual Property and Proprietary Rights Notice", nh2))
    f.append(P("3. <b>Proprietary architecture and frameworks.</b> The content, structure, design, and code associated with the digital repository and the "
               "underlying frameworks (including the N.E.W.T., VALORAIPLUS, and VALORCHAIN architectures) are proprietary intellectual property of That's "
               "Edutainment LLC, 32D LLC, and Dr. Donny Gillson, Ed.D., protected under copyright, trademark, and trade-secret law (17 U.S.C. \u00a7 101 et seq.; "
               "15 U.S.C. \u00a7 1051 et seq.; Civ. Code, \u00a7 3426 et seq.). Publication of the court record on the repository is not a waiver of those rights in the "
               "platform itself.", nbody))
    f.append(P(f"4. <b>Monitoring for unauthorized use.</b> Notice is given that unauthorized scraping, data harvesting, mirroring, duplication, or misappropriation "
               f"of the intellectual property housed within or linked from <link href='{URL}'><u>{URL}</u></link> will be monitored and pursued as willful "
               "infringement. This paragraph does not restrict the Court, court staff, or counsel of record from accessing, printing, or citing the case "
               "documents published there for purposes of this litigation.", nbody))
    f.append(P("III. Forthcoming Hard-Copy Pleading Service via Rapid Legal", nh2))
    f.append(P("5. <b>Pleading-paper hard copies.</b> In compliance with California Rules of Court, rules 2.100\u20132.119, formal hard copies of the papers in this "
               "binder, formatted on pleading paper, are being finalized.", nbody))
    f.append(P("6. <b>Service through a registered process server.</b> On completion the hard copies will be conveyed and served on Department 606 (Hon. Stephen "
               "M. Murphy), the clerk, and counsel for plaintiff through Rapid Legal, a registered third-party process server, under Code of Civil Procedure "
               "sections 1010\u20131013 and California Rules of Court, rule 2.251, with proofs of service to be filed. Electronic service previously effected on "
               "counsel (Evidence Exhibit Binder, Category J) remains effective and is not superseded by this notice.", nbody))
    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Notice of Lodgment of Digital Case Repository")


if __name__ == "__main__":
    out = os.path.join(TMP, "notice_lodgment.pdf")
    build(out); print(out)
