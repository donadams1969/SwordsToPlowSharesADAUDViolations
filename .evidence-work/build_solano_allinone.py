"""Solano County all-in-one accommodation binder (separate from the San Francisco trial binder).
Reuses the 1-inch-margin, wrapped-cell layout from build_allinone.py."""
import os, warnings
warnings.filterwarnings("ignore")
import fitz
from reportlab.lib.units import inch
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle

import build_allinone as A
from build_allinone import P, rl, h1, cen, small, grid, assemble, merge, TMP, ART, COMP, NAME, ADDR1, ADDR2, PHONE, EMAIL, DATED
from build_binders import make_mc410, medical_exhibit, ADA_EXHIBITS, compress_scans

A.PREFIX = "GSB"
OUT = os.path.join(ART, "Gillson_Solano_All_In_One_Accommodation_Binder.pdf")
HERE = os.path.dirname(os.path.abspath(__file__))


def cover(path):
    f = [Spacer(1, 1.3 * inch), P("ALL-IN-ONE ACCOMMODATION BINDER", ParagraphStyle("big", parent=h1, fontSize=24, leading=32)),
         P("Solano County", ParagraphStyle("sub", parent=cen, fontSize=14, leading=22)), Spacer(1, 24),
         P("<i>Gillson v. Landrum, Torres &amp; Zanghi</i>", ParagraphStyle("c1", parent=cen, fontSize=13, leading=22)),
         P("Petition for Civil Harassment Restraining Orders (Code Civ. Proc., § 527.6)", cen),
         P("Superior Court of California, County of Solano", cen), P("Case No. ______________ – Dept. ______", cen), Spacer(1, 30),
         P(f"Submitted by {NAME}, Petitioner in propria persona", cen), P(f"{ADDR1}, {ADDR2}", cen), P(f"{PHONE} | {EMAIL}", cen), Spacer(1, 30),
         P("Tab A is filed with the petition. Tab B is delivered to the Court's ADA Coordinator; Attachment Item 5 and the confidential medical exhibit "
           "are confidential under California Rules of Court, rule 1.100(c)(4). Tab C contains the twenty San Francisco Superior Court rule 1.100 orders "
           "and responses referenced in the application. The San Francisco trial binder (CUD-26-682107) is maintained separately.", small),
         Spacer(1, 10), P(f"Prepared {DATED}", cen)]
    return rl(f, path, "Cover")


if __name__ == "__main__":
    med_ex = medical_exhibit(os.path.join(TMP, "medical_exhibit.pdf"))
    mc_sol = make_mc410("solano", "Solano", "600 Union Avenue", "Fairfield, CA 94533", "(to be assigned)",
                        "Superior Court of California, County of Solano – Civil Harassment (Code Civ. Proc., § 527.6)",
                        ["I am under medical orders to rest: on October 30, 2026 the John Muir Health Concord Emergency Department placed me off work through November 3, 2026 (return no earlier than November 4) after a fall, with directed follow-up at Travis Air Force Base on or about November 1, 2026, where an extension of approximately two weeks is anticipated. I ask to appear by Zoom at every hearing in this matter until those orders are lifted. The emergency department record is attached as a confidential exhibit."],
                        "First hearing on the petition (date to be set) and all further hearings.", "Petitioner", "Civil harassment (CCP 527.6)", "Hearing on petition (date to be set) and all further hearings.")
    mcsp = merge(mc_sol, os.path.join(TMP, "sol_mc_merged.pdf"))
    ada_items = [(f"Ex. {i+1}. {lab}", os.path.join(HERE, "ada", fn)) for i, (fn, lab) in enumerate(ADA_EXHIBITS)]
    sections = [
        ("A", "Ex Parte Application for Order Shortening Time; Rule 1.100 Request; Memorandum; Declaration; [Proposed] Order",
         [("Application, Memorandum, Declaration, Proposed Order, and Routing Note", os.path.join(COMP, "Gillson_Solano_OST_and_Accommodation_Request.pdf"))]),
        ("B", "Request for Accommodations – MC-410 (Solano County) – CONFIDENTIAL IN PART",
         [("MC-410 with Attachment (Items 3–5)", mcsp),
          ("CONFIDENTIAL Exhibit – John Muir Health ED record (Oct. 30, 2026) and wristband photographs", med_ex)]),
        ("C", "San Francisco Superior Court Rule 1.100 Orders and Responses (July–October 2026)", ada_items),
    ]
    cov = cover(os.path.join(TMP, "sol_cover.pdf"))
    n = assemble(OUT, cov, sections, "Gillson – Solano All-in-One Accommodation Binder – Confidential in part (CRC 1.100(c)(4))")
    print("pages", n)
    compress_scans(OUT)
    old = os.path.join(ART, "Gillson_Solano_Accommodation_Binder.pdf")
    if os.path.exists(old):
        os.remove(old)
