import os, json, hashlib
from PIL import Image, ExifTags, ImageOps, ImageDraw, ImageFont

SRC = os.path.join(os.path.dirname(__file__), "src")
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg"))

TAGS = {v: k for k, v in ExifTags.TAGS.items()}
GPS = ExifTags.GPSTAGS

def dms(v, ref):
    try:
        d = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
        return -d if ref in ("S", "W") else d
    except Exception:
        return None

meta = []
for f in files:
    p = os.path.join(SRC, f)
    rec = {"file": f, "bytes": os.path.getsize(p)}
    with open(p, "rb") as fh:
        rec["sha256"] = hashlib.sha256(fh.read()).hexdigest()
    im = Image.open(p)
    rec["size"] = im.size
    ex = im.getexif()
    rec["make"] = str(ex.get(TAGS["Make"], "")).strip()
    rec["model"] = str(ex.get(TAGS["Model"], "")).strip()
    rec["software"] = str(ex.get(TAGS["Software"], "")).strip()
    rec["datetime"] = str(ex.get(TAGS["DateTime"], "")).strip()
    ifd = ex.get_ifd(0x8769)
    rec["original"] = str(ifd.get(TAGS["DateTimeOriginal"], "")).strip()
    rec["digitized"] = str(ifd.get(TAGS["DateTimeDigitized"], "")).strip()
    rec["offset"] = str(ifd.get(0x9011, "")).strip()
    g = ex.get_ifd(0x8825)
    if g:
        lat = dms(g.get(2), g.get(1)); lon = dms(g.get(4), g.get(3))
        if lat is not None and lon is not None:
            rec["gps"] = [round(lat, 6), round(lon, 6)]
    meta.append(rec)

with open(os.path.join(os.path.dirname(__file__), "meta.json"), "w") as fh:
    json.dump(meta, fh, indent=1)

# contact sheets: 12 per sheet, 4 x 3, labelled by index
os.makedirs(os.path.join(os.path.dirname(__file__), "sheets"), exist_ok=True)
font = ImageFont.load_default()
TW, TH = 300, 400
for s in range(0, len(files), 12):
    sheet = Image.new("RGB", (TW * 4, (TH + 24) * 3), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files[s:s + 12]):
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f)))
        im.thumbnail((TW, TH))
        x = (i % 4) * TW; y = (i // 4) * (TH + 24)
        sheet.paste(im, (x + (TW - im.width) // 2, y + 24 + (TH - im.height) // 2))
        d.text((x + 4, y + 4), f"[{s + i}] {f}", fill="black", font=font)
    sheet.save(os.path.join(os.path.dirname(__file__), "sheets", f"sheet{s // 12}.jpg"), quality=80)

for i, r in enumerate(meta):
    print(i, r["file"], r["original"] or r["datetime"] or "-", r["model"], r["size"], r.get("gps", ""))
