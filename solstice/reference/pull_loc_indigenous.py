# Indigenous / traditional-society portraits from the Library of Congress Prints & Photographs (public domain), via the loc.gov JSON API.
import os, json, time, urllib.request, urllib.parse, re
HERE = os.path.dirname(os.path.abspath(__file__)); DL = os.path.join(HERE, "indigenous", "cand_loc"); os.makedirs(DL, exist_ok=True)
UA = {"User-Agent": "solstice-film-reference-board/1.0 (personal research)"}
Q = [  # (query, society, how many)
 ("hopi curtis", "Hopi", 10), ("hopi snake priest", "Hopi", 6), ("navaho curtis portrait", "Navajo", 6), ("apache curtis portrait", "Apache", 6),
 ("zuni curtis", "Zuni", 4), ("eskimo portrait", "Inuit", 8), ("lapland lapp portrait", "Sami", 6), ("bedouin portrait", "Bedouin", 6),
 ("mongolian portrait", "Mongolian", 6), ("ainu portrait", "Ainu", 6), ("tibet tibetan portrait", "Tibetan", 6), ("peru indian portrait", "Quechua", 6),
 ("bolivia indian portrait", "Aymara", 4), ("araucanian mapuche", "Mapuche", 4), ("australian aborigines portrait", "Aboriginal Australian", 4),
 ("new guinea native portrait", "Papua New Guinea", 4), ("masai portrait", "Maasai", 4), ("kabyle berber portrait", "Berber", 4), ("tuareg portrait", "Tuareg", 4),
 ("kirghiz portrait", "Kyrgyz / Kazakh", 4), ("samoyed portrait", "Nenets", 4), ("siberia native portrait", "Siberian", 4), ("amazon indian portrait", "Amazonian", 4),
 ("kalash kafir chitral", "Kalash", 3), ("sioux curtis portrait", "Lakota", 4), ("piegan curtis", "Blackfeet", 4),
]
items = []
for q, soc, n in Q:
    url = "https://www.loc.gov/pictures/search/?" + urllib.parse.urlencode(dict(q=q, fo="json", c=n*3))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: d = json.load(r)
    except Exception as e: print("failed", q, e, flush=True); time.sleep(3); continue
    got = 0
    for res in d.get("results", []):
        img = res.get("image", {}); u = img.get("full") or img.get("thumb")
        t = res.get("title", "")
        if not u or re.search(r"map|landscape|village|camp|dance group|panorama", t, re.I): continue
        if u.startswith("//"): u = "https:" + u
        link = res.get("links", {}).get("item", ""); link = "https:" + link if link.startswith("//") else link
        items.append(dict(title=t[:110], url=u, page=link, lic="Public domain (Library of Congress)", author=(res.get("creator") or "")[:50], society=soc, cat="LOC " + q)); got += 1
        if got >= n: break
    print(f"{soc:>22} '{q}': {got}", flush=True); time.sleep(2)
ok = []
for i, it in enumerate(items):
    p = os.path.join(DL, f"l{i:03d}.jpg")
    try:
        with urllib.request.urlopen(urllib.request.Request(it["url"], headers=UA), timeout=120) as r, open(p, "wb") as f: f.write(r.read())
        it["path"] = p; ok.append(it)
    except Exception as e: print("dl failed", it["title"][:40], e, flush=True)
    time.sleep(0.8)
json.dump(ok, open(os.path.join(HERE, "indigenous", "cand_loc.json"), "w"), indent=1)
print(len(ok), "LOC candidates downloaded", flush=True)
