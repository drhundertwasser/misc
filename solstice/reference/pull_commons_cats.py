# Pull candidate portraits from curated Wikimedia Commons categories (public domain / CC only).
import os, sys, json, re, time, urllib.request, urllib.parse, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); DL = os.path.join(HERE, "cand"); os.makedirs(DL, exist_ok=True)
UA = {"User-Agent": "solstice-film-reference-board/1.0 (personal research)"}
CATS = [
 ("Portraits by Edward S. Curtis", 14), ("Photographs by Dorothea Lange", 14), ("Photographs by Walker Evans", 10),
 ("Photographs by Lewis Hine", 10), ("Elderly people of Nepal", 6), ("Elderly people of Peru", 6), ("Elderly people of Mongolia", 6),
 ("Elderly people of Morocco", 6), ("Sami people", 6), ("Inuit people", 6), ("Elderly people of Ethiopia", 6), ("Elderly people of India", 6),
 ("Elderly people of Ireland", 6), ("People of the Aran Islands", 6), ("Elderly people of Guatemala", 6), ("Elderly people of Papua New Guinea", 6),
]
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(8*(attempt+1))
    raise RuntimeError("rate limited")
def get(url, path):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(path, "wb") as f: f.write(r.read())
            return True
        except urllib.error.HTTPError as e:
            if e.code != 429: return False
            time.sleep(10*(attempt+1))
    return False
items = []
for cat, n in CATS:
    try:
        d = api(dict(action="query", format="json", list="categorymembers", cmtitle="Category:"+cat, cmtype="file", cmlimit=60))
        titles = [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        titles = [t for t in titles if re.search(r"\.(jpe?g|tiff?|png)$", t, re.I) and not re.search(r"letter|map|landscape|house|building|street|group|crowd", t, re.I)]
        time.sleep(3)
        picked = 0
        for i in range(0, len(titles), 20):
            if picked >= n: break
            d2 = api(dict(action="query", format="json", titles="|".join(titles[i:i+20]), prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=640))
            time.sleep(3)
            for p in d2.get("query", {}).get("pages", {}).values():
                if picked >= n: break
                ii = p.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
                lic = md.get("LicenseShortName", {}).get("value", ""); author = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()[:50]
                if not any(k in lic.lower() for k in ("public domain", "cc0", "cc by", "cc-by", "pd")): continue
                w, h = ii.get("width", 0), ii.get("height", 0)
                if w < 400 or h < 400 or w > 2.2*h: continue           # skip tiny files and wide landscapes
                items.append(dict(title=p["title"].replace("File:", ""), url=ii.get("thumburl") or ii["url"], page=ii.get("descriptionurl"), lic=lic, author=author, cat=cat)); picked += 1
        print(f"{cat}: {picked}", flush=True)
    except Exception as e: print("failed", cat, e, flush=True)
seen = set(); items = [it for it in items if not (it["title"] in seen or seen.add(it["title"]))]
ok = []
for i, it in enumerate(items):
    p = os.path.join(DL, f"c{i:03d}.jpg")
    if get(it["url"], p): it["path"] = p; ok.append(it)
    time.sleep(1.2)
json.dump(ok, open(os.path.join(HERE, "cand_commons.json"), "w"), indent=1)
print(len(ok), "candidates downloaded", flush=True)
