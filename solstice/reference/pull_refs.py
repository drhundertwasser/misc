# Pull public-domain / CC documentary portraits from Wikimedia Commons as a look-reference board.
# Usage: python3 pull_refs.py  -> reference/refs/*.jpg, reference/board_*.jpg, reference/INDEX.md
import os, sys, json, re, urllib.request, urllib.parse, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); DL = os.path.join(HERE, "refs"); os.makedirs(DL, exist_ok=True)
UA = {"User-Agent": "solstice-film-reference-board/1.0 (personal research; contact via github drhundertwasser)"}
QUERIES = [
 # (search terms, how many to take, label)
 ("Dorothea Lange portrait woman face", 5, "Lange"),
 ("Dorothea Lange portrait man face", 4, "Lange"),
 ("Walker Evans portrait face Alabama", 4, "Evans"),
 ("Edward S. Curtis portrait man", 5, "Curtis"),
 ("Edward S. Curtis portrait woman", 4, "Curtis"),
 ("Edward S. Curtis Hopi", 4, "Curtis/Hopi"),
 ("Farm Security Administration child portrait face", 4, "FSA child"),
 ("Aran Islands man portrait", 3, "Ireland"),
 ("Irish farmer old man portrait face", 3, "Ireland"),
 ("old man wrinkled face portrait weathered", 6, "elders"),
 ("old woman wrinkled face portrait", 5, "elders"),
 ("Sami elder portrait face", 3, "Sami"),
 ("Nepal old woman face portrait", 3, "Nepal"),
 ("Quechua elder portrait face Peru", 3, "Andes"),
 ("Bedouin old man portrait face", 3, "Bedouin"),
 ("Mongolian herder portrait face", 3, "Mongolia"),
 ("Inuit elder portrait face", 3, "Inuit"),
 ("Berber woman old portrait face", 3, "Berber"),
]
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            r = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(r, timeout=60) as resp: return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(8 * (attempt + 1))
    raise RuntimeError("rate limited")
def search(q, n):
    d = api(dict(action="query", format="json", generator="search", gsrsearch=q + " filetype:bitmap", gsrnamespace=6, gsrlimit=n*4,
                 prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=800))
    out = []
    for p in d.get("query", {}).get("pages", {}).values():
        ii = p.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", ""); author = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:60]
        ok = any(k in lic.lower() for k in ("public domain", "cc0", "cc by", "cc-by", "pd"))
        if not ok or ii.get("width", 0) < 500 or ii.get("height", 0) < ii.get("width", 0) * 0.5: continue
        out.append(dict(title=p["title"].replace("File:", ""), url=ii.get("thumburl") or ii["url"], page=ii.get("descriptionurl"), lic=lic, author=author))
        if len(out) >= n: break
    return out
def fetch(item, i):
    p = os.path.join(DL, f"{i:03d}.jpg")
    if os.path.exists(p): return p
    for attempt in range(6):
        try:
            r = urllib.request.Request(item["url"], headers=UA)
            with urllib.request.urlopen(r, timeout=120) as resp, open(p, "wb") as f: f.write(resp.read())
            time.sleep(1.0); return p
        except urllib.error.HTTPError as e:
            if e.code != 429: print("download failed", item["title"], e); return None
            time.sleep(10 * (attempt + 1))
    return None
items = []
for q, n, label in QUERIES:
    try:
        res = search(q, n); print(f"{label:>10}: {len(res)} for '{q}'", flush=True)
        for r in res: r["label"] = label; items.append(r)
        time.sleep(3.0)
    except Exception as e: print("search failed", q, e)
# de-duplicate by title
seen = set(); items = [it for it in items if not (it["title"] in seen or seen.add(it["title"]))]
with ThreadPoolExecutor(1) as ex: paths = list(ex.map(lambda a: fetch(*a), [(it, i) for i, it in enumerate(items)]))
from PIL import Image, ImageDraw, ImageFont, ImageOps
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 16)
cw, ch, cols = 400, 400, 6; per = 24
with open(os.path.join(HERE, "INDEX.md"), "w") as idx:
    idx.write("# Reference faces (Wikimedia Commons, public domain / CC)\n\n")
    for b in range(0, len(items), per):
        chunk = items[b:b+per]; rows = (len(chunk)+cols-1)//cols
        sheet = Image.new("RGB", (cw*cols, (ch+40)*rows), (8, 8, 8)); d = ImageDraw.Draw(sheet)
        for j, it in enumerate(chunk):
            i = b + j
            try:
                if not paths[i]: continue
                im = Image.open(paths[i]).convert("RGB"); im = ImageOps.fit(im, (cw, ch), centering=(0.5, 0.35))
            except Exception: continue
            x, y = (j % cols)*cw, (j // cols)*(ch+40); sheet.paste(im, (x, y))
            cap = f"{i:03d} {it['label']} · {it['author'] or '?'} · {it['lic']}"[:52]
            d.text((x+6, y+ch+10), cap, font=f, fill=(220, 220, 220))
            idx.write(f"- **{i:03d}** [{it['title']}]({it['page']}) — {it['author'] or 'unknown'} — {it['lic']} — {it['label']}\n")
        sheet.save(os.path.join(HERE, f"board_{b//per+1}.jpg"), quality=86)
print(len(items), "images;", (len(items)+per-1)//per, "boards")
