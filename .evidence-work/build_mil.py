"""
Defendant's Emergency Motion in Limine No. 1 (disqualify Zanghi Torres Adams LLP; exclude evidence derived from
confidential VA information; rule 1.100 procedural accommodation), with Memorandum, Declaration and [Proposed] Order.
Drafted from the defendant's text; bracketed items are facts only the defendant can supply.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer, PageBreak
from reportlab.lib import colors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, grid, signature, small, TMP, CASE_NO, COURT, DEPT, TEXT_W, DATED
from reportlab.lib.units import inch
from build_notice import body, h2, h3, phase, box

TITLE = ["DEFENDANT'S EMERGENCY MOTION IN LIMINE NO. 1 TO DISQUALIFY ZANGHI TORRES ADAMS LLP AS COUNSEL FOR PLAINTIFF AND TO EXCLUDE EVIDENCE DERIVED FROM "
         "DEFENDANT'S CONFIDENTIAL VA INFORMATION;",
         "REQUEST FOR PROCEDURAL ACCOMMODATION (CAL. RULES OF COURT, RULE 1.100);",
         "MEMORANDUM OF POINTS AND AUTHORITIES; DECLARATION OF DONALD E. GILLSON; [PROPOSED] ORDER",
         "[Code Civ. Proc. \u00a7 128(a)(5); Evid. Code \u00a7\u00a7 352, 402; Cal. Rules of Court, rules 1.100, 3.1112(f); Rules Prof. Conduct, rules 1.7, 3.7; 42 U.S.C. \u00a7 12132]"]

B = "[__________]"

CONTENT = [
    ("box", "Filing notes (remove before filing). Rule 3.1112(f): a motion in limine filed before or during trial needs no separate notice of hearing, so this can be heard at the "
            "trial call without 16 court days' notice; serve opposing counsel as early as possible. For a ruling before the trial date, also file an ex parte application "
            "(rules 3.1200 et seq.; notify counsel by 10:00 a.m. the court day before, rule 3.1203). Form MC-410 goes to the ADA coordinator separately (rule 1.100(c)(4)); this motion "
            "only says that it was submitted. Rule 1.100 changes how the defendant participates; it does not change the disqualification standard, and the motion does not say it does. "
            "Items marked [VERIFY] are to be checked against the reporter before filing."),
    ("h2", "Emergency Motion in Limine No. 1"),
    ("p", "TO PLAINTIFF SWORDS TO PLOWSHARES AND ITS ATTORNEYS OF RECORD, JOHN P. ZANGHI, NICHOLAS P. WAGENER, CHARITY MARTINEZ, AND ZANGHI TORRES ADAMS LLP:"),
    ("p", f"Defendant Donald Ernest Gillson, Ed.D., moves in limine, before the start of trial, in {DEPT} of the above-entitled Court, 400 McAllister Street, San Francisco, "
          "California 94102. Under California Rules of Court, rule 3.1112(f), no separate notice of hearing is required. Defendant asks for an order:"),
    ("n", "Disqualifying John P. Zanghi and Zanghi Torres Adams LLP from representing Plaintiff Swords to Plowshares at trial and in this action;"),
    ("n", "In the alternative, barring Mr. Zanghi from acting as trial advocate while also being a witness (Rules Prof. Conduct, rule 3.7);"),
    ("n", "Excluding any evidence, testimony, or argument derived from confidential information Defendant gave Plaintiff as his accredited VA representative (Evid. Code, \u00a7\u00a7 352, 402);"),
    ("n", "Prohibiting disqualified counsel from giving successor counsel any work product derived from that confidential information;"),
    ("n", "Continuing trial for a reasonable period, if needed, so Plaintiff can retain unconflicted counsel; and"),
    ("n", "Granting the procedural accommodations requested in Section V below."),
    ("p", f"Emergency basis. Trial call is set for November 2, 2026. Defendant learned the facts supporting this motion on {B}. If this motion is not decided before evidence is taken, "
          "Plaintiff's director-lawyer will act as both advocate and witness, and evidence derived from Defendant's confidential VA information may be put before the trier of fact. "
          "Once that happens, it cannot be undone."),
    ("p", "This motion is based on the attached Memorandum of Points and Authorities, the Declaration of Donald E. Gillson and its exhibits, the pleadings and records on file "
          "(including Tabs A through M of this binder), and any argument at the hearing."),
    ("sig", ""),
    ("h2", "Memorandum of Points and Authorities"),
    ("h3", "I. Introduction"),
    ("p", "Plaintiff's lead counsel, John P. Zanghi, is not merely Plaintiff's lawyer in this case. He sits on Plaintiff's Board of Directors, and he signed verified papers in this "
          "case as Plaintiff's agent. He is therefore both advocate and witness, and he has a personal stake in the outcome. Meanwhile, Plaintiff is, or was, Defendant's own "
          "accredited VA representative. It is now evicting the disabled veteran it was entrusted to protect, through a director-lawyer who may have access to that veteran's "
          "confidential VA information."),
    ("p", "These problems go to who may try this case and what evidence may be offered. They must be resolved before trial begins, which is exactly what a motion in limine is for."),
    ("h3", "II. Statement of Facts"),
    ("n", "Defendant is a 90% service-connected disabled veteran and a dependent adult. He resides at 1030 Girard Road, Unit 301A, San Francisco, a property operated by Plaintiff. (Gillson Decl. \u00b6 2.)"),
    ("n", f"Plaintiff [is / was] Defendant's accredited representative before the VA under VA Form 21-22, dated {B}. In that role, Plaintiff received Defendant's confidential claim, "
          "medical, and disability information. (Gillson Decl. \u00b6 3, Ex. A.)"),
    ("n", "John P. Zanghi is a member of Plaintiff's Board of Directors. (Gillson Decl. \u00b6 4, Ex. B.)"),
    ("n", f"On {B}, Mr. Zanghi signed [the verification of the Complaint / discovery responses / other document] \u201cas agent\u201d for Plaintiff, stating that Plaintiff's officers "
          "were [absent from the county / unavailable]. (Gillson Decl. \u00b6 5, Ex. C.)"),
    ("n", "On information and belief, Zanghi Torres Adams LLP has communicated with Cooley LLP about Defendant and his company, That's Edutainment LLC, and has shared information "
          "about them. (Gillson Decl. \u00b6 6, Ex. D.)"),
    ("n", "Defendant has submitted requests for accommodation under rule 1.100 in this case since July 2026 (Tab H), and a further Form MC-410 concurrently with this motion (Tab B). (Gillson Decl. \u00b6 8.)"),
    ("h3", "III. This Motion Is Properly Brought in Limine"),
    ("p", "A motion in limine is a pretrial request to resolve issues that would otherwise disrupt trial or expose the trier of fact to improper matter. (Amtower v. Photon Dynamics, "
          "Inc. (2008) 158 Cal.App.4th 1582, 1593 [VERIFY].) The court may hear it before or during trial without a separate notice of hearing. (Cal. Rules of Court, rule 3.1112(f).)"),
    ("p", "The Court also has inherent and statutory power to control the conduct of attorneys before it, including disqualifying counsel at any stage. (Code Civ. Proc., \u00a7 128(a)(5); "
          "People ex rel. Dept. of Corporations v. SpeeDee Oil Change Systems, Inc. (1999) 20 Cal.4th 1135, 1145.) Who may act as trial advocate, and whether evidence derived from "
          "confidential information may be used, are threshold questions that must be settled before the first witness is called."),
    ("h3", "IV. Argument"),
    ("p", "A. Legal standard. The paramount concern is \u201cto preserve public trust in the scrupulous administration of justice and the integrity of the bar.\u201d (SpeeDee Oil, supra, "
          "20 Cal.4th at p. 1145.) A non-client may seek disqualification when the ethical breach is \u201cmanifest and glaring\u201d and so infects the litigation that it affects the "
          "non-client's interest in a just determination of the claims. (Kennecott Utah Copper Corp. v. Union Pacific Railroad Co. (2009) 178 Cal.App.4th 1214, 1223\u20131224 [VERIFY].) "
          "Defendant also has standing as a client, or former client, of Plaintiff's VA representation."),
    ("p", "B. Mr. Zanghi is a likely witness and cannot also act as trial advocate (rule 3.7). Rule 3.7(a) prohibits a lawyer from acting as advocate in a trial in which the lawyer is "
          "likely to be a witness, unless an exception applies."),
    ("n", "Verification. Code of Civil Procedure section 446 allows an attorney to verify a corporation's pleading only when its officers are absent from the county, and the attorney "
          "must state the reason. By verifying, Mr. Zanghi made himself the source of the sworn facts, and the opposing party may examine an attorney-verifier about the basis for verified "
          "statements. (Melendrez v. Superior Court (2013) 215 Cal.App.4th 1343 [VERIFY].) Defendant intends to call Mr. Zanghi at trial."),
    ("n", "Board decision. As a director, Mr. Zanghi has personal knowledge of why Plaintiff decided to evict Defendant. That knowledge goes to Defendant's defenses of retaliation "
          "(Civ. Code, \u00a7 1942.5), discrimination, and failure to accommodate disability."),
    ("n", "No exception applies. His testimony concerns contested facts, not an uncontested matter or the value of legal services (rule 3.7(a)(1)\u2013(2)). Client consent under rule "
          "3.7(a)(3) does not cure the risk of confusion between testimony and argument, which harms the trial itself. (Rules Prof. Conduct, rule 3.7, com. [3]; Kennecott, supra, "
          "178 Cal.App.4th at p. 1231 [VERIFY].)"),
    ("p", "C. Dual roles create a disqualifying conflict (rule 1.7). Rule 1.7(b) prohibits representation when there is a significant risk that the lawyer's own interests or "
          "responsibilities to others will materially limit it. Mr. Zanghi is (1) a fiduciary of Plaintiff as a director, (2) its verifying agent, and (3) a partner in the firm Plaintiff "
          "pays to prosecute this case. As a director whose firm is compensated by the nonprofit he governs, he has a personal financial interest in the litigation (see Corp. Code, \u00a7 5233)."),
    ("p", "D. Evidence derived from Defendant's confidential VA information should be excluded, and the firm disqualified. An attorney who has obtained confidential information "
          "material to a case may be disqualified, and that disqualification extends to the firm. (Flatt v. Superior Court (1994) 9 Cal.4th 275, 283; SpeeDee Oil, supra, 20 Cal.4th at "
          "p. 1146.) Accredited VA representatives must act faithfully toward the claimants they represent (38 C.F.R. \u00a7 14.632). Defendant's disability status, benefits, and income "
          "are central to this eviction and to his defenses, so the matters are substantially related. Any evidence Plaintiff obtained through its VA representation of Defendant should "
          "be excluded; its probative value is substantially outweighed by unfair prejudice and by the damage to the integrity of these proceedings. (Evid. Code, \u00a7 352.) Defendant asks "
          "for an Evidence Code section 402 hearing outside the presence of the trier of fact before any such evidence is offered."),
    ("p", "E. Disqualification is the proportionate remedy. This is a limited-jurisdiction unlawful detainer case, and many attorneys can handle it. Any delay results from counsel's "
          "own choice to act as director, verifier, and advocate at once. A short continuance is far less harmful than a trial in which the opposing advocate is a key witness who may "
          "hold Defendant's confidential VA information."),
    ("h3", "V. Request for Procedural Accommodation (Cal. Rules of Court, rule 1.100)"),
    ("p", "Defendant is a person with disabilities within the meaning of the Americans with Disabilities Act (42 U.S.C. \u00a7 12102) and Civil Code section 51 et seq. Title II requires "
          "public entities, including state courts, to provide reasonable modifications so persons with disabilities have meaningful access to court proceedings. (42 U.S.C. \u00a7 12132; "
          "Tennessee v. Lane (2004) 541 U.S. 509, 531\u2013534.) Rule 1.100 implements that duty. Defendant's confidential Form MC-410 is submitted separately; its contents are not "
          "repeated here (rule 1.100(c)(4))."),
    ("p", "Defendant does not ask the Court to change the legal standard for disqualification. He asks for modifications to procedure so he can present this motion on equal footing "
          "with represented parties:"),
    ("n", "That this motion be heard at the trial call, or earlier by ex parte application, despite the short time before trial, because Defendant's disabilities and the medical "
          "orders described in Tab B affected his ability to prepare and file it sooner;"),
    ("n", "That the Court excuse minor technical defects in format or service that do not prejudice Plaintiff;"),
    ("n", "That Defendant be permitted to appear by Zoom, to read from prepared notes, to take scheduled breaks, and to receive written rulings, as requested in the concurrently "
          "submitted MC-410 (Tab B)."),
    ("p", "Under rule 1.100(e), the Court must respond to an accommodation request promptly and, if denied, state its reasons in writing. Under rule 1.100(g), Defendant may seek review of a denial."),
    ("h3", "VI. Conclusion"),
    ("p", "Defendant respectfully asks the Court to grant this Emergency Motion in Limine No. 1 in full, including the requested procedural accommodations."),
    ("sig", ""),
    ("page", ""),
    ("h2", "Declaration of Donald E. Gillson"),
    ("p", "I, Donald Ernest Gillson, declare:"),
    ("d", "I am the Defendant in this action. I have personal knowledge of the facts below, except those stated on information and belief, which I believe to be true. If called as a "
          "witness, I could and would testify competently to them."),
    ("d", "I am a 90% service-connected disabled veteran. I reside at 1030 Girard Road, Unit 301A, San Francisco, California."),
    ("d", "Swords to Plowshares [is / was] my accredited representative before the VA. A true copy of my VA Form 21-22 [and/or other proof] is attached as Exhibit A. In that role, "
          "I gave Swords to Plowshares confidential information about my disabilities, medical history, and benefits."),
    ("d", "John P. Zanghi serves on the Board of Directors of Swords to Plowshares. A true copy of [the source] is attached as Exhibit B."),
    ("d", f"Mr. Zanghi signed [document name(s)] in this case as agent for Swords to Plowshares on {B}. True copies are attached as Exhibit C."),
    ("d", "On information and belief, Zanghi Torres Adams LLP has communicated with Cooley LLP about me and That's Edutainment LLC. The basis for this belief is [describe]. A true "
          "copy is attached as Exhibit D."),
    ("d", f"I learned of Mr. Zanghi's board position and verification on {B}. Because of my disabilities, and the medical orders of October 30, 2026 described in Tab B, I needed "
          "additional time to research and prepare this motion and could not file it earlier."),
    ("d", "I have submitted confidential requests for accommodation (Form MC-410) to the court's ADA coordinator, including the request submitted with this motion."),
    ("d", "I intend to call Mr. Zanghi as a witness at trial about the facts he verified and the Board's decision to bring this action."),
    ("p", "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct."),
    ("p", f"Executed on {DATED}, at San Francisco, California."),
    ("sig", ""),
    ("page", ""),
    ("h2", "[Proposed] Order on Defendant's Emergency Motion in Limine No. 1"),
    ("p", "The Court, having considered Defendant's Emergency Motion in Limine No. 1 and the papers and arguments submitted, and good cause appearing, ORDERS:"),
    ("o", "The motion is GRANTED."),
    ("o", "John P. Zanghi and Zanghi Torres Adams LLP are DISQUALIFIED from representing Plaintiff Swords to Plowshares in this action."),
    ("o", "Evidence, testimony, or argument derived from confidential information Defendant gave Plaintiff as his accredited VA representative is EXCLUDED, subject to an Evidence "
          "Code section 402 hearing if Plaintiff seeks to offer such evidence."),
    ("o", "Disqualified counsel shall not transmit to successor counsel any work product derived from Defendant's confidential information."),
    ("o", f"Trial is CONTINUED to {B} to allow Plaintiff to substitute counsel."),
    ("o", f"Defendant's requested procedural accommodations are GRANTED as follows: {B}."),
    ("p", "IT IS SO ORDERED."),
    ("p", f"Dated: {B}\u2003\u2003\u2003\u2003______________________________<br/>Judge of the Superior Court"),
    ("page", ""),
    ("h2", "Checklist Before Filing"),
    ("table", [["Done", "Item"],
               ["\u2610", "Submit Form MC-410 to the ADA coordinator now, separate from this motion (copy at Tab B)"],
               ["\u2610", f"Ask the {DEPT} clerk: ex parte before trial, or in limine at the November 2 trial call?"],
               ["\u2610", "Exhibit A: VA Form 21-22 or other proof that Swords to Plowshares represented Defendant before the VA"],
               ["\u2610", "Exhibit B: proof Mr. Zanghi is a director (IRS Form 990, Secretary of State filing, or plaintiff's website)"],
               ["\u2610", "Exhibit C: every document Mr. Zanghi signed \u201cas agent\u201d"],
               ["\u2610", "Exhibit D: the Cooley LLP-related emails"],
               ["\u2610", "Confirm the citations marked [VERIFY]"],
               ["\u2610", "Pleading paper (rule 2.108), sign, three copies; serve counsel and file Proof of Service; bring the proposed order"]],
     [0.7 * inch, TEXT_W - 0.7 * inch]),
]


def build_mil(path):
    f = caption("<br/>".join(TITLE))
    n = 0
    for item in CONTENT:
        kind, text = item[0], item[1]
        if kind == "h2": n = 0; f.append(P(text, h2))
        elif kind == "h3": n = 0; f.append(P(text, h3))
        elif kind == "p": f.append(P(text, body))
        elif kind in ("n", "d", "o"):
            n += 1; f.append(P(f"{n}. {text}", body))
        elif kind == "box": f.append(P(text, box))
        elif kind == "sig": f.append(Spacer(1, 8)); f.extend(signature()); n = 0
        elif kind == "page": f.append(PageBreak())
        elif kind == "table": f.append(Spacer(1, 6)); f.append(grid(item[1], item[2])); f.append(Spacer(1, 8))
    return rl(f, path, "Emergency Motion in Limine No. 1 \u2013 Disqualification of Counsel")


if __name__ == "__main__":
    out = os.path.join(TMP, "mil_1.pdf")
    build_mil(out); print(out)
