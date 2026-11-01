"""
Opening paper for both binders:

  NOTICE OF GOVERNMENT CLAIMS; REQUEST FOR JUDICIAL NOTICE; VERIFIED STATEMENT OF
  DISQUALIFICATION (CCP 170.3(c)); NOTICE OF FEDERAL RIGHTS AND RESERVATION OF REMOVAL;
  POINTS AND AUTHORITIES (STATE AND FEDERAL)

Written to be filed: every demand is tied to a statute or rule that actually authorizes it,
and the record cites point at R01-R10 / Tabs of the binder. 12.5 pt body, 22.5 pt headings.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer, KeepTogether, PageBreak
from reportlab.lib import colors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_allinone as A
from build_allinone import P, rl, caption, grid, signature, h1, h2, h3, body, small, cen, TMP, CASE_NO, COURT, DEPT, DATED, NAME

BODY_PT, H2_PT, H3_PT = 12.5, 22.5, 15
body = ParagraphStyle("nbody", parent=body, fontSize=BODY_PT, leading=BODY_PT * 1.45, spaceAfter=8)
h2 = ParagraphStyle("nh2", parent=h2, fontSize=H2_PT, leading=H2_PT * 1.2, spaceBefore=16, spaceAfter=8)
h3 = ParagraphStyle("nh3", parent=h3, fontSize=H3_PT, leading=H3_PT * 1.3, spaceBefore=12, spaceAfter=6)
phase = ParagraphStyle("nphase", parent=small, fontSize=9.5, leading=12, textColor=colors.HexColor("#555555"), spaceBefore=14)
box = ParagraphStyle("nbox", parent=body, fontSize=11.5, leading=16, leftIndent=14, rightIndent=14, borderColor=colors.HexColor("#555555"),
                     borderWidth=0.6, borderPadding=8, spaceBefore=10, spaceAfter=14)

TITLE = ["NOTICE OF GOVERNMENT CLAIMS PRESENTED AGAINST THE CITY AND COUNTY OF SAN FRANCISCO AND THE SUPERIOR COURT;",
         "REQUEST FOR JUDICIAL NOTICE (EVID. CODE \u00a7\u00a7 452, 453);",
         "VERIFIED STATEMENT OF DISQUALIFICATION (CODE CIV. PROC. \u00a7 170.3, SUBD. (c)) AND PEREMPTORY CHALLENGE IN THE ALTERNATIVE (\u00a7 170.6);",
         "NOTICE OF FEDERAL RIGHTS, RESERVATION OF REMOVAL, AND REQUEST THAT ENFORCEMENT STAND DOWN;",
         "MEMORANDUM OF POINTS AND AUTHORITIES (STATE AND FEDERAL)"]

CONTENT = [
    ("phase", "STRUCTURE: ANALYZE \u2192 DESIGN \u2192 DEVELOP \u2192 IMPLEMENT \u2192 EVALUATE. Each part states what is noticed, the authority that permits it, and what is asked."),
    ("h2", "Reader's Map"),
    ("table", [["Part", "What it does", "Authority"],
               ["I", "Gives notice that Government Claims have been presented against the City and County and against the Superior Court, and asks the Court to take judicial notice of them.", "Gov. Code \u00a7\u00a7 905, 910, 911.2, 912.7; Evid. Code \u00a7 452(c), (d), (h)"],
               ["II", "Verified statement of disqualification of the assigned judicial officer for cause; peremptory challenge in the alternative; request for reassignment outside Department 606.", "Code Civ. Proc. \u00a7\u00a7 170.1(a)(6)(A)(iii), 170.3(c), 170.6; Cal. Code Jud. Ethics, canon 3E"],
               ["III", "Notice of federal rights engaged by this case and reservation of removal and federal relief.", "42 U.S.C. \u00a7\u00a7 12131\u201312134, 3604, 3617, 1983; 29 U.S.C. \u00a7 794; 28 U.S.C. \u00a7\u00a7 1441, 1443, 1446; 16 U.S.C. \u00a7 460bb note"],
               ["IV", "Request that enforcement stand down pending resolution of Parts I\u2013III and the pending rule 1.100 requests.", "Code Civ. Proc. \u00a7\u00a7 918, 1176; Cal. Rules of Court, rule 1.100(e)(2)"],
               ["V", "Memorandum of points and authorities, state and federal, with the record cites.", "\u2014"],
               ["VI", "Verification and reservation of rights.", "Code Civ. Proc. \u00a7\u00a7 170.3(c)(1), 2015.5"]],
     [0.55 * inch, 3.6 * inch, 2.35 * inch]),

    ("phase", "PHASE 1 \u2014 ANALYZE"),
    ("h2", "I. Notice of Government Claims and Request for Judicial Notice"),
    ("n", "Defendant gives notice that he has presented, or is presenting concurrently with this paper, claims under the Government Claims Act (Gov. Code, \u00a7 810 et seq.) "
          "as follows. (a) Against the City and County of San Francisco, presented to the Controller / Clerk of the Board of Supervisors under Government Code sections 905, 910 "
          "and 911.2, for injuries arising from the conduct of City agencies and officers in connection with the tenancy at 1030 Girard Road, Unit 301A, including the Sheriff's "
          "participation in enforcement of a default judgment entered without service on the named defendant (R07; Tab A, Figs. 7\u201310) and the City's administration of the "
          "federal housing subsidy and inspection functions implicated by the habitability record (Tab L). (b) Against the Superior Court of California, County of San Francisco, "
          "presented to the Judicial Council of California as the claims body for judicial-branch entities under Government Code section 912.7, for injuries arising from the "
          "Court's administrative handling of defendant's disability accommodation requests under rule 1.100 and its records-access obligations under Title II of the ADA, as "
          "distinct from any judicial decision. Claim numbers and dates of presentation will be lodged with the Court upon receipt of acknowledgment."),
    ("n", "Defendant requests that the Court take judicial notice under Evidence Code sections 452, subdivisions (c), (d) and (h), and 453, of: (1) the two Government Claims "
          "described above and the official acts of receiving them; (2) the records of this Court in CUD-26-682107 (R01\u2013R10, Tab H) and in CCH-26-589086; (3) the rule 1.100 "
          "orders and responses of this Court dated July through October 2026 (Tab K); (4) the complaints pending before the Board of Behavioral Sciences, Nos. 2002026002097 "
          "and 2002026002098 (Tab L, Evidence Exhibit Binder, Category K); (5) the San Francisco 311 record, Case 101003004371; and (6) the Presidio Trust Act, Pub. L. 104-333, title I, \u00a7 103, as amended "
          "(16 U.S.C. \u00a7 460bb note), establishing the federal status of the Presidio of San Francisco within which the premises lie. Copies of items (2)\u2013(4) are in this binder; "
          "items (1), (5) and (6) are public records whose existence is not reasonably subject to dispute."),
    ("box", "What is noticed is the existence and content of these official acts and records, not the truth of every statement within them. Evidence Code section 452 "
            "permits exactly this; the Court is asked to do no more."),
    ("chk", "Government claims presented to the City (\u00a7 910) and to the Judicial Council for the Court (\u00a7 912.7); public records listed (1)\u2013(6).",
            "Claim acknowledgment numbers (to be lodged on receipt).", "Take judicial notice; note the claims on the register of actions."),

    ("phase", "PHASE 2 \u2014 DESIGN"),
    ("h2", "II. Verified Statement of Disqualification; Peremptory Challenge in the Alternative; Request for Reassignment"),
    ("h3", "A. Statement of disqualification for cause (Code Civ. Proc., \u00a7\u00a7 170.1, 170.3, subd. (c))"),
    ("n", "Under Code of Civil Procedure section 170.3, subdivision (c)(1), defendant files this verified statement objecting to the hearing or trial of this matter before the "
          "judicial officer presently assigned to Department 606 and setting forth the facts constituting the grounds for disqualification. The statement is presented at the "
          "earliest practicable opportunity after discovery of the facts: the October 30, 2026 emergency-department record and the October 2026 refusals to act on pending "
          "rule 1.100 requests (Tabs J, K) post-date the prior orders in this case."),
    ("n", "Grounds. (1) A person aware of the facts might reasonably entertain a doubt that the judicial officer would be able to be impartial (\u00a7 170.1, subd. (a)(6)(A)(iii)), where: "
          "(a) accommodation requests under rule 1.100 that were granted in Departments 501 and 505 in July\u2013September 2026 (Tab K, Exs. 1\u201312) were thereafter narrowed or left "
          "unruled in Department 606 while trial was advanced (Tab K, Exs. 13\u201320); (b) the Court has in defendant's presence adopted plaintiff's characterization of his assistive-technology "
          "record as unreliable, without an evidentiary basis (Tab A \u00a7 III.J); (c) the Court has set in-person trial call for November 2, 2026 notwithstanding a treating physician's "
          "order placing defendant off activity through November 3 (Tab J); and (d) defendant's May 17, 2026 Answer was treated as unfiled while a default was entered on a proof of "
          "service naming only \u201cAll Unnamed Occupants\u201d (Tab A, Figs. 7\u201310; R09). (2) Each of these is a fact, stated on personal knowledge, that bears on the appearance of "
          "impartiality under canon 3E of the Code of Judicial Ethics; defendant does not allege, and need not allege, actual bias."),
    ("n", "Procedure requested. Section 170.3, subdivision (c)(3), requires the judge, within ten days, to file a consent to disqualification or a verified answer; failure to do so is "
          "deemed consent (\u00a7 170.3, subd. (c)(4)). If the statement is contested, the question of disqualification is to be heard and determined by a judge agreed upon by the "
          "parties or, failing agreement, by a judge selected by the Chairperson of the Judicial Council (\u00a7 170.3, subd. (c)(5)). Defendant asks that no further orders issue in this "
          "case other than those necessary to preserve the status quo until the statement is determined (\u00a7 170.4, subds. (a), (c), (d))."),
    ("h3", "B. Peremptory challenge in the alternative (Code Civ. Proc., \u00a7 170.6)"),
    ("n", "If and to the extent the matter has not yet been assigned for all purposes to a judge who has ruled on a contested fact issue relating to the merits, defendant exercises "
          "his peremptory challenge under section 170.6 against the judicial officer presently assigned, supported by the declaration below (\u00a7 170.6, subd. (a)(2), (6)). Defendant "
          "acknowledges that a party has one such challenge and that it must be timely; it is made here in the alternative so that the Court may rule on the for-cause statement first."),
    ("h3", "C. Request for reassignment outside Department 606"),
    ("n", "Defendant asks the Presiding Judge, under California Rules of Court, rule 10.603(c)(1)(C) and (D), to reassign this matter to a department other than 606 and, given that "
          "accommodation requests in this case have now been handled by three departments with inconsistent results (Tab K), to assign a single judicial officer for all purposes "
          "with the ADA Coordinator's recommendations before that officer. Defendant does not ask that every judge of this Court be disqualified; that is not a remedy section 170.1 "
          "provides. He asks for one impartial officer, outside the department in which the facts above arose, and for the Judicial Council to select that officer if the parties "
          "cannot agree (\u00a7 170.3, subd. (c)(5))."),
    ("chk", "Verified statement under \u00a7 170.3(c) with four enumerated facts; \u00a7 170.6 challenge in the alternative; reassignment request to the Presiding Judge.",
            "Nothing further is required of defendant; the ten-day clock under \u00a7 170.3(c)(3) runs from service.",
            "Strike or answer within ten days (\u00a7 170.3(c)(3)); stay merits orders meanwhile (\u00a7 170.4)."),

    ("phase", "PHASE 3 \u2014 DEVELOP"),
    ("h2", "III. Notice of Federal Rights Engaged and Reservation of Removal"),
    ("n", "Americans with Disabilities Act, Title II. The Superior Court is a public entity (42 U.S.C. \u00a7 12131(1)). It may not exclude a qualified individual with a disability from "
          "participation in, or deny him the benefits of, its services, programs or activities (\u00a7 12132), and it must make reasonable modifications in policies, practices and "
          "procedures and furnish auxiliary aids and services (28 C.F.R. \u00a7\u00a7 35.130(b)(7), 35.160). Access to the courts is a fundamental right to which Title II validly applies "
          "(Tennessee v. Lane (2004) 541 U.S. 509, 531\u2013534). Rule 1.100 is California's implementation of that obligation (rule 1.100(a)); its orders are enforceable as ADA compliance, "
          "not as discretionary courtesies. Section 504 of the Rehabilitation Act (29 U.S.C. \u00a7 794) imposes the same obligations on recipients of federal financial assistance, which "
          "both the Court and plaintiff are."),
    ("n", "Fair Housing Act and FEHA. Plaintiff's notice names the accommodated written channel and the elder-abuse petition as grounds (Tab A, Fig. 1). That is interference with "
          "the exercise of fair-housing rights (42 U.S.C. \u00a7 3617; 24 C.F.R. \u00a7 100.400) and refusal of a reasonable accommodation (\u00a7 3604(f)(3)(B); Gov. Code, \u00a7 12927, subd. (c)(1)). "
          "HUD-VASH and SSVF participation subject plaintiff to 24 C.F.R. part 982 and the VA's program requirements; the Department of Veterans Affairs Office of Inspector General "
          "and HUD's Office of Fair Housing and Equal Opportunity have been noticed."),
    ("n", "Federal status of the premises. The Presidio of San Francisco is federal land administered by the Presidio Trust under the Presidio Trust Act (16 U.S.C. \u00a7 460bb note; "
          "Pub. L. 104-333, \u00a7 103). Residential leasing within the Presidio operates under Trust ground leases and federal program agreements. Defendant does not contend that this "
          "Court lacks subject-matter jurisdiction over an unlawful detainer by reason of federal ownership alone; he contends that the federal program conditions attached to the "
          "tenancy, and the Trust's and VA's oversight roles, are part of the record of plaintiff's obligations and are reserved for the federal forum."),
    ("n", "Civil-rights remedies. 42 U.S.C. \u00a7 1983 provides a remedy against persons acting under color of state law who deprive a citizen of federal rights, and against a municipality "
          "whose policy or custom causes the deprivation (Monell v. Department of Social Services (1978) 436 U.S. 658, 690\u2013691). Defendant acknowledges that judicial officers are "
          "absolutely immune from damages for judicial acts (Stump v. Sparkman (1978) 435 U.S. 349, 356\u2013357; Mireles v. Waco (1991) 502 U.S. 9, 11\u201312) and that the Government Claim "
          "against the Court in Part I is accordingly directed at administrative, not adjudicative, conduct \u2014 the processing of accommodation requests and records access. Title II "
          "itself contains no such immunity for the entity (United States v. Georgia (2006) 546 U.S. 151, 159)."),
    ("n", "Interstate business interests. Defendant is the principal of That's Edutainment LLC and 32D LLC, a Nevada limited liability company, and operates the 18fu.ai "
          "platform from a node in Saint Paul, Minnesota. Unit 301A is his California place of business as well as his residence. The displacement described in Part IV has "
          "interrupted those operations across state lines; the resulting losses are part of the Government Claims in Part I and of the damages reserved for the federal forum. "
          "Defendant states these facts for the record and does not contend that they alone confer federal jurisdiction. The assistive-technology record system described in "
          "Tab A \u00a7 III.J is deployed as a web application (v0-shadcn-6rk4pboha-dgillson9175-1000s-projects.vercel.app) and is the repository of every communication, filing "
          "and timestamp in this case. Defendant states, on information and belief, that plaintiff's agents' demands that he \u201cstop with the emails\u201d and their characterization "
          "of that system as unreliable are directed at the record it holds; he asks that the system and its contents be treated as protected work product and assistive "
          "technology, and that any demand for its shutdown or surrender be made only by noticed motion."),
    ("n", "Service of papers distinguished from correspondence. Plaintiff's counsel has characterized defendant's lodged binders as \u201cvoluminous emails.\u201d The formal binders and "
          "bench copies were served through Rapid Legal, a registered process server, under Code of Civil Procedure sections 1010\u20131013 and rule 2.251, and the proofs of service are "
          "in Tab H and Tab I. Email was used only for the written-communication accommodation that plaintiff's own agent agreed to on December 23, 2025 (Tab A, Integrated Statement, Fig. 1)."),
    ("n", "Reservation of removal. Defendant reserves the right to remove this action to the United States District Court for the Northern District of California under 28 U.S.C. "
          "sections 1441, 1443(1) and 1446, and to seek relief there under Title II, section 504, the Fair Housing Act and section 1983. Defendant is aware that removal of an "
          "unlawful detainer is tested against the well-pleaded complaint rule and that section 1443(1) is construed narrowly (Georgia v. Rachel (1966) 384 U.S. 780, 792; Johnson v. "
          "Mississippi (1975) 421 U.S. 213, 219); the reservation is made with that law in view, and the notice of removal, if filed, will be filed in good faith on the grounds stated "
          "there and not as a device to delay. Until a notice of removal is filed and a copy lodged with this Court, this Court retains jurisdiction (28 U.S.C. \u00a7 1446(d))."),
    ("chk", "Title II / \u00a7 504 duties of the Court; FHA \u00a7\u00a7 3604(f)(3)(B), 3617 on the notice's face; federal program status of the premises; \u00a7 1983 and Monell; removal reserved under \u00a7\u00a7 1441, 1443, 1446.",
            "A filed notice of removal \u2014 not yet filed; this Court retains jurisdiction until \u00a7 1446(d) is satisfied.",
            "Treat rule 1.100 compliance as a federal obligation, not a courtesy."),

    ("phase", "PHASE 4 \u2014 IMPLEMENT"),
    ("h2", "IV. Request That Enforcement Stand Down"),
    ("n", "Defendant asks that no writ of possession issue or be executed, and that the November 2, 2026 trial call be continued or conducted remotely, until: (a) the statement of "
          "disqualification is determined (\u00a7 170.4); (b) the pending rule 1.100 requests (Tab J; Tab K, Exs. 13\u201320) are ruled on in writing with the findings rule 1.100(e)(2) "
          "requires if any part is denied; and (c) the treating physician's activity restrictions have lapsed (Tab J). A trial court must consider an ADA-based continuance request "
          "under rule 1.100, not under the ordinary good-cause standard, and must state its reasons for any denial (Vesco v. Superior Court (2013) 221 Cal.App.4th 275, 282\u2013284; "
          "In re Marriage of James & Christine C. (2008) 158 Cal.App.4th 1261, 1273\u20131274). Code of Civil Procedure section 1176 authorizes a stay of enforcement in an unlawful detainer "
          "pending appeal on conditions; section 918 authorizes a stay of up to ten days beyond the time to appeal. Defendant will post the use-and-occupancy payments the Court sets."),
    ("n", "Constructive displacement. Defendant's enforced absence from the unit \u2014 sheltering aboard a vessel in Vallejo, Solano County, under a posted eviction, with the travel, "
          "cost and medical risk that entails for a person with TBI and PTSD (Tab J; Tab D, Ex. E) \u2014 is the practical result of a default entered without service (Tab A, Figs. 7\u201310) "
          "and of the Court's delay in acting on accommodation requests. Defendant records this so that the damages period is fixed in the record from the date of the first unserved "
          "default, June 30, 2026, and so that the related Solano County civil-harassment matter has the complete San Francisco record before it."),
    ("chk", "Stay authority (\u00a7\u00a7 170.4, 918, 1176; rule 1.100(e)(2); Vesco); physician's orders (Tab J); displacement record.",
            "Written findings on the pending rule 1.100 requests.", "Stay enforcement; continue or conduct trial call remotely; rule in writing."),

    ("phase", "PHASE 5 \u2014 EVALUATE"),
    ("h2", "V. Memorandum of Points and Authorities"),
    ("h3", "A. California"),
    ("table", [["Authority", "Proposition", "Record"],
               ["Gov. Code \u00a7\u00a7 905, 910, 911.2, 912.7", "Claims against local public entities are presented to the entity; claims against judicial-branch entities to the Judicial Council; six-month presentation period for personal injury.", "Part I"],
               ["Evid. Code \u00a7\u00a7 452(c), (d), (h), 453", "Judicial notice of official acts, court records, and facts not reasonably subject to dispute; mandatory on request with notice and sufficient information.", "Part I"],
               ["Code Civ. Proc. \u00a7\u00a7 170.1(a)(6)(A)(iii), 170.3(c), 170.4", "Disqualification where a reasonable person might doubt impartiality; verified statement procedure; limits on the challenged judge's powers pending determination.", "Part II.A"],
               ["Code Civ. Proc. \u00a7 170.6", "One peremptory challenge per side, timely made, no cause required.", "Part II.B"],
               ["Cal. Rules of Court, rule 1.100", "Accommodation requests may be made at any time; denials require written findings on specified grounds; medical information confidential.", "Tabs J, K"],
               ["Vesco v. Superior Court (2013) 221 Cal.App.4th 275", "ADA continuance request must be analyzed under rule 1.100; denial without the required findings is an abuse of discretion.", "Part IV"],
               ["In re Marriage of James & Christine C. (2008) 158 Cal.App.4th 1261", "Court must consider accommodation request on its merits and state reasons; disability-related inability to participate is not a basis to proceed without the party.", "Part IV"],
               ["Biscaro v. Stern (2010) 181 Cal.App.4th 702", "Failure to rule on a rule 1.100 request is itself error requiring reversal of the resulting judgment.", "Tab K, Exs. 13\u201320"],
               ["Civ. Code \u00a7 1942.5(a), (d)", "Retaliatory eviction presumption within 180 days of protected complaints; retaliation for exercise of rights barred.", "Tab A \u00a7 III.A\u2013B"],
               ["Code Civ. Proc. \u00a7\u00a7 415.45, 585, 473(d)", "Posting requires a court order on a showing of diligence; default without service of summons on the named defendant is void.", "Tab A, Figs. 3, 6\u201310"],
               ["Code Civ. Proc. \u00a7\u00a7 918, 1176", "Stays of enforcement.", "Part IV"],
               ["Cal. Rules of Court, rule 10.603(c)(1)", "Presiding Judge's authority to assign and reassign cases.", "Part II.C"]],
     [2.0 * inch, 3.3 * inch, 1.2 * inch]),
    ("h3", "B. Federal"),
    ("table", [["Authority", "Proposition", "Record"],
               ["42 U.S.C. \u00a7\u00a7 12131\u201312134; 28 C.F.R. \u00a7\u00a7 35.130(b)(7), 35.160", "Title II: state courts are public entities; duty to modify procedures and furnish auxiliary aids and services.", "Part III"],
               ["Tennessee v. Lane (2004) 541 U.S. 509", "Title II validly abrogates state immunity as applied to access to the courts.", "Part III"],
               ["United States v. Georgia (2006) 546 U.S. 151", "Title II creates a private cause of action for damages against the state for conduct that actually violates the Fourteenth Amendment.", "Part III"],
               ["29 U.S.C. \u00a7 794", "Section 504: no exclusion from programs receiving federal financial assistance by reason of disability.", "Part III"],
               ["42 U.S.C. \u00a7\u00a7 3604(f)(3)(B), 3617; 24 C.F.R. \u00a7\u00a7 100.204, 100.400", "Refusal of reasonable accommodation; interference, coercion, intimidation in the exercise of fair-housing rights.", "Tab A, Figs. 1\u20132"],
               ["24 C.F.R. part 982; 38 U.S.C. \u00a7 2041 et seq.", "Housing Choice Voucher / HUD-VASH program obligations of participating owners.", "Part III"],
               ["16 U.S.C. \u00a7 460bb note (Presidio Trust Act, Pub. L. 104-333, \u00a7 103)", "Federal status and administration of the Presidio of San Francisco.", "Part I, item (6)"],
               ["42 U.S.C. \u00a7 1983; Monell v. Dept. of Social Services (1978) 436 U.S. 658", "Remedy against persons and municipalities for deprivation of federal rights under color of law.", "Part III"],
               ["Stump v. Sparkman (1978) 435 U.S. 349; Mireles v. Waco (1991) 502 U.S. 9", "Judicial immunity from damages for judicial acts \u2014 acknowledged; claim against Court limited to administrative conduct.", "Part III"],
               ["28 U.S.C. \u00a7\u00a7 1441, 1443(1), 1446; Georgia v. Rachel (1966) 384 U.S. 780; Johnson v. Mississippi (1975) 421 U.S. 213", "Removal; narrow construction of civil-rights removal; state court retains jurisdiction until notice filed and lodged.", "Part III"],
               ["42 U.S.C. \u00a7 12103(1); 28 C.F.R. \u00a7\u00a7 35.104, 36.303", "Auxiliary aids and services include assistive technology; defendant's timestamped record system is such an aid.", "Tab A \u00a7 III.J"],
               ["Pen. Code \u00a7 632(c)", "No confidential communication where parties may reasonably expect to be overheard; common-area recordings lawful.", "Tab A \u00a7 III.J; Tab E"]],
     [2.0 * inch, 3.3 * inch, 1.2 * inch]),
    ("h3", "C. What this paper does not do"),
    ("n", "It does not ask this Court to find that it lacks jurisdiction; it does not ask that every judge of the Court be disqualified; it does not threaten counsel or the Court. "
          "It gives the notices the law requires before the remedies it reserves can be pursued, it invokes the disqualification procedure the Legislature provided, and it "
          "asks the Court to do what rule 1.100 and Title II already require. Defendant's good faith in each of these is verified below."),

    ("h2", "VI. Verification and Reservation of Rights"),
    ("n", "I, Donald Gillson, am the defendant in this action. I have read the foregoing Notice, Request for Judicial Notice, Statement of Disqualification and Memorandum. The facts "
          "stated in Parts I, II and IV are true of my own knowledge, except as to matters stated on information and belief, and as to those matters I believe them to be true. "
          "The statement of disqualification in Part II is made in good faith and not for the purpose of delay. I reserve all rights and remedies in this Court, in the Superior Court "
          "of Solano County, in the United States District Court, and before the federal and state agencies noticed, and waive none by proceeding here. I declare under penalty of "
          "perjury under the laws of the State of California that the foregoing is true and correct."),
]

chkstyle = ParagraphStyle("nchk", parent=small, fontSize=10, leading=13.5)
from reportlab.platypus import Table, TableStyle
chkbox = TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#888888")),
                     ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)])


def chk_flowable(shown, missing, asked):
    rows = [[P("<b>CHECK-<br/>POINT</b>", chkstyle), P("<b>Record shows</b>", chkstyle), P("<b>Record omits</b>", chkstyle), P("<b>Asked of the Court</b>", chkstyle)],
            ["", P(shown, chkstyle), P(missing, chkstyle), P(asked, chkstyle)]]
    t = Table(rows, colWidths=[1.0 * inch, 1.9 * inch, 1.8 * inch, 1.8 * inch]); t.setStyle(chkbox)
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def build_notice(path):
    f = caption("<br/>".join(TITLE))
    f.append(P(f"TO: {COURT}, {DEPT}, and to plaintiff and its counsel of record.", body))
    n = 0
    for item in CONTENT:
        kind = item[0]
        if kind == "phase": f.append(P(item[1], phase))
        elif kind == "h2": f.append(P(item[1], h2))
        elif kind == "h3": f.append(P(item[1], h3))
        elif kind == "n":
            n += 1; f.append(P(f"{n}. {item[1]}", body))
        elif kind == "box": f.append(P(item[1], box))
        elif kind == "chk": f.append(chk_flowable(*item[1:]))
        elif kind == "table":
            f.append(Spacer(1, 6)); f.append(grid(item[1], item[2])); f.append(Spacer(1, 8))
    f.append(Spacer(1, 10)); f.extend(signature())
    return rl(f, path, "Notice of Government Claims; Disqualification; Federal Rights")


if __name__ == "__main__":
    out = os.path.join(TMP, "notice_opening.pdf")
    build_notice(out); print(out)
