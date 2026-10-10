# Tiny fal.ai queue client. Needs FAL_KEY in the environment.
import os, time, json, urllib.request, urllib.error
KEY = os.environ.get("FAL_KEY")
H = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}

def _req(url, data=None, headers=H, timeout=120):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
    with urllib.request.urlopen(r, timeout=timeout) as resp: return json.loads(resp.read())

def run(model, payload, log=print, poll=3.0, max_wait=1800):
    """Submit a job to the fal queue, wait for it, return the result dict."""
    t0 = time.time()
    try: q = _req(f"https://queue.fal.run/{model}", payload)
    except urllib.error.HTTPError as e: raise RuntimeError(f"submit {model} failed {e.code}: {e.read()[:500]}")
    last = None
    while time.time() - t0 < max_wait:
        time.sleep(poll)
        try: s = _req(q["status_url"] + "?logs=0")
        except urllib.error.HTTPError as e:
            if e.code in (404, 429, 500, 502, 503): continue
            raise
        if s["status"] != last: log(f"{model}: {s['status']} ({int(time.time()-t0)}s)"); last = s["status"]
        if s["status"] == "COMPLETED": break
        if s["status"] == "FAILED": raise RuntimeError(f"{model} failed: {json.dumps(s)[:600]}")
    else: raise RuntimeError(f"{model} timed out")
    return _req(q["response_url"])

def download(url, path):
    with urllib.request.urlopen(url, timeout=600) as r, open(path, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk: break
            f.write(chunk)
    return os.path.getsize(path)

def first_url(res):
    """Find the first media URL in a fal response (video.url, audio.url, audio_file.url, ...)."""
    if isinstance(res, dict):
        if "url" in res and isinstance(res["url"], str): return res["url"]
        for k in ("video", "audio", "audio_file", "output", "image", "images"):
            if k in res:
                u = first_url(res[k])
                if u: return u
        for v in res.values():
            u = first_url(v)
            if u: return u
    if isinstance(res, list):
        for v in res:
            u = first_url(v)
            if u: return u
    return None
