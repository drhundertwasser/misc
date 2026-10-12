# Pull indigenous-portrait candidates from verified Commons categories (PD/CC only). Adapted from pull_commons_cats.py.
# usage: python3 pull_indigenous_cats.py [plan.json] [out_dir] [cand_json]   (defaults: built-in PLAN, indigenous/cand, indigenous/cand_commons.json)
# Category names below were verified with list=search ns=14 on 2026-10-12. Run only when no other Commons job shares this IP.
import os, sys, json, re, time, urllib.request, urllib.parse, urllib.error
UA = {"User-Agent": "solstice-film-reference-board/1.0 (personal research)"}
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = json.loads("""[
 {"society":"Hopi/Pueblo","cat":"Hopi people","n":6,"limit":80},
 {"society":"Navajo/Apache","cat":"Navajo people","n":5,"limit":80},
 {"society":"Navajo/Apache","cat":"Apache people","n":4,"limit":80},
 {"society":"Inuit/Yupik","cat":"Inuit people","n":6,"limit":80},
 {"society":"Sami","cat":"Sami people","n":6,"limit":80},
 {"society":"Quechua/Aymara","cat":"Quechua people","n":5,"limit":80},
 {"society":"Quechua/Aymara","cat":"Aymara people","n":4,"limit":80},
 {"society":"Mapuche","cat":"Mapuche people","n":6,"limit":80},
 {"society":"PNG highlanders","cat":"Huli people","n":6,"limit":80},
 {"society":"Maasai/Himba","cat":"Maasai","n":4,"limit":80},
 {"society":"Maasai/Himba","cat":"Himba","n":4,"limit":80},
 {"society":"Tuareg/Berber","cat":"Tuareg people","n":6,"limit":80},
 {"society":"Bedouin","cat":"Bedouins","n":6,"limit":80},
 {"society":"Kalash","cat":"Kalash people","n":6,"limit":80},
 {"society":"Mongolian/Kazakh","cat":"People of Mongolia","n":6,"limit":80},
 {"society":"Ainu","cat":"Ainu people","n":6,"limit":80},
 {"society":"Tibetan/Nepali","cat":"Tibetan people","n":6,"limit":80},
 {"society":"Amazonian","cat":"Yanomami","n":6,"limit":80},
 {"society":"Siberian","cat":"Nenets people","n":4,"limit":80},
 {"society":"Siberian","cat":"Chukchi people","n":4,"limit":80},
 {"society":"Aboriginal Australians","cat":"Aboriginal Australians","n":6,"limit":80}
]
""")
plan = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else PLAN
DL = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "indigenous", "cand")
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "indigenous", "cand_commons.json")
os.makedirs(DL, exist_ok=True)
existing = json.load(open(OUT)) if os.path.exists(OUT) else []
seen_titles = {it["title"] for it in existing}
start_idx = max([int(re.search(r"c(\d+)", it["path"]).group(1)) for it in existing], default=-1) + 1
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            ra = e.headers.get("Retry-After"); s = min(60, int(ra)) if ra and ra.isdigit() else min(60, 10*(attempt+1))
            print("API 429 retry-after", ra, "sleep", s, flush=True); time.sleep(s)
    raise RuntimeError("rate limited")
def get(url, path):
    for attempt in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(path, "wb") as f: f.write(r.read())
            return True
        except urllib.error.HTTPError as e:
            if e.code != 429: print("HTTP", e.code, url, flush=True); return False
            s = min(60, 10*(attempt+1)); print("DL 429, sleep", s, flush=True); time.sleep(s)
        except Exception as e:
            print("DL error", e, flush=True); time.sleep(5)
    return False
BAD = r"letter|map\b|landscape|house|building|street|crowd|flag|coin|stamp|drawing|painting|sketch|engraving|lithograph|illustration|poster|book|page|cover|logo|chart|diagram|aerial|village view|panorama|sign\b|text|manuscript|card\b|postcard|statue|sculpture|museum|exhibit|dance performance|parade|stadium"
items = []
for entry in plan:
    soc, cat, n = entry["society"], entry["cat"], entry.get("n", 10)
    skip = entry.get("skip", "")
    try:
        d = api(dict(action="query", format="json", list="categorymembers", cmtitle="Category:"+cat, cmtype="file", cmlimit=entry.get("limit", 120)))
        mem = d.get("query", {}).get("categorymembers", [])
        titles = [m["title"] for m in mem]
        titles = [t for t in titles if re.search(r"\.(jpe?g|tiff?|png)$", t, re.I) and not re.search(BAD, t, re.I) and not (skip and re.search(skip, t, re.I))]
        titles = [t for t in titles if t.replace("File:", "") not in seen_titles]
        print(f"[{soc}] {cat}: {len(mem)} members, {len(titles)} after filter", flush=True)
        time.sleep(5.0)
        picked = 0
        for i in range(0, len(titles), 25):
            if picked >= n: break
            d2 = api(dict(action="query", format="json", titles="|".join(titles[i:i+25]), prop="imageinfo", iiprop="url|extmetadata|size|mime", iiurlwidth=640))
            time.sleep(5.0)
            for p in d2.get("query", {}).get("pages", {}).values():
                if picked >= n: break
                ii = p.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
                lic = md.get("LicenseShortName", {}).get("value", ""); author = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()[:80]
                ll = lic.lower()
                if not any(k in ll for k in ("public domain", "cc0", "cc by", "cc-by", "pd")) or "nc" in ll.replace("cc by", "") and "cc by-nc" in ll: 
                    if not any(k in ll for k in ("public domain", "cc0", "pd")) and "cc by" not in ll: continue
                if "nc" in ll or "nd" in ll:  # keep NC/ND out of the inspiration board? allowed CC -- keep but flag
                    pass
                w, h = ii.get("width", 0), ii.get("height", 0)
                if w < 350 or h < 350 or w > 2.0*h: continue
                desc = re.sub("<[^>]+>", "", md.get("ImageDescription", {}).get("value", "")).strip()[:200]
                date = md.get("DateTimeOriginal", {}).get("value", "")[:40]
                t = p["title"].replace("File:", "")
                if t in seen_titles: continue
                seen_titles.add(t)
                items.append(dict(title=t, url=ii.get("thumburl") or ii["url"], page=ii.get("descriptionurl"), lic=lic, author=author, cat=cat, society=soc, desc=desc, date=date, w=w, h=h)); picked += 1
        print(f"  -> picked {picked}", flush=True)
    except Exception as e: print("failed", soc, cat, e, flush=True)
json.dump(existing + items, open(OUT + ".pending.json", "w"), indent=1)   # metadata saved before any download so a throttled run loses nothing
ok = list(existing)
for i, it in enumerate(items):
    p = os.path.join(DL, f"c{start_idx+i:03d}.jpg")
    if get(it["url"], p): it["path"] = p; ok.append(it)
    time.sleep(1.6)
    json.dump(ok, open(OUT, "w"), indent=1)
json.dump(ok, open(OUT, "w"), indent=1)
print(len(items), "new candidates downloaded; total", len(ok), flush=True)
