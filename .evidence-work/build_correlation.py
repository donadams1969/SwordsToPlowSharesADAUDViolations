"""
Correlation of defendant's medical record to the Vesco / rule 1.100 accommodation proceedings.
Every row pairs a dated entry in the medical record with a dated event in the court record, and cites both.
Nothing here characterizes a diagnosis beyond what the clinician wrote; the connection drawn is defendant's contention.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.lib.units import inch
from reportlab.platypus import Spacer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, grid, h2, small, body, TMP

ADA_FILES = {
    "0806": "20260806_CUD_order_re_ADA_requests.pdf",
    "0814a": "20260814a_CUD_response_to_requests.pdf",
    "0814b": "20260814b_CUD_response_to_requests.pdf",
    "0827": "20260827_CUD_response_to_requests.pdf",
    "0918a": "20260918a_CUD_CCH589086_response_to_0917_request.pdf",
    "0918b": "20260918b_CUD_CCH589086_response_to_0917_request.pdf",
    "0922": "20260922_CUD_response_to_0917_request.pdf",
    "1008a": "20261008a_CCH589728_response_to_1002_request.pdf",
    "1008b": "20261008b_CCH589728_response_to_1006_request.pdf",
    "1014a": "20261014a_CUD_response_to_1009_request.pdf",
    "1014b": "20261014b_CUD_response_to_1009_request.pdf",
}

TITLE = ("CORRELATION OF DEFENDANT'S MEDICAL RECORD TO THE <i>VESCO</i> / RULE 1.100 ACCOMMODATION PROCEEDINGS "
         "\u2013 CONFIDENTIAL (CAL. RULES OF COURT, RULE 1.100(c)(4))")


def build(path, ex):
    """ex maps ADA key -> exhibit number in the Rule 1.100 Orders tab of the same binder."""
    def e(*keys):
        nums = [str(ex[k]) for k in keys if k in ex]
        return ("Rule 1.100 Orders, Ex. " + ", ".join(nums)) if nums else "Rule 1.100 Orders tab"

    f = caption(TITLE)
    f.append(P("<b>Purpose.</b> This table lets the Court and the ADA Coordinator see, date by date, that defendant's accommodation requests and the emergency "
               "access he invokes under <i>Vesco v. Superior Court</i> (2013) 221 Cal.App.4th 275 and rule 1.100 track dated entries in his own medical record. "
               "The left column is what a clinician recorded; the middle column is what happened in the court or accommodation record; the right column is "
               "defendant's contention about why the pairing matters. Defendant does not offer any lay opinion about diagnosis or causation; the clinical "
               "statements are quoted from, or paraphrase, the cited record.", small))
    f.append(P("Part 1. Date-by-date correlation", h2))
    rows = [["Date (2026)", "Medical record (where found)", "Court / accommodation record", "Why the pairing matters (defendant's contention)"]]
    rows += [
        ["Aug. 6", "VA psychiatry progress note: diagnoses and medication list, including complex PTSD and history of TBI (VA Blue Button excerpts, Tab D).",
         f"SF Superior Court Order re ADA Requests, Aug. 6 ({e('0806')}).",
         "A treating psychiatrist documented the conditions on the day the Court ruled on the accommodation requests."],
        ["Aug. 14 - Aug. 27", "VA mental-health secure message of Aug. 19 (VA Blue Button excerpts, Tab D).",
         f"Responses to ADA requests of Aug. 14 (two) and Aug. 27 ({e('0814a', '0814b', '0827')}).",
         "Treatment continued while the Court was answering written requests; the written channel the Court ordered is the only access defendant has used."],
        ["Sept. 17", "VA emergency department social-work and attending notes, Palo Alto VA: records defendant's report that his room was infested with cockroaches, that repeated "
         "complaints were not addressed, and that this distressed him and his service dog; intermittent right-hand paralysis attributed to cervical stenosis (VA Blue Button excerpts, Tab D).",
         f"Accommodation request of Sept. 17 (CUD and CCH-26-589086); responses issued Sept. 18 (two) and Sept. 22 ({e('0918a', '0918b', '0922')}).",
         "Same-day pairing of an emergency-department visit that documents the habitability complaint with a new written accommodation request."],
        ["Oct. 1 - Oct. 8", "VA Homeless Veterans (HCHV) telephone social-work note, Oct. 1 (Tab D).",
         f"Accommodation requests of Oct. 2 and Oct. 6 (CCH-26-589728); responses Oct. 8 ({e('1008a', '1008b')}).",
         "Social-work contact about housing precedes the Oct. 2 and Oct. 6 requests."],
        ["Oct. 6", "VA PCMHI care-management note with PHQ-9 total score of 16 and GAD-7 screening (Tab D).",
         f"Accommodation request of Oct. 6; response Oct. 8 ({e('1008b')}).",
         "A standardized screening result recorded on the date of the request."],
        ["Oct. 9 - Oct. 14", "(No entry in the excerpts.)", f"Request of Oct. 9; responses Oct. 14 ({e('1014a', '1014b')}).",
         "Final written responses before trial; defendant's follow-up requests are pending."],
        ["Oct. 18", "VA wristband print stamps dated 10/18/2026, 11:08-11:09, photographed Oct. 31 (Tab C, Medical Exhibit, photos 5-6).",
         "Between the Oct. 14 responses and the trial call.", "Corroborates a VA clinical encounter in the final two weeks before trial."],
        ["Oct. 27", "Neuropsychological evaluation; results not yet available (stated in the MC-410 Attachment, Tab C).",
         "Trial call Nov. 2 is five days after the evaluation.", "Defendant asks that proceedings await the results or proceed by Zoom."],
        ["Oct. 30", "John Muir Health, Concord Emergency Department: fall; diagnosis acute strain of neck muscle; CT head and CT cervical spine; off work through Nov. 3, return Nov. 4; "
         "follow-up at Travis AFB (David Grant USAF Medical Center) in 2 days (Tab C, Part 1, with wristband photographs).",
         "Evidence notices forwarded to Dept. 606 on Oct. 30; MC-410 prepared for the Nov. 2 trial call (Tab C).",
         "A physician's written work restriction covers the Nov. 2 trial call."],
        ["Oct. 31", "Wristbands still worn (Tab C, photos 5-7).", "Notice to Francisco Torres, Esq., Oct. 31 (Witness List and Subpoenas binder).",
         "Contemporaneous proof of the continuing condition."],
        ["Nov. 1", "VA Blue Button report generated 6:53 a.m.; Travis AFB follow-up directed on or about this date (Tabs D and E; Tab C).",
         "Opening Statement and Application for Reasonable Accommodation and Emergency Judicial Access (Vesco), Nov. 1 (Tab A).",
         "The Vesco application is filed on the date the records were pulled and the follow-up was due."],
        ["Nov. 2 (9:00 a.m.)", "Work restriction in effect through Nov. 3.", "Trial call, Dept. 606.",
         "Defendant asks for Zoom appearance or a continuance until the restrictions are lifted (Tab A; Tab C)."],
    ]
    f.append(grid(rows, [0.8 * inch, 2.1 * inch, 1.85 * inch, 1.75 * inch]))
    f.append(Spacer(1, 10))
    f.append(P("Part 2. Documented conditions and the accommodation each supports", h2))
    f.append(P("The conditions below appear in the VA problem list or in a clinician's note in the excerpts (Tab D). The full report is at Tab E; page numbers refer to its "
               "\"Page n of 215\" footers once located.", small))
    rows2 = [["Condition as recorded", "Where recorded", "Accommodation requested"],
             ["Complex / chronic PTSD; history of traumatic brain injury", "VA psychiatry notes, Aug. 6 and later; problem list (Tab D)",
              "Written communication in place of oral argument; additional time; Zoom attendance; no adverse inference from delay."],
             ["Cervical spinal stenosis with intermittent right-hand paralysis; essential tremor", "ED attending note, Sept. 17; problem list (Tab D)",
              "Written filings by e-mail to Dept. 606; assistive-technology signature; relief from handwritten and in-person requirements."],
             ["Right foot drop; common peroneal neuropathy", "Problem list (Tab D)", "Remote appearance; seating and mobility accommodations if in person."],
             ["Depressive disorder; PHQ-9 of 16 on Oct. 6", "PCMHI note, Oct. 6; problem list (Tab D)", "Breaks, advance notice of hearing dates, and written orders (rule 1.100(e)(2))."],
             ["Acute neck strain after a fall; off work through Nov. 3", "John Muir Health ED, Oct. 30 (Tab C)", "Zoom appearance or continuance of the Nov. 2 trial call and later proceedings."]]
    f.append(grid(rows2, [2.2 * inch, 2.1 * inch, 2.2 * inch]))
    f.append(Spacer(1, 10))
    f.append(P("Part 3. Confidentiality and use", h2))
    f.append(P("Tabs C through E are confidential in part under Cal. Rules of Court, rule 1.100(c)(4) and the Confidentiality of Medical Information Act (Civ. Code, \u00a7 56 et seq.). "
               "They are offered to the Court and the ADA Coordinator only. The full VA report at Tab E contains clinical content unrelated to this action and is to be lodged "
               "conditionally under seal, if at all; the excerpts at Tab D are the pages relied on.", small))
    f += signature()
    return rl(f, path, "Correlation of Medical Record to Vesco Accommodation Proceedings")


if __name__ == "__main__":
    out = os.path.join(TMP, "correlation.pdf"); build(out, {k: i + 1 for i, k in enumerate(ADA_FILES)}); print(out)
