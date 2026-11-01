"""Exports the Notice and Integrated Statement content to lib/case-data.json for the website."""
import os, re, json, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_integrated as I
import build_notice as N
import build_brief as B
import build_mil as M

TAG = re.compile(r"<[^>]+>")


def clean(t):
    return TAG.sub("", t).replace("&amp;", "&").replace("&apos;", "'")


def convert(content):
    out = []
    for item in content:
        k = item[0]
        if k in ("d", "o"): k = "n"
        if k in ("h2", "h3", "p", "n", "phase", "box"):
            out.append({"type": k, "text": clean(item[1])})
        elif k == "fig":
            out.append({"type": "fig", "key": item[1]})
        elif k == "chk":
            out.append({"type": "chk", "shows": clean(item[1]), "omits": clean(item[2]), "asked": clean(item[3])})
        elif k == "table":
            out.append({"type": "table", "rows": [[clean(c) for c in r] for r in item[1]]})
    return out


figs = {key: {"src": f"/figures/{key}.png", "caption": clean(cap), "page": page} for key, _, page, _, cap in I.FIGS}
data = {"figures": figs, "statement": convert(I.CONTENT), "notice": convert(N.CONTENT), "noticeTitle": [clean(t) for t in N.TITLE], "motion": convert(M.CONTENT), "motionTitle": [clean(t) for t in M.TITLE], "brief": convert(B.CONTENT), "briefTitle": [clean(t) for t in B.TITLE]}
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(root, "lib"), exist_ok=True)
with open(os.path.join(root, "lib", "case-data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("statement blocks", len(data["statement"]), "notice blocks", len(data["notice"]))
