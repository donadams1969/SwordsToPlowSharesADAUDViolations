"""
LEAD MEMORANDUM OF POINTS AND AUTHORITIES - statutory bars, administrative exhaustion, federal grant funds, audit demand.
Dated November 1, 2026. Opening paper (Tab A) in Binder 1.
Contentions are framed as defendant's allegations/contentions; unverified facts are stated on information and belief.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP

mbody = ParagraphStyle("lmbody", parent=body, fontSize=12, leading=16.5, spaceAfter=7)
mh2 = ParagraphStyle("lmh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6, textTransform="uppercase", keepWithNext=1)
mh3 = ParagraphStyle("lmh3", parent=mbody, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4, keepWithNext=1)
mbul = ParagraphStyle("lmbul", parent=mbody, leftIndent=26, firstLineIndent=-14, spaceAfter=5)

TITLE = ("LEAD MEMORANDUM OF POINTS AND AUTHORITIES IN SUPPORT OF EMERGENCY DISMISSAL, MANDATORY AUDIT OF FEDERAL GRANT FUNDS, "
         "AND INJUNCTIVE RELIEF REGARDING FIDUCIARY HYPOCRISY, CONFLICT OF INTEREST, AND UNLAWFUL PROSECUTION BY SWORDS TO PLOWSHARES<br/>"
         "[Related Matters: CCH-26-589086 | CCH-26-589728]")


def bullets(f, items):
    for t in items:
        f.append(P("\u2022&nbsp;&nbsp;" + t, mbul))


def build(path):
    f = caption(TITLE)
    f.append(P("<b>Presiding:</b> Hon. Stephen M. Murphy, Department 606. <b>Trial call:</b> November 2, 2026, 9:00 a.m. "
               "<b>Defendant in pro per:</b> Dr. Donny Gillson, Ed.D. (Donald Ernest Gillson). "
               "<b>Accommodated channel:</b> donny@18fu.ai | (408) 384-1376 (Cal. Rules of Court, rule 1.100).", mbody))

    f.append(P("I. Introduction and Executive Summary: The Dual Role of Swords to Plowshares", mh2))
    f.append(P("Swords to Plowshares holds itself out as a premier veterans' advocacy and rights organization and, on information and belief, is funded in part by "
               "federal, state, and Department of Veterans Affairs (VA) grants. Defendant contends that in that position it owes its own program participant, "
               "Dr. Donny Gillson, Ed.D., a 90% disabled veteran, disabled adult, and California business owner, a duty of loyalty, care, and statutory protection.", mbody))
    f.append(P("Defendant contends that Swords to Plowshares has instead turned on its own beneficiary and is acting at the same time as the landlord seeking "
               "a retaliatory eviction. He contends that it cannot prosecute its own participant; that it may not apply federal grant or HHS contract funds to "
               "finance retaliatory litigation through outside counsel (Zanghi Torres Adams LLP; Cooley LLP); and that the action should be dismissed with prejudice, "
               "or at minimum stayed, and its funding and legal-expenditure records audited. Facts not yet established by documents in Defendant's possession "
               "are pleaded <b>on information and belief</b>, and Defendant asks that the records that would confirm or dispel them be produced.", mbody))

    f.append(P("II. Points and Authorities: Statutory Bars, Jurisdiction, and Mandatory Federal Exhaustion", mh2))

    f.append(P("1. Multiple Statutory Violations Strip Plaintiff of Standing and Oust This Court of Jurisdiction to Proceed", mh3))
    f.append(P("<b>Protected status.</b> Defendant is a 90% disabled veteran, disabled adult, and California business owner managing severe Traumatic Brain Injury (TBI), "
               "Post-Traumatic Stress Disorder (PTSD), Parkinson's disease, and hearing loss. (See Binder 5, confidential medical and VA records, lodged under rule 1.100(c)(4).)", mbody))
    f.append(P("<b>Statutory framework.</b> Defendant contends that continued prosecution of this unlawful detainer violates the following independent state and "
               "federal protections, and that each, separately and together, deprives Plaintiff of standing to proceed and this Court of authority to enter judgment for possession:", mbody))
    bullets(f, [
        "<b>Unruh Civil Rights Act (Civ. Code, \u00a7 51 et seq.).</b> Prohibits arbitrary discrimination, disparate treatment, and disability-based harassment by business establishments, including in housing accommodations, and incorporates violations of the Americans with Disabilities Act (Civ. Code, \u00a7 51, subd. (f)). Defendant contends Plaintiff's refusal to honor his written-communication accommodation, followed by this action, is such discrimination.",
        "<b>Federal Presidio Act and federal enclave and grant protections.</b> Defendant contends that where federal funding, VA oversight, and veteran-housing covenants govern the tenancy, federal law preempts or conditions the state eviction mechanism, and that this action proceeds in disregard of those conditions. The statute relied on is the Presidio Trust Act (Pub. L. No. 104-333, tit. I, \u00a7 101 et seq., codified as a note to 16 U.S.C. \u00a7 460bb), including section 103, which establishes the Presidio Trust and charges it with managing and leasing property within its jurisdiction. Defendant will supply any further pinpoint provisions at or before the hearing and asks that this contention be read as an assertion on information and belief until he does.",
        "<b>Elder and Dependent Adult Civil Protection Act (Welf. &amp; Inst. Code, \u00a7 15600 et seq.).</b> Protects dependent adults from financial, physical, and psychological abuse, including bad-faith intimidation and retaliatory displacement. Defendant contends that pursuing his removal while on notice of his cognitive and medical disabilities falls within the conduct the Act addresses.",
        "<b>Short-Doyle Act (as superseded by the Bronzan-McCorquodale Act, Welf. &amp; Inst. Code, \u00a7 5600 et seq.) and fiduciary protections.</b> To the extent Plaintiff's services to Defendant are tied to state-funded community mental-health or supportive-housing programs, Defendant invokes these provisions, and the general law of fiduciary duty, for the principle that an entity entrusted with veteran welfare is accountable as a fiduciary and may not engage in self-dealing or litigate adversely to the beneficiary it serves. Defendant refers to this as the \"Doyle Act\" in earlier filings; he will lodge, with the Court's leave, the specific provisions relied upon.",
    ])
    f.append(P("Defendant also relies on Civil Code section 1942.5 (retaliatory eviction) and the Fair Employment and Housing Act (Gov. Code, \u00a7 12900 et seq.) and the Fair Housing Act (42 U.S.C. \u00a7 3604(f)), as set out in the Streamlined Statement of the Case (Binder 1, Tab D).", mbody))

    f.append(P("2. Malicious Prosecution and Judicial and Administrative Overreach", mh3))
    f.append(P("<b>Standard.</b> A civil action brought without probable cause and with malice, and terminated in the defendant's favor, supports a claim for malicious prosecution. "
               "(<i>Sheldon Appel Co. v. Albert &amp; Oliver</i> (1989) 47 Cal.3d 863, 871.) Defendant contends that pressing an eviction in the face of the statutory bars above, "
               "pending federal administrative review, and documented disability discrimination is the kind of proceeding that doctrine addresses, and reserves that claim.", mbody))
    f.append(P("<b>Application.</b> Defendant contends that forcing trial in the face of the Rule 1.100 accommodation orders, the pending exhaustion described below, "
               "and the October 30, 2026 emergency-department record would penalize him for his disabilities and constitute overreach. He asks the Court to decide the "
               "accommodation and continuance requests before reaching the merits.", mbody))

    f.append(P("3. Mandatory Pre-Litigation Administrative Exhaustion and Federal Oversight", mh3))
    f.append(P("<b>Contention.</b> Defendant contends that, before an eviction involving federally funded veteran housing may lawfully proceed, the following administrative grievances "
               "and regulatory reviews must be completed, and that each remains pending:", mbody))
    bullets(f, [
        "<b>VA Office of Inspector General (OIG) and VA Regional Office (Oakland):</b> formal grievances concerning breach of veteran-welfare obligations and misuse of grant funds.",
        "<b>U.S. Department of Housing and Urban Development (HUD) OIG:</b> investigation of federal grant violations and housing discrimination.",
        "<b>VA Office of General Counsel (OGC):</b> review of the veteran service organization's fiduciary compliance and conflict of interest.",
        "<b>Federal grant-oversight bodies</b> responsible for the HHS, VA, and HUD awards under which Plaintiff operates.",
    ])
    f.append(P("<b>Consequence.</b> Because those reviews are unexhausted, Defendant contends this Court should not proceed with the unlawful detainer, and that "
               "the action should be dismissed or, at minimum, <b>stayed</b> until the reviews are complete. Defendant acknowledges that the Court cannot itself direct "
               "a federal agency; he asks only that the Court not enter judgment against a disabled veteran while those agencies have the underlying questions before them. Defendant recognizes that a superior court has general jurisdiction over unlawful detainer (Code Civ. Proc., \u00a7 1161 et seq.); his primary request is therefore a stay under the doctrine of primary jurisdiction, with dismissal sought on the statutory grounds above.", mbody))

    f.append(P("4. Federal Grant Money and HHS Contracts May Not Finance Retaliatory Litigation", mh3))
    f.append(P("<b>Authority.</b> Federal awards are governed by the Uniform Guidance, 2 C.F.R. part 200. Section 200.403 requires that costs charged to an award be necessary, "
               "reasonable, and allocable to it, and section 200.435 addresses the allowability of the costs of civil proceedings. HHS and VA awards, including "
               "housing awards, also carry program-specific terms and participant-protection conditions. (2 C.F.R. \u00a7\u00a7 200.403, 200.405, 200.435.)", mbody))
    f.append(P("<b>Contention.</b> Federal grants, HHS contracts (including funding structures Defendant understands to extend through 2027), and VA appropriations are earmarked "
               "for veteran support, housing stability, medical advocacy, and social services. Defendant contends such funds may not lawfully be diverted to retain outside "
               "counsel or to prosecute a retaliatory eviction against a program participant. Defendant does not presently know whether any federal funds or staff "
               "time paid from them were applied to this litigation; that is the question he asks to have answered.", mbody))
    f.append(P("<b>Demand for forensic audit.</b> Defendant formally demands a comprehensive independent audit of Swords to Plowshares' HHS contracts, VA funding allocations, "
               "and legal-expenditure ledgers for this matter, including the fee arrangements with Zanghi Torres Adams LLP and Cooley LLP. Because those records are in "
               "Plaintiff's and its funders' hands, Defendant requests production by order or through the subpoenas lodged at Binder 3, and, in the alternative, that the "
               "Court note the issue for referral to the awarding agencies' Offices of Inspector General, whose audit authority the Court does not have.", mbody))

    f.append(P("5. Response to the \"Weaponization\" Accusation and Protection of ADA Rights", mh3))
    f.append(P("Opposing counsel and management have alleged that Defendant is \"weaponizing\" the ADA, his medical records, or assistive technology. Invoking the Americans with "
               "Disabilities Act and rule 1.100, lodging contemporaneous medical evidence (John Muir Health Concord Emergency Department record of October 30, 2026; VA treatment "
               "records; see Binder 5), and using assistive technology to communicate are the exercise of federally protected civil rights, not misconduct. Defendant "
               "lodged the medical material in confidence under rule 1.100(c)(4) and has placed it before the Court only to the extent needed to support the accommodation, "
               "continuance, and remote-appearance requests (MC-410).", mbody))

    f.append(P("III. PRAYER FOR RELIEF AND REQUESTED ORDERS", mh2))
    f.append(P("Defendant Dr. Donny Gillson, Ed.D. respectfully requests that Department 606 enter orders:", mbody))
    for n, t in enumerate([
        "<b>DISMISSING</b> Unlawful Detainer Case No. CUD-26-682107 <b>with prejudice</b> for lack of standing and on the grounds of the Unruh Civil Rights Act, the Elder and Dependent Adult Civil Protection Act, the Short-Doyle/Bronzan-McCorquodale Act, and the Presidio Trust Act, together with retaliatory eviction under Civil Code section 1942.5;",
        "<b>STAYING</b> all proceedings, in the alternative, pending completion of administrative review before the VA Regional Office (Oakland), VA OIG, VA OGC, HUD OIG, and the federal grant-oversight bodies identified above;",
        "<b>ORDERING</b> production, on an order shortening time or through the lodged subpoenas, of Swords to Plowshares' federal, state, and VA funding agreements and legal-expenditure ledgers and fee agreements for this action, and an independent forensic audit of Swords to Plowshares, Cooley LLP, and associated legal billing to determine whether federal grant funds or 2027 HHS contract allocations were applied to this litigation; in the alternative, noting the issue for referral to the appropriate Offices of Inspector General;",
        "<b>ENJOINING</b> further adverse action against Defendant in this matter pending the Court's ruling on the foregoing and on the Rule 1.100 accommodation requests; and",
        "<b>AWARDING</b> costs and such statutory damages, sanctions (including under Code Civ. Proc., \u00a7\u00a7 128.5 and 128.7), and equitable relief as the Court finds warranted for retaliation, civil-rights violations, and the conduct described above, reserving Defendant's claim for malicious prosecution.",
    ], 1):
        f.append(P(f"{n}. {t}", mbody))

    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Lead Memorandum of Points and Authorities - Statutory Bars, Exhaustion, Federal Funding Audit")


if __name__ == "__main__":
    out = os.path.join(TMP, "lead_memo.pdf")
    build(out); print(out)
