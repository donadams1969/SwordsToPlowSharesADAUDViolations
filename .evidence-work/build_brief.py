"""
MASTER INTEGRATED STATEMENT OF THE CASE AND TRIAL BRIEF (defendant's final pre-trial paper).
Sits in Tab A immediately after the Notice and before the Integrated Statement. Same 12.5/22.5 pt
typography as the Notice so the opening of the binder reads as one document.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.lib.units import inch
from reportlab.platypus import Spacer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, grid, signature, TMP, COURT, DEPT
from build_notice import body, h2, h3, phase, box

TITLE = ["MASTER INTEGRATED STATEMENT OF THE CASE AND TRIAL BRIEF;",
         "RECORD CROSS-REFERENCE (R01\u2013R10) AND LINE-BY-LINE INDEX OF RECORD IRREGULARITIES;",
         "SUMMARY OF TRIAL EXHIBITS (TABS A\u2013M) AND RELIEF REQUESTED"]

S = "\u00a7"

CONTENT = [
    ("phase", "TRIAL CALL: NOVEMBER 2, 2026, 9:00 A.M., DEPARTMENT 606 (HON. STEPHEN M. MURPHY). RELATED: CCH-26-589086, CCH-26-589728. "
              "STRUCTURE: ANALYZE \u2192 DESIGN \u2192 DEVELOP \u2192 IMPLEMENT \u2192 EVALUATE."),

    ("h2", "I. Executive Summary and Reader's Map"),
    ("n", "Nature of action. Residential unlawful detainer for possession only, arising from a default judgment entered June 30, 2026 ($0.00 monetary relief) and set aside on July 22, 2026 (R08\u2013R10)."),
    ("n", "Core defense position. The action is retaliatory on the face of plaintiff's own notice (Civ. Code " + S + " 1942.5; Gov. Code " + S + " 12955(f)); procedurally void for defective notice and defective service "
          "(Code Civ. Proc. " + S + S + " 1161, 1162, 415.45, 417.10); and prosecuted while plaintiff's management and legal agents suppressed a written disability accommodation "
          "(Cal. Rules of Court, rule 1.100; 42 U.S.C. " + S + " 3604(f)(3)(B)) and used a known traumatic brain injury and PTSD against the defendant."),
    ("n", "Record integrity. Every citation in this brief points to the ten filed court documents (R01\u2013R10, Tab H), the verified administrative complaints (Tabs L and M), "
          "the Court's rule 1.100 responses (Tab K), or a numbered Figure in the Integrated Statement that follows (Tab A). Nothing is cited that is not in the binder."),
    ("table", [["Part", "Contents", "Where the record is"],
               ["II", "Chronological statement of the case, November 2025 to trial", "Tab A Figs. 1\u201314; Tab H"],
               ["III", "Line-by-line index of record irregularities (ten items)", "R01, R02, R05, R10"],
               ["IV", "Summary of trial exhibits by Tab", "Tabs E, H\u2013M"],
               ["V", "Conclusion and relief requested", "\u2014"]],
     [0.6 * inch, 3.9 * inch, 2.0 * inch]),

    ("h2", "II. Chronological Statement of the Case"),
    ("h3", "A. Protected activity and accommodation consensus (November 2025 \u2013 March 2026)"),
    ("n", "November 20, 2025. Defendant submitted a written reasonable-accommodation request asking that communication with management be in writing by email, to accommodate "
          "service-connected TBI, PTSD and cognitive pacing (Tab A Fig. 1)."),
    ("n", "December 23, 2025. Written accommodation consensus between defendant, Joel Champion and property-management agent Kolby Losik confirming the email protocol (Tab A Fig. 2)."),
    ("n", "January 2, 2026. Agent Losik told defendant to \u201cstop with the f\u2014ing emails, or else,\u201d penalizing the accommodated channel itself. Board of Behavioral Sciences "
          "complaints Nos. 2002026002097 and 2002026002098 were initiated against staff (Tab M)."),
    ("n", "January 3, 2026. Confrontation with property manager William Landrum following unaddressed pest infestation (SF 311 Case 101003004371; Tab L)."),
    ("n", "February 25, 2026. Defendant petitioned this Court for an elder/dependent-adult abuse restraining order against the assistant property manager (CCH-26-589086; hearing March 19, 2026)."),
    ("box", "Statutory significance. Under Civil Code " + S + " 1942.5, subd. (a), a notice to quit served within 180 days of a habitability complaint to the landlord or an agency, or of a "
            "tenant's lawful exercise of rights, is presumptively retaliatory; the landlord bears the burden of proving a non-retaliatory purpose. Every event in Part II.A falls inside that window."),

    ("h3", "B. The facially retaliatory April 8, 2026 notice to quit (R01 pp. 33\u201335)"),
    ("n", "Express retaliatory grounds. The three-page notice cites defendant's February 25 restraining-order petition and March 19 court appearance as grounds, and penalizes "
          "\u201cover one thousand (1,000) lengthy emails\u201d \u2014 the written channel agreed in December 2025 (Tab A Figs. 3\u20134)."),
    ("n", "Contradictory exemptions. Page 3 of the notice asserts the tenancy is \u201cexempt from the provisions of the San Francisco Residential Rent Stabilization and Arbitration "
          "Ordinance,\u201d while the complaint (Attachment 18) pleads that the tenancy is subject to just-cause requirements for federally subsidized housing."),
    ("n", "Premature publication. The notice was copied to the San Francisco Housing Authority and HSH before any adjudication."),

    ("h3", "C. The defective complaint and its verification (R01, filed May 5, 2026)"),
    ("n", "Verified by the accused agent. The complaint was verified May 4, 2026 by Jerome Bradford as an \u201cauthorized employee\u201d with personal knowledge. The verification names the "
          "defendant \u201cDonald Gillison,\u201d carries a recycled attorney block for Andrew Wong dated January 19, 2025, and states conflicting rent figures ($1,500/mo. against a $1,126/mo. subsidy breakdown) (Tab A Fig. 5)."),
    ("n", "Missing Exhibit 3. The complaint pleads that proof of service of the notice is attached as Exhibit 3. Pages 36\u201354 contain HUD VAWA forms and the Mayor's Office eviction-prevention insert. No proof of service of the notice appears (Tab A Fig. 6)."),

    ("h3", "D. Service by posting and premature default (R02, R03, R05)"),
    ("n", "No reasonable diligence. On May 19, 2026 plaintiff applied ex parte for service by posting (Code Civ. Proc. " + S + " 415.45) two days after defendant's Answer dated May 17, 2026 was tendered, "
          "and while plaintiff's counsel was corresponding with defendant in the related restraining-order proceeding (Tab A Fig. 7)."),
    ("n", "Impossible declaration. The process server's declaration (Joseph Falanga, Spirit Courier) is dated May 11, 2026 and swears to an attempt on May 12, 2026 at 6:06 p.m. \u2014 a future event "
          "attested under penalty of perjury (Pen. Code " + S + " 118; Code Civ. Proc. " + S + " 2015.5) (Tab A Fig. 8)."),
    ("n", "No service on the named defendant. The only POS-010 in the record names \u201cAll Unnamed Occupants.\u201d No POS-010 naming Donald Ernest Gillson was ever filed; the June 30, 2026 entry of default is void on its face (Tab A Figs. 9\u201310)."),
    ("n", "Clerk rejection and same-day judgment. On June 10, 2026 the clerk notified the parties that the default paperwork was incomplete. Without curing service, plaintiff refiled June 30, 2026 and obtained judgment for possession the same day (Tab A Fig. 11)."),

    ("h3", "E. Emergency stay, vacation of default, preservation of defenses (R08\u2013R10)"),
    ("n", "July 7, 2026: emergency ex parte application. July 8, 2026: Hon. Charles F. Haines stayed execution of the writ through July 22, 2026 and set the motion to vacate (Tab A Fig. 12)."),
    ("n", "July 22, 2026: default set aside. August 27, 2026: the Court preserved the affirmative defenses of retaliation, habitability, failure to accommodate and unclean hands for trial (Tab A Figs. 13\u201314)."),

    ("h2", "III. Line-by-Line Index of Record Irregularities"),
    ("table", [["No.", "Document / line", "Irregularity", "Offense / consequence"],
               ["1", "R01 (notice proof)", "Both \u201ccopy given to person residing\u201d and \u201cno person found\u201d are checked.", "Internally contradictory return; Code Civ. Proc. " + S + " 1162; Pen. Code " + S + " 118."],
               ["2", "R01 (notice dates)", "Served April 8; expired April 16.", "Short of the HUD/24 C.F.R. part 247 notice period for subsidized tenancies."],
               ["3", "R01 (notice content)", "No specific statement of grounds; no ten-day meeting notice.", "24 C.F.R. " + S + " 247.4; Gersten Companies v. Deloney (1989) 212 Cal.App.3d 1119."],
               ["4", "R01 (UD-100 item 7)", "Marked so as to state that no proper notice was served.", "Judicial admission on the face of the complaint."],
               ["5", "R01 (verification)", "Verified by Jerome Bradford; names \u201cDonald Gillison.\u201d", "Code Civ. Proc. " + S + S + " 446, 1166(a)(1); pleading subject to strike."],
               ["6", "R02 (Falanga decl.)", "Signed May 11, 2026; attests to attempt May 12, 2026, 6:06 p.m.", "Declaration of a future event under penalty of perjury; Pen. Code " + S + " 118."],
               ["7", "R02 (diligence)", "Omits known email, phone and courtroom contact.", "Code Civ. Proc. " + S + " 415.45; Evartt v. Superior Court (1979) 89 Cal.App.3d 795."],
               ["8", "R02 (order)", "No signed order authorizing posting appears in the file.", "Posting without prior order is ineffective."],
               ["9", "R05 (POS-010)", "Names only \u201cAll Unnamed Occupants.\u201d", "No service on the named defendant; Code Civ. Proc. " + S + S + " 417.10, 1169."],
               ["10", "R10 (P&A signature)", "Signed by plaintiff's counsel as \u201cAttorneys for Defendant.\u201d", "Rules Prof. Conduct, rule 1.7; at minimum a defective filing."]],
     [0.45 * inch, 1.35 * inch, 2.5 * inch, 2.2 * inch]),

    ("h2", "IV. Summary of Trial Exhibits"),
    ("table", [["Tab", "Contents"],
               ["A", "Opening Notice; this Trial Brief; Integrated Statement with Figures 1\u201314 and twelve checkpoints."],
               ["E", "Audio-visual exhibits: two verified video suites (V-01\u2013V-07; second suite V-01\u2013V-06): property-level hostility, habitability collapse, resident-advisor statement, process-server conduct."],
               ["H", "The filed court record, R01\u2013R10: notice, complaint, posting application, default, judgment, stay, vacatur."],
               ["I", "Notice to counsel and civil subpoenas duces tecum: William Landrum, Jerome Bradford, John P. Zanghi, Francisco G. Torres, Michael Blecker (Swords to Plowshares), SFDPH Healthy Housing custodian, Court ADA Coordinator."],
               ["J", "MC-410 and confidential medical records, including John Muir Health emergency-department records of October 30, 2026 (rule 1.100(c)(4))."],
               ["K", "Twenty rule 1.100 responses and orders, July 20 \u2013 October 14, 2026."],
               ["L", "Evidence exhibit binder, categories A\u2013K: infestation, service-animal injuries, medical, vehicle, APS/311 reports."],
               ["M", "Administrative complaints: BBS Nos. 2002026002097 (Losik) and 2002026002098 (Villalobos)."]],
     [0.6 * inch, 5.9 * inch]),

    ("h2", "V. Conclusion and Relief Requested"),
    ("n", "Plaintiff has not established a lawful predicate notice, has not effected valid service on the named defendant, and brought this summary proceeding within 180 days of protected "
          "habitability complaints, accommodation requests and judicial petitions (Civ. Code " + S + " 1942.5)."),
    ("n", "Defendant asks that the Court enter judgment for defendant; dismiss the complaint; confirm that the June 30, 2026 default and judgment were void when entered; award the statutory "
          "retaliation remedy and costs (Civ. Code " + S + " 1942.5, subds. (h), (i)); and continue every rule 1.100 accommodation now in force for all remaining proceedings."),
]


def build_brief(path):
    f = caption("<br/>".join(TITLE))
    f.append(P(f"TO: {COURT}, {DEPT}, and to plaintiff and its counsel of record.", body))
    n = 0
    for item in CONTENT:
        kind = item[0]
        if kind == "phase": f.append(P(item[1], phase))
        elif kind == "h2":
            n = 0; f.append(P(item[1], h2))
        elif kind == "h3": f.append(P(item[1], h3))
        elif kind == "n":
            n += 1; f.append(P(f"{n}. {item[1]}", body))
        elif kind == "box": f.append(P(item[1], box))
        elif kind == "table":
            f.append(Spacer(1, 6)); f.append(grid(item[1], item[2])); f.append(Spacer(1, 8))
    f.append(Spacer(1, 10)); f.extend(signature())
    return rl(f, path, "Master Integrated Statement of the Case and Trial Brief")


if __name__ == "__main__":
    out = os.path.join(TMP, "trial_brief.pdf")
    build_brief(out); print(out)
