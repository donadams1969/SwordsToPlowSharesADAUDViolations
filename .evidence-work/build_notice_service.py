"""
NOTICE OF PLAINTIFF'S FAILURE TO SERVE STATEMENT OF THE CASE AND PRETRIAL TRIAL MATERIALS
Dated November 1, 2026. Opening paper (Tab A) in the San Francisco binder.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP, COURT, DEPT

nbody = ParagraphStyle("svbody", parent=body, fontSize=12.5, leading=18, spaceAfter=8)
nh2 = ParagraphStyle("svh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6)

TITLE = ("NOTICE OF PLAINTIFF'S FAILURE TO SERVE STATEMENT OF THE CASE AND PRETRIAL TRIAL MATERIALS;<br/>"
         "OBJECTION AND PRESERVATION OF RIGHTS (CODE CIV. PROC. \u00a7\u00a7 1010, 1013, 2024.020; CAL. RULES OF COURT, RULES 3.1548, 3.1550)")


def build(path):
    f = caption(TITLE)
    f.append(P(f"TO THE PRESIDING JUDGE (HON. STEPHEN M. MURPHY), {DEPT}, {COURT}, ALL PARTIES, AND COUNSEL OF RECORD:", nbody))
    f.append(P("PLEASE TAKE FURTHER NOTICE that defendant Dr. Donny Gillson, Ed.D., appearing in pro per, submits this notice and objection regarding "
               "plaintiff's continuing procedural default and failure of service.", nbody))
    f.append(P("I. Complete Absence of Service by Plaintiff", nh2))
    f.append(P("1. <b>Withholding of mandatory trial materials.</b> As of the date of this notice plaintiff and its counsel have not served, conveyed, or provided "
               "defendant with any statement of the case, witness list, exhibit list or index, trial brief, or other pretrial disclosure required by the Code of "
               "Civil Procedure, the California Rules of Court, and the local rules and standing orders of this Court governing trial-readiness in unlawful "
               "detainer matters, in advance of the trial call set for November 2, 2026, 9:00 a.m., in Department 606. Defendant, by contrast, served his "
               "witness list, exhibit list, statement of the case, and evidentiary designations on counsel on October 29\u201331, 2026 (Tab I; Evidence Exhibit "
               "Binder, Category J).", nbody))
    f.append(P("2. <b>Violation of statutory and due-process requirements.</b> A party prosecuting an unlawful detainer must serve every paper it intends to rely "
               "on at trial on the opposing party (Code Civ. Proc., \u00a7\u00a7 1010, 1013), and the Court's trial-readiness requirements apply equally to a plaintiff "
               "and to an accommodated in pro per defendant. Plaintiff's failure deprives defendant of fair notice of the claims, witnesses, and documents he "
               "must meet; prejudices his ability to prepare a defense within the summary timeline plaintiff itself invoked; and defeats the purpose of the "
               "rule 1.100 accommodations already ordered (Tab K), which presuppose that defendant receives the materials he is to review in writing and in advance.", nbody))
    f.append(P("II. Preservation of Objections and Request for Relief", nh2))
    f.append(P("3. Defendant preserves every objection arising from this failure of service, including objection to any witness, exhibit, or statement of the "
               "case that plaintiff has not disclosed before the trial call. Proceeding to trial call, or attempting to introduce evidence, while withholding "
               "mandatory pretrial disclosures from an accommodated in pro per litigant is unfair surprise and bad faith within the meaning of Code of Civil "
               "Procedure section 128.5 and an independent ground for continuance or dismissal.", nbody))
    f.append(P("4. Defendant requests that the Court: (a) order plaintiff to serve its statement of the case, witness list, exhibit list, and trial brief forthwith "
               "and lodge proof of service; (b) exclude at trial any witness or exhibit not so disclosed (Evid. Code, \u00a7 352; Code Civ. Proc., \u00a7 2023.030, subd. (c)); "
               "(c) continue the trial call under rule 1.100 and Code of Civil Procedure section 1170.5, subdivision (c), for a period sufficient for defendant to "
               "review plaintiff's disclosures with the accommodations ordered; and (d) award sanctions under section 128.5 in an amount to be shown at hearing.", nbody))
    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Notice of Plaintiff's Failure to Serve Pretrial Materials")


if __name__ == "__main__":
    out = os.path.join(TMP, "notice_failure_to_serve.pdf")
    build(out); print(out)
