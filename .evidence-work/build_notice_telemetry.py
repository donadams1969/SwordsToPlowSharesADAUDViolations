"""
SUPPLEMENTAL NOTICE OF ACTIVE MONITORING, DIGITAL TELEMETRY, AND EVIDENTIARY LOGS (calindex.vercel.app)
Dated November 1, 2026. Opening paper (Tab A) in the San Francisco binder.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_allinone import P, rl, caption, signature, h2, body, TMP, COURT, DEPT

nbody = ParagraphStyle("tlbody", parent=body, fontSize=12.5, leading=18, spaceAfter=8)
nh2 = ParagraphStyle("tlh2", parent=h2, fontSize=15, leading=19, spaceBefore=14, spaceAfter=6)

TITLE = ("SUPPLEMENTAL NOTICE OF ACTIVE MONITORING, DIGITAL TELEMETRY, AND EVIDENTIARY LOGS;<br/>"
         "VERIFICATION OF EXTERNAL ACCESS TO THE LODGED DIGITAL REPOSITORY (CALINDEX.VERCEL.APP)")


def build(path):
    f = caption(TITLE)
    f.append(P(f"TO THE HONORABLE STEPHEN M. MURPHY, {DEPT}, {COURT}, AND COUNSEL OF RECORD:", nbody))
    f.append(P("As part of the continuous evidentiary record and electronically stored information (ESI) logs associated with Case No. CUD-26-682107, "
               "notice is given of the real-time digital telemetry captured from the project analytics dashboard for the lodged digital repository, "
               "calindex.vercel.app (see Notice of Lodgment, Tab A).", nbody))
    f.append(P("I. Telemetry Breakdown and Device Signatures", nh2))
    f.append(P("1. The analytics record captured on November 1, 2026 registers a distinct split in operating systems and device categories accessing "
               "the platform: approximately <b>86 percent mobile (Android)</b>, corresponding to the author's own administrative access from his mobile "
               "device, and approximately <b>14 percent desktop (Windows)</b>, which does not correspond to any device used by the author.", nbody))
    f.append(P("2. The deployment link was distributed solely within the context of this litigation, in the filings and communications served on plaintiff's "
               "counsel and the Court (Evidence Exhibit Binder, Category J). The recorded Windows/desktop access is therefore offered as circumstantial "
               "evidence (Evid. Code, \u00a7\u00a7 600, subd. (b), 1552, 1553) that the served materials have been opened and reviewed by counsel or persons acting "
               "with them, and that the service effected on October 29\u201331, 2026 reached its intended recipients. Defendant does not represent that the "
               "analytics identify any individual; the inference is drawn from the restricted distribution of the link.", nbody))
    f.append(P("II. Integration into the Evidentiary Record", nh2))
    f.append(P("3. The analytics capture (screenshot with the dashboard's own date stamp) is preserved in native form with its SHA-256 hash and will be "
               "lodged with the Court or produced on request. It is incorporated into the ESI tracking logs maintained for this matter, which document the "
               "timeline of review, digital engagement, and administrative oversight surrounding these proceedings, and it supplements the sent-mail "
               "records and read indications already reproduced in the Evidence Exhibit Binder.", nbody))
    f.append(P("4. Defendant will supplement this notice if the telemetry changes materially before trial, and asks that any dispute over the inference "
               "drawn be resolved on the native analytics data rather than on counsel's characterization of it.", nbody))
    f.append(Spacer(1, 6))
    f.extend(signature())
    return rl(f, path, "Supplemental Notice of Digital Telemetry and ESI Logs")


if __name__ == "__main__":
    out = os.path.join(TMP, "notice_telemetry.pdf")
    build(out); print(out)
