# Pull candidate portraits from the Library of Congress FSA/OWI collection (public domain) via the loc.gov JSON API.
import os, json, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); DL = os.path.join(HERE, "cand"); os.makedirs(DL, exist_ok=True)
UA = {"User-Agent": "solstice-film-reference-board/1.0 (personal research)"}
QUERIES = [("portrait farmer face", 10), ("old man portrait", 8), ("old woman portrait", 8), ("child portrait migrant", 8), ("mother child portrait", 6), ("Indian portrait", 6), ("Mexican portrait", 6), ("Negro farmer portrait", 6)]
items = []
for q, n in QUERIES:
    url = "https://www.loc.gov/pictures/search/?" + urllib.parse.urlencode(dict(q=q, co="fsa", fo="json", c=n*2))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: d = json.load(r)
    except Exception as e: print("failed", q, e, flush=True); continue
    got = 0
    for res in d.get("results", []):
        img = res.get("image", {}); u = img.get("full") or img.get("thumb")
        if not u: continue
        if u.startswith("//"): u = "https:" + u
        items.append(dict(title=res.get("title", "")[:90], url=u, page="https:" + res["links"]["item"] if res.get("links", {}).get("item", "").startswith("//") else res.get("links", {}).get("item", ""), lic="Public domain (LOC FSA/OWI)", author=res.get("creator", "")[:50], cat="LOC " + q))
        got += 1
        if got >= n: break
    print(f"LOC {q}: {got}", flush=True); time.sleep(2)
ok = []
for i, it in enumerate(items):
    p = os.path.join(DL, f"l{i:03d}.jpg")
    try:
        with urllib.request.urlopen(urllib.request.Request(it["url"], headers=UA), timeout=120) as r, open(p, "wb") as f: f.write(r.read())
        it["path"] = p; ok.append(it)
    except Exception as e: print("dl failed", it["title"][:40], e, flush=True)
    time.sleep(0.7)
json.dump(ok, open(os.path.join(HERE, "cand_loc.json"), "w"), indent=1)
print(len(ok), "LOC candidates downloaded", flush=True)
