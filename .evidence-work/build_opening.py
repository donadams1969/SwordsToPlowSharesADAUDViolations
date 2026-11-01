"""
OPENING STATEMENT AND APPLICATION FOR REASONABLE ACCOMMODATION AND EMERGENCY JUDICIAL ACCESS (VESCO)
First document in Tab A of the San Francisco binder. Dated November 1, 2026.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP, COURT, DEPT

nbody = ParagraphStyle("opbody", parent=body, fontSize=12.5, leading=18.5, spaceAfter=9)
nh2 = ParagraphStyle("oph2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6)
bullet = ParagraphStyle("opbul", parent=nbody, leftIndent=18, bulletIndent=4, spaceAfter=6)

TITLE = ("OPENING STATEMENT;<br/>APPLICATION FOR REASONABLE ACCOMMODATION (CAL. RULES OF COURT, RULE 1.100) AND FOR EMERGENCY JUDICIAL ACCESS "
         "UNDER <i>VESCO v. SUPERIOR COURT</i> (2013) 221 CAL.APP.4TH 275")


def build(path):
    f = caption(TITLE)
    f.append(P(f"TO THE HONORABLE STEPHEN M. MURPHY, PRESIDING, {DEPT}, {COURT}:", nbody))
    f.append(P("May it please the Court.", nbody))
    f.append(P("My name is Dr. Donald Ernest Gillson, Ed.D. I appear before this Court seeking an immediate reasonable accommodation and formal judicial "
               "recognition of the filings I have submitted directly to Department 606. For the past several weeks my urgent medical needs, physical "
               "vulnerabilities, and documented disabilities have been met with administrative and procedural disregard that has placed my health, safety, "
               "and housing security in jeopardy. I make this opening statement and emergency notice so that the Court is fully informed of the medical "
               "necessity behind these submissions, and so that the record reflects that every transmission of evidence was made in good faith under the "
               "accommodation framework the Rules of Court and the Americans with Disabilities Act provide.", nbody))

    f.append(P("I. Medical Necessity and the Need for Immediate Judicial Access", nh2))
    f.append(P("The record before this Court, including my VA Blue Button medical reports (Evidence Exhibit Binder, Category M) and the emergency-department "
               "record of October 30, 2026 (Tab J), documents chronic conditions including cervical spinal stenosis at C5\u2013C6 with upper-extremity tremor and "
               "transient right-hand paralysis, peripheral neuropathy, foot drop, complex PTSD and traumatic brain injury, and acute injuries from a fall. "
               "The disregard of these conditions over the past weeks has forced me to rely on the emergency mechanisms the law provides to protect my life "
               "and my right to be heard.", nbody))
    f.append(P("To address these medical and housing vulnerabilities without being stopped by dilatory procedural barriers, I invoke my right under rule 1.100 "
               "and <i>Vesco v. Superior Court</i> (2013) 221 Cal.App.4th 275 to have my accommodation requests considered as such, ruled on in writing with the "
               "findings rule 1.100(e)(2) requires, and to transmit critical health records, investigative notices, and evidentiary binders directly to this Court "
               "through the written channel that is itself an ordered accommodation (Tab K).", nbody))

    f.append(P("II. Notice of Rule 1.100 and Vesco Rights; Lawful Transmission of Medical Evidence; Response to Claims of Procedural Obstruction", nh2))
    f.append(P("Please take further notice that any attempt by plaintiff Swords to Plowshares and its counsel to use procedural delay, including artificial "
               "\u201cfive-day notice\u201d or \u201creasonable accommodation\u201d objections, to suppress evidence is without merit and contrary to the protections "
               "that govern an accommodated litigant.", nbody))
    f.append(P("<b>1. The primacy of the accommodation framework.</b>", nbody))
    f.append(P("<b>Immediate judicial access.</b> Under <i>Vesco</i>, rule 1.100, and the ex parte and writ procedures of this Court, a litigant facing imminent "
               "displacement, medical vulnerability, and institutional retaliation is entitled to present health records, investigative notices, and evidentiary "
               "binders to the Court promptly and to have an accommodation request decided under rule 1.100 rather than the ordinary good-cause standard "
               "(<i>Vesco</i>, at pp. 282\u2013284; <i>In re Marriage of James &amp; Christine C.</i> (2008) 158 Cal.App.4th 1261, 1273\u20131274).", bullet, ))
    f.append(P("<b>Priority over dilatory objection.</b> The Court must consider the accommodation request on its merits; counsel's procedural objections do not "
               "relieve the Court of that duty, and a veteran's life, safety, and due-process rights are not to be subordinated to bureaucratic delay "
               "(42 U.S.C. \u00a7 12132; 28 C.F.R. \u00a7 35.130(b)(7); <i>Tennessee v. Lane</i> (2004) 541 U.S. 509, 531\u2013534).", bullet))
    f.append(P("<b>2. Lawful transmission of medical records in the absence of any prohibitory order.</b>", nbody))
    f.append(P("<b>No prohibitory order exists.</b> There is no written, entered order of this Court prohibiting the transmission, update, or submission of "
               "official medical documentation (including VA Blue Button reports and clinical notes) by electronic mail, by MC-410 filing, or by direct "
               "communication to Department 606. To the contrary, written communication is an accommodation this Court ordered (Tab K).", bullet))
    f.append(P("<b>Full compliance.</b> The communications, filings, and updates containing verified medical and investigative data were made in good faith, "
               "directly support the affirmative defenses of habitability, retaliation, and disability discrimination (Tab A, Streamlined Statement), and "
               "violate no lawful directive of this Court.", bullet))
    f.append(P("<b>3. No basis for a finding of misconduct, malicious intent, or defiance.</b>", nbody))
    f.append(P("<b>Protection of statutory and constitutional rights.</b> Because the acquisition and submission of my own VA medical records is authorized by "
               "rule 1.100, the ADA, the HIPAA right of access (45 C.F.R. \u00a7 164.524), and the evidence-preservation duties that attach once litigation is pending, "
               "no finding of malicious intent, unprofessional conduct, malicious prosecution, sanction, or penalty should be entered against me for making them.", bullet))
    f.append(P("<b>No defiance of the Court.</b> E-mails, evidentiary submissions, and emergency filings transmitted to Department 606 under this framework are "
               "not defiance of any order; they are the medically necessary exercise of a right the Court itself recognized when it ordered written communication.", bullet))
    f.append(P("<b>Good faith.</b> Every step taken in assembling and transmitting this material was directed to securing judicial notice of active federal "
               "investigations, documenting habitability breaches, and defending against an unlawful eviction in Department 606.", bullet))

    f.append(P("III. Conclusion and Prayer for Reasonable Accommodation", nh2))
    f.append(P("Your Honor, I respectfully request that this Court:", nbody))
    f.append(P("1. <b>Grant this request for reasonable accommodation</b>, accepting these emergency submissions and medical records into the record of "
               "Department 606 without penalty or procedural default, and ruling in writing on each pending rule 1.100 request (Tab J; Tab K, Exs. 13\u201320).", bullet))
    f.append(P("2. <b>Find that these submissions were made in good faith</b>, and state on the record that no finding of malicious intent, unprofessional "
               "conduct, or court defiance attaches to them.", bullet))
    f.append(P("3. <b>Protect the health, safety, and procedural rights</b> of this veteran litigant as these matters proceed, including by continuing the "
               "November 2, 2026 trial call or conducting it remotely while the treating physician's restrictions remain in effect (Tab J).", bullet))
    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Opening Statement and Application for Reasonable Accommodation")


if __name__ == "__main__":
    out = os.path.join(TMP, "opening_statement.pdf")
    build(out); print(out)
