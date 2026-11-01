"""
LEAD OPENING STATEMENT AND SYSTEMIC DOSSIER - willful blindness, institutional funding compliance, pretextual nuisance.
Dated November 1, 2026. Companion to the Lead Memorandum (Tab A).
An opening statement is argument, not evidence: contentions are framed as what Defendant expects the evidence to show,
and facts not yet confirmed by documents are stated on information and belief.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP

obody = ParagraphStyle("osbody", parent=body, fontSize=12, leading=16.5, spaceAfter=7)
oh2 = ParagraphStyle("osh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6, textTransform="uppercase", keepWithNext=1)
obul = ParagraphStyle("osbul", parent=obody, leftIndent=26, firstLineIndent=-14, spaceAfter=5)

TITLE = ("LEAD OPENING STATEMENT AND SYSTEMIC DOSSIER: WILLFUL BLINDNESS, INSTITUTIONAL FUNDING-COMPLIANCE FAILURES, "
         "AND A RETALIATORY EVICTION PRESENTED AS NUISANCE<br/>[Related Matters: CCH-26-589086 | CCH-26-589728]")


def bullets(f, items):
    for t in items:
        f.append(P("\u2022&nbsp;&nbsp;" + t, obul))


def build(path):
    f = caption(TITLE)
    f.append(P("<b>Presiding:</b> Hon. Stephen M. Murphy, Department 606. <b>Trial call:</b> November 2, 2026, 9:00 a.m. "
               "<b>Defendant in pro per:</b> Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson). "
               "<b>Accommodated channel:</b> donny@18fu.ai | (408) 384-1376 (Cal. Rules of Court, rule 1.100).", obody))

    f.append(P("I. Introduction: The Inversion of \u201cNuisance\u201d", oh2))
    f.append(P("Plaintiff presents this case as a routine summary proceeding, an unlawful detainer resting on a notice alleging nuisance. "
               "Defendant will show that it is neither routine nor about nuisance. He expects the evidence to show that the nuisance notice "
               "followed, and is a response to, his written requests for reasonable accommodation and his administrative grievances about "
               "supportive-housing services and federal funding compliance.", obody))
    f.append(P("Defendant contends that Plaintiff and its counsel have been given documentary notice of those concerns and have chosen to litigate possession "
               "rather than answer them. Defendant does not ask the Court to accept that contention on his say-so. He asks the Court to hold Plaintiff "
               "to its burden, to receive the records lodged in his trial binder, and to decide whether the stated ground for eviction is the real one. "
               "Where a fact depends on records only Plaintiff holds, Defendant states it on <b>information and belief</b> and asks that the records be produced.", obody))
    f.append(P("This Court is asked to decide possession of a unit. Defendant asks it to decide that question on the whole record, including the context in which the notice issued.", obody))

    f.append(P("II. Willful Blindness: The Legal Frame", oh2))
    f.append(P("Courts treat deliberate ignorance as the equivalent of knowledge. Under the federal formulation, a party is willfully blind when it "
               "(1) subjectively believes there is a high probability that a fact exists and (2) takes deliberate actions to avoid learning of it. "
               "(<i>Global-Tech Appliances, Inc. v. SEB S.A.</i> (2011) 563 U.S. 754, 769.) Negligence or carelessness does not meet that standard, and "
               "Defendant does not argue that it does. What he asks the Court to examine is whether the evidence shows awareness followed by deliberate avoidance.", obody))
    f.append(P("Defendant expects the evidence to show three things:", obody))
    bullets(f, [
        "<b>Notice.</b> The concerns raised in this case were transmitted in writing, over time, to Plaintiff, its counsel, the VA Regional Office (Oakland), "
        "and the HUD Office of Inspector General. The transmittals and dates are in the trial binder. Defendant will establish receipt through the documents and, where needed, by subpoena and testimony.",
        "<b>No substantive response.</b> Defendant contends that, rather than addressing the accommodation requests, the program-services complaints, or the funding questions "
        "on the merits, Plaintiff served a nuisance notice and filed this action. Defendant will point the Court to the sequence and timing of those events.",
        "<b>Timing.</b> Defendant contends the action was filed ahead of the federal reviews and audit demands he has pursued, including the demand relating to 2027 HHS contract funding, "
        "and that this sequence is circumstantial evidence of retaliatory purpose. Civil Code section 1942.5 prohibits retaliation against a tenant for exercising legal rights, and Defendant will rely on it.",
    ])

    f.append(P("III. Swords to Plowshares: Funding, Supply of Services, and Systemic Failure", oh2))
    f.append(P("Plaintiff holds itself out as a primary conduit for veteran housing, supportive services, and publicly funded programs. "
               "On information and belief, those programs are funded in part by federal awards subject to the Uniform Guidance, title 2 of the Code of Federal Regulations, part 200. "
               "Defendant contends as follows, and will ask that the funding agreements, program files, and ledgers be produced so the contentions can be tested:", obody))
    bullets(f, [
        "<b>Cost principles.</b> Federal awards are subject to allowability and allocability rules (2 C.F.R. \u00a7\u00a7 200.403, 200.405), and section 200.435 separately governs when the costs of "
        "defending or prosecuting civil proceedings may be charged to an award. Defendant asks whether, and how, the cost of this litigation, including fees paid to outside counsel, is being recorded and funded. "
        "He does not assert that funds were misapplied; he asserts that the records needed to answer the question are in Plaintiff's hands and have not been provided.",
        "<b>Delivery of supportive services.</b> Defendant contends that the supportive-housing services owed to him as a participant were not delivered as represented, "
        "and that his written requests for reasonable accommodation of his documented disabilities, which are protected under the Unruh Civil Rights Act (Civ. Code, \u00a7 51 et seq.) "
        "and the Fair Employment and Housing Act (Gov. Code, \u00a7 12900 et seq.), were not meaningfully engaged. (See Binder 5, confidential medical and VA records, lodged under rule 1.100(c)(4).)",
        "<b>Eviction as the response.</b> Defendant contends that when he asked for accountability, the response was eviction. If the evidence shows that, a nuisance label cannot "
        "separate the eviction from its cause.",
    ])

    f.append(P("IV. The Real Nuisance Question", oh2))
    f.append(P("A disabled veteran's accommodation requests, administrative grievances, and requests for regulatory review are protected activity. They are not a nuisance. "
               "Defendant asks the Court to consider the following when it weighs Plaintiff's stated ground:", obody))
    bullets(f, [
        "<b>Use of the summary process.</b> Whether an unlawful detainer, with its shortened timelines, is being used to resolve a possession question that is entangled with unresolved federal "
        "administrative reviews and with Defendant's retaliation and discrimination defenses.",
        "<b>Duties to a program participant.</b> Whether an organization that serves veterans and is funded to do so can, consistent with its obligations and its public mission, "
        "bring an eviction against a participant who has asked for accountability, without first addressing the accommodation and services issues he raised.",
        "<b>The record behind the label.</b> Whether the incidents described in the nuisance notice are supported by admissible evidence, or whether the notice rests on characterizations of conduct "
        "that is, in fact, disability-related behavior or the exercise of protected rights.",
    ])

    f.append(P("V. Why a Stay Is Warranted", oh2))
    f.append(P("Defendant has also pursued review through the VA Regional Office (Oakland), the VA and HUD Offices of Inspector General, and the VA Office of General Counsel. "
               "Under the doctrine of primary jurisdiction, a court may stay or defer a proceeding so that an agency with special competence can address issues within its expertise. "
               "(See <i>Farmers Ins. Exchange v. Superior Court</i> (1992) 2 Cal.4th 377, 391-393.) "
               "Defendant asks for a stay on that basis, and in the alternative asks that the Court rule on the funding-records and accommodation questions before it proceeds to trial on possession.", obody))
    f.append(P("<b>Candor to the Court.</b> Defendant is a self-represented litigant managing documented cognitive and neurological disabilities. "
               "Defendant acknowledges that some of the federal-program and exhaustion contentions raise questions of law that the Court will decide, "
               "and that an opening statement is not evidence. He will offer the exhibits and testimony described above and asks that the Court apply the rule 1.100 accommodations "
               "in receiving them.", obody))

    f.append(P("VI. Prayer / Requested Relief", oh2))
    f.append(P("Defendant respectfully requests that Department 606:", obody))
    for n, t in enumerate([
        "<b>CONSIDER</b> the full record, including the sequence of Defendant's accommodation requests and grievances and Plaintiff's nuisance notice, in determining whether the stated ground for eviction is the actual ground or a retaliatory pretext under Civil Code section 1942.5;",
        "<b>STAY</b> these proceedings, under the doctrine of primary jurisdiction, pending completion of review by the VA Regional Office (Oakland), the VA and HUD Offices of Inspector General, and the pending federal audit and oversight processes, or in the alternative set the funding and accommodation issues for determination before trial on possession;",
        "<b>DIRECT</b> Plaintiff to produce, or to respond to the lodged subpoenas for, the funding agreements, program and service records, accommodation-request files, and legal-expenditure and fee records identified in Defendant's papers, and to address the documentary evidence on the merits; and",
        "<b>GRANT</b> such further relief, including any dismissal, costs, and sanctions the Court finds warranted under Code of Civil Procedure sections 128.5 and 128.7, as the record supports.",
    ], 1):
        f.append(P(f"{n}. {t}", obody))

    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Lead Opening Statement and Systemic Dossier - Willful Blindness and Retaliatory Eviction")


if __name__ == "__main__":
    out = os.path.join(TMP, "lead_opening_statement.pdf")
    build(out); print(out)
