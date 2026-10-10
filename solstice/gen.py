# Generate every asset for the film through fal.ai, in parallel. Re-running skips files that already exist.
# Usage: python3 gen.py            (everything)
#        python3 gen.py voice      (only narration)   | music | sfx | video | v07 (one shot)
import os, sys, json, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film, fal_client as fal

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"); os.makedirs(OUT, exist_ok=True)
lock = threading.Lock()
def log(msg):
    with lock: print(time.strftime("%H:%M:%S"), msg, flush=True)

def job_voice(seg):
    p = os.path.join(OUT, f"voice_{seg['id']}.mp3"); meta = p + ".json"
    if os.path.exists(p): return p
    res = fal.run("fal-ai/elevenlabs/tts/eleven-v3", dict(text=" ".join(seg["text"].split()), voice=film.VOICE, stability=0.45, timestamps=True), log)
    fal.download(fal.first_url(res), p); json.dump(res, open(meta, "w"))
    return p

def job_music():
    p = os.path.join(OUT, "music.mp3")
    if os.path.exists(p): return p
    res = fal.run("elevenlabs/music/v2.5", dict(prompt=film.MUSIC_PROMPT, music_length_ms=185000, force_instrumental=True, output_format="mp3_44100_192"), log)
    fal.download(fal.first_url(res), p); return p

def job_sfx(s):
    p = os.path.join(OUT, f"sfx_{s['id']}.mp3")
    if os.path.exists(p): return p
    res = fal.run("fal-ai/elevenlabs/sound-effects/v2", dict(text=s["text"], duration_seconds=s["seconds"], loop=s.get("loop", False), prompt_influence=0.4), log)
    fal.download(fal.first_url(res), p); return p

def job_video(shot):
    p = os.path.join(OUT, f"{shot['id']}.mp4")
    if os.path.exists(p): return p
    res = fal.run("bytedance/seedance-2.0/fast/text-to-video",
                  dict(prompt=shot["prompt"] + " " + film.STYLE, duration="8", aspect_ratio="16:9", resolution="720p", generate_audio=True, codec="H264"), log)
    fal.download(fal.first_url(res), p); json.dump(res, open(p + ".json", "w")); return p

def main():
    want = sys.argv[1:] or ["voice", "music", "sfx", "video"]
    jobs = []
    if "voice" in want: jobs += [(f"voice {s['id']}", job_voice, s) for s in film.SEGMENTS]
    if "music" in want: jobs += [("music", job_music)]
    if "sfx" in want:   jobs += [(f"sfx {s['id']}", job_sfx, s) for s in film.SFX]
    if "video" in want: jobs += [(f"video {s['id']}", job_video, s) for s in film.SHOTS if s.get("kind", "gen") == "gen"]
    for w in want:
        for s in film.SHOTS:
            if s["id"] == w: jobs.append((f"video {w}", job_video, s))
        for s in film.SEGMENTS:
            if s["id"] == w: jobs.append((f"voice {w}", job_voice, s))
    ok, bad = [], []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(j[1], *j[2:]): j[0] for j in jobs}
        for f in as_completed(futs):
            name = futs[f]
            try: r = f.result(); log(f"DONE {name} -> {os.path.basename(r)} {os.path.getsize(r)//1024} KB"); ok.append(name)
            except Exception as e: log(f"FAILED {name}: {e}"); bad.append((name, str(e)))
    log(f"{len(ok)} ok, {len(bad)} failed"); 
    for n, e in bad: print("  ", n, e[:300])

if __name__ == "__main__": main()
