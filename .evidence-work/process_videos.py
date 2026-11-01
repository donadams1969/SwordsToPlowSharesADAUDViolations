"""Hash, probe, and extract a still frame from each downloaded recording; stage files by exhibit number."""
import os, sys, json, hashlib, shutil, re
sys.path.insert(0, "/tmp/avlib"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import av
from PIL import Image
from notices import NOTICES

SRC = "/tmp/vid"; OUT = "/tmp/b4"; VDIR = os.path.join(OUT, "Binder4_Videos"); STILLS = os.path.join(OUT, "stills")
os.makedirs(VDIR, exist_ok=True); os.makedirs(STILLS, exist_ok=True)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


manifest, by_hash = [], {}
for si in (0, 1):
    for code, title, url, desc in NOTICES[si]["videos"]:
        ex = f"V{si+1}-{code.split('-')[1]}"; src = os.path.join(SRC, f"S{si+1}-{code}.bin")
        rec = {"exhibit": ex, "suite": si + 1, "code": code, "title": title, "url": url, "desc": desc,
               "drive_id": re.search(r"/d/([^/]+)/", url).group(1), "bytes": os.path.getsize(src), "sha256": sha256(src)}
        if rec["sha256"] in by_hash:
            rec.update(kind="duplicate", duplicate_of=by_hash[rec["sha256"]], filename=None)
            manifest.append(rec); print(ex, "duplicate of", rec["duplicate_of"]); continue
        by_hash[rec["sha256"]] = ex
        with open(src, "rb") as f:
            head = f.read(4)
        if head[:2] == b"\xff\xd8":
            ext = "jpg"; im = Image.open(src); rec.update(kind="image", width=im.width, height=im.height, duration=None, created=None)
            exif = im.getexif(); rec["created"] = (exif.get(306) or "").replace(":", "-", 2) or None
            im.convert("RGB").save(os.path.join(STILLS, ex + ".jpg"), quality=92, subsampling=0); rec["still"] = True
        else:
            c = av.open(src); md = c.metadata
            ext = "3gp" if "3gp" in md.get("major_brand", "") else "mp4"
            vs = [s for s in c.streams if s.type == "video"]
            rec.update(kind="video" if vs else "audio", duration=c.duration / 1e6, created=md.get("creation_time"),
                       utc_offset=md.get("com.samsung.android.utc_offset"), brand=md.get("major_brand"))
            if vs:
                v = vs[0]; rec.update(width=v.codec_context.width, height=v.codec_context.height, codec=v.codec_context.name)
                target = int(min(5.0, c.duration / 1e6 * 0.05) * 1e6)
                c.seek(target, backward=True)
                for fr in c.decode(video=0):
                    if fr.time is None or fr.time * 1e6 >= target - 5e5 or True:
                        fr.to_image().save(os.path.join(STILLS, ex + ".jpg"), quality=92, subsampling=0); rec["still"] = True
                        rec["still_at"] = fr.time; break
            c.close()
        fn = f"{ex}.{ext}"; shutil.copy2(src, os.path.join(VDIR, fn)); rec["filename"] = fn
        manifest.append(rec); print(ex, rec["kind"], fn, round(rec.get("duration") or 0, 1), rec["sha256"][:12])
json.dump(manifest, open(os.path.join(OUT, "video_manifest.json"), "w"), indent=1)
print("done", len(manifest))
