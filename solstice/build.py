# Cut "The Longest Night" from the generated assets. Usage: python3 build.py [--target 180]
# Reads film.py and assets/, writes out/the_longest_night.mp4 (1080p, 24 fps) and a timeline.json.
import os, sys, json, math, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets"); OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 24
XF = 1.0            # crossfade seconds between shots
TARGET = float(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 180.0
TAIL = 9.0          # seconds after the last narration line (end card + fade)
CLIP_LEN = 8.0      # Seedance clips are 8 s

SERIF = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
SANS = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
SANS_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
F = lambda p, s: ImageFont.truetype(p, s)

def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())

# ---------------- code-drawn shots ----------------
def ease(t): t = max(0.0, min(1.0, t)); return t*t*(3-2*t)

def pipe_frames(path, nframes, frame_fn):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(nframes): p.stdin.write(np.asarray(frame_fn(i / FPS).convert("RGB")).tobytes())
    p.stdin.close(); p.wait()

def tracked(d, xy, text, font, fill, tracking, anchor="m"):
    # draw text with letter spacing, centered on xy
    widths = [font.getlength(c) for c in text]; total = sum(widths) + tracking*(len(text)-1)
    x = xy[0] - total/2; y = xy[1]
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill, anchor="lm"); x += w + tracking

# --- shared "old star chart" look for the code-drawn cards: dark warm paper grain, ivory ink, gold accents
IVORY = (226, 212, 178); GOLD = (214, 172, 80); INK_BLUE = (30, 46, 78)
_PAPER = None
def paper():
    global _PAPER
    if _PAPER is None:
        rng = np.random.default_rng(3)
        g = rng.normal(0, 1, (H, W)).astype(np.float32)
        g = np.asarray(Image.fromarray(np.clip(g*40+128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) - 128
        base = np.zeros((H, W, 3), np.float32) + np.array([16, 13, 10], np.float32)
        base += g[..., None] * np.array([0.09, 0.08, 0.06], np.float32)
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx-W/2)/(W/2))**2 + ((yy-H/2)/(H/2))**2)
        base *= (1 - 0.35*np.clip(r-0.5, 0, 1))[..., None]
        _PAPER = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    return _PAPER.copy()

def mul(rgb, a): return tuple(int(v*max(0.0, min(1.0, a))) for v in rgb)

def woodcut_sun(d, cx, cy, r, col, rays=24, a=1.0):
    # alternating straight and wavy rays, like an old engraving
    for i in range(rays):
        th = 2*math.pi*i/rays; L = r*0.55 if i % 2 == 0 else r*0.38
        x0, y0 = cx + (r+10)*math.cos(th), cy + (r+10)*math.sin(th)
        if i % 2 == 0:
            d.line((x0, y0, cx + (r+10+L)*math.cos(th), cy + (r+10+L)*math.sin(th)), fill=mul(col, a), width=3)
        else:
            pts = []
            for k in range(9):
                f = k/8; rr = r+10+L*f; w = 7*math.sin(f*math.pi*3)
                pts.append((cx + rr*math.cos(th) - w*math.sin(th), cy + rr*math.sin(th) + w*math.cos(th)))
            d.line(pts, fill=mul(col, a), width=2)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=mul(col, a), outline=mul(IVORY, 0.6*a), width=2)

def render_title(path, length):
    bg = paper()
    def frame(t):
        im = bg.copy(); d = ImageDraw.Draw(im)
        rng = np.random.default_rng(7)
        for _ in range(220):
            x, y, b = rng.integers(0, W), rng.integers(0, H), rng.integers(50, 150)
            tw = 0.6 + 0.4*math.sin(t*1.3 + x*0.01)
            d.point((x, y), fill=mul(IVORY, b/255*tw))
        a1 = ease((t-0.8)/2.0); a2 = ease((t-2.2)/1.6); out = 1 - ease((t-(length-1.6))/1.4)
        woodcut_sun(d, W//2, 380, 26, GOLD, rays=16, a=a1*out)
        tracked(d, (W//2, 540), "THE LONGEST NIGHT", F(SERIF, 96), mul(IVORY, a1*out), 14)
        d.line((W//2-260, 610, W//2+260, 610), fill=mul(GOLD, 0.7*a2*out), width=1)
        tracked(d, (W//2, 660), "a film for the winter solstice", F(SERIF_I, 38), mul(IVORY, 0.85*a2*out), 2)
        return im
    pipe_frames(path, int(length*FPS), frame)

def render_tilt(path, length):
    bg = paper()
    def frame(t):
        im = bg.copy(); d = ImageDraw.Draw(im)
        fade = ease(t/1.2) * (1 - ease((t-(length-1.2))/1.2))
        c = lambda rgb, a=1.0: mul(rgb, a*fade)
        sx, sy = 330, H//2
        glow = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((sx-280, sy-280, sx+280, sy+280), fill=c((50, 36, 10))); glow = glow.filter(ImageFilter.GaussianBlur(100))
        im = Image.fromarray(np.clip(np.asarray(im).astype(np.int16) + np.asarray(glow), 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
        # rays of light drawn as fine engraved lines
        for y in range(-300, 301, 50):
            d.line((sx+170, sy+y, W-150, sy+y), fill=c(GOLD, 0.16), width=1)
        woodcut_sun(d, sx, sy, 100, GOLD, rays=28, a=fade)
        # earth: engraved globe with meridians, tilting from 0 to 23.4 degrees between t=1.5 and 4.5
        ex, ey, R = 1330, H//2, 230
        tilt = ease((t-1.5)/3.0); ang = math.radians(23.4*tilt)
        d.ellipse((ex-R, ey-R, ex+R, ey+R), fill=c(INK_BLUE))
        def rot(x, y): return (ex + x*math.cos(ang) - y*math.sin(ang), ey + x*math.sin(ang) + y*math.cos(ang))
        # meridians and parallels, rotated with the axis
        for k in (-0.75, -0.4, 0.4, 0.75):
            pts = [rot(R*k*math.cos(p), R*math.sin(p)) for p in np.linspace(-math.pi/2, math.pi/2, 40)]
            d.line(pts, fill=c(IVORY, 0.35), width=1)
        for k in (-0.6, -0.3, 0.3, 0.6):
            yk = R*k; xr = R*math.sqrt(1-k*k)
            d.line([rot(-xr, yk), rot(xr, yk)], fill=c(IVORY, 0.28), width=1)
        d.line([rot(-R, 0), rot(R, 0)], fill=c(IVORY, 0.6), width=2)   # equator
        # night side: dark wash plus diagonal hatching, clipped to the half facing away from the sun
        night = Image.new("L", (W, H), 0); nd = ImageDraw.Draw(night)
        nd.ellipse((ex-R, ey-R, ex+R, ey+R), fill=255); nd.rectangle((0, 0, ex, H), fill=0)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle((0, 0, W, H), fill=(4, 5, 10, int(150*fade)))
        for k in range(-R*2, R*2, 11):
            od.line((ex+k, ey-R-10, ex+k+R, ey+R+10), fill=(4, 5, 10, int(230*fade)), width=2)
        ov.putalpha(Image.fromarray((np.asarray(ov.split()[3]).astype(np.uint16) * np.asarray(night) // 255).astype(np.uint8)))
        im = im.convert("RGBA"); im.alpha_composite(ov); im = im.convert("RGB"); d = ImageDraw.Draw(im)
        d.ellipse((ex-R, ey-R, ex+R, ey+R), outline=c(IVORY, 0.9), width=2)
        d.ellipse((ex-R-14, ey-R-14, ex+R+14, ey+R+14), outline=c(IVORY, 0.25), width=1)
        # axis, reference, arc with ticks
        d.line([rot(0, -R-80), rot(0, R+80)], fill=c(IVORY), width=3)
        d.line((ex, ey-R-80, ex, ey-R-16), fill=c(IVORY, 0.35), width=1)
        if ang > 0.01:
            d.arc((ex-R-50, ey-R-50, ex+R+50, ey+R+50), start=270, end=270+math.degrees(ang), fill=c(GOLD), width=3)
            for deg in range(0, int(math.degrees(ang))+1, 5):
                th = math.radians(270+deg); r1, r2 = R+44, R+58
                d.line((ex+r1*math.cos(th), ey+r1*math.sin(th), ex+r2*math.cos(th), ey+r2*math.sin(th)), fill=c(GOLD, 0.8), width=1)
        lab = ease((t-4.0)/1.0)
        d.text((ex+80, ey-R-130), f"{23.4*tilt:.1f}°", font=F(SERIF, 64), fill=c(GOLD, lab))
        d.text((ex, ey+R+74), "The northern half leans away from the sun", font=F(SERIF_I, 32), fill=c(IVORY, 0.8*lab), anchor="ma")
        d.text((ex, ey+R+120), "December solstice", font=F(SERIF, 32), fill=c(IVORY, lab), anchor="ma")
        return im
    pipe_frames(path, int(length*FPS), frame)

def render_end(path, length):
    bg = paper()
    def frame(t):
        im = bg.copy(); d = ImageDraw.Draw(im)
        a1 = ease((t-0.5)/1.6); a2 = ease((t-2.5)/1.5); out = 1 - ease((t-(length-1.5))/1.5)
        woodcut_sun(d, W//2, 300, 22, GOLD, rays=16, a=a1*out)
        tracked(d, (W//2, 430), "Happy solstice.", F(SERIF_I, 92), mul(IVORY, a1*out), 2)
        d.line((W//2-200, 500, W//2+200, 500), fill=mul(GOLD, 0.7*a2*out), width=1)
        tracked(d, (W//2, 560), f"Directed by {film.DIRECTOR}", F(SERIF, 40), mul(IVORY, a2*out), 3)
        lines = ["Made with AI for the AI Cafe holiday film festival",
                 "Video: Seedance 2.0 Fast  ·  Voice, music and effects: ElevenLabs  ·  via fal.ai",
                 "Lettering and diagrams drawn in code"]
        for i, ln in enumerate(lines):
            d.text((W//2, 690 + i*46), ln, font=F(SERIF, 28), fill=mul(IVORY, 0.6*a2*out), anchor="ma")
        return im
    pipe_frames(path, int(length*FPS), frame)

def render_caption(path, text):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = F(SERIF, 40)
    # soft shadow for legibility
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    BAR = 138; y = H - BAR - 96
    sd.text((122, y), text, font=f, fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(6))
    im.alpha_composite(sh)
    d.line((120, y-16, 120, y+46), fill=(242, 193, 78, 255), width=3)
    d.text((142, y), text, font=f, fill=(245, 245, 245, 255))
    im.save(path)

# ---------------- timeline ----------------
def main():
    segs = []
    for s in film.SEGMENTS:
        p = os.path.join(A, f"voice_{s['id']}.mp3")
        if not os.path.exists(p): sys.exit(f"missing narration {p}; run gen.py voice")
        segs.append(dict(s, path=p, ndur=dur(p)))
    N = sum(s["ndur"] for s in segs); G = sum(s["gap"] for s in segs)
    k = (TARGET - TAIL - N) / G
    if k < 0.3: print(f"warning: narration ({N:.0f}s) nearly fills the target; gaps squeezed (k={k:.2f})")
    t = 0.0
    for s in segs:
        s["start"] = t + s["gap"]*k; s["slot_start"] = t; t = s["start"] + s["ndur"]
    segs[-1]["slot_end"] = t + TAIL
    for i in range(len(segs)-1): segs[i]["slot_end"] = segs[i+1]["slot_start"]
    total = segs[-1]["slot_end"]
    print(f"narration {N:.1f}s, gaps scaled x{k:.2f}, total {total:.1f}s")

    # shots: give fixed-length code cards (title, end) their time first, then split the rest of the
    # segment's slot evenly among the other shots (generated shots whose file is missing are skipped)
    FIXED = {"title": 9.0, "end": TAIL}
    shots = []
    for s in segs:
        mine = [sh for sh in film.SHOTS if sh["seg"] == s["id"]]
        mine = [sh for sh in mine if sh.get("kind", "gen") == "code" or os.path.exists(os.path.join(A, sh["id"] + ".mp4"))]
        if not mine: sys.exit(f"no shots available for segment {s['id']}")
        slot = s["slot_end"] - s["slot_start"]
        fixed = sum(v for k, v in FIXED.items() for sh in mine if sh.get(k))
        flex = [sh for sh in mine if not any(sh.get(k) for k in FIXED)]
        L = (slot - fixed) / max(1, len(flex))
        for sh in mine:
            shots.append(dict(sh, L=next((v for k, v in FIXED.items() if sh.get(k)), L)))
    # recompute starts sequentially so they chain exactly
    t = 0.0
    for sh in shots: sh["start"] = t; t += sh["L"]
    total = t
    for sh in shots: print(f"{sh['id']:>4} {sh['seg']} {sh['start']:6.1f}s  {sh['L']:4.1f}s  {sh.get('cap') or ''}")

    # render code shots and captions
    for sh in shots:
        if sh.get("kind") == "code":
            path = os.path.join(OUT, sh["id"] + ".mp4"); need = sh["L"] + (0 if sh is shots[-1] else XF)
            if not os.path.exists(path) or abs(dur(path) - need) > 0.2:
                (render_title if sh.get("title") else render_tilt if sh.get("tilt") else render_end)(path, need)
            sh["path"] = path
        else:
            sh["path"] = os.path.join(A, sh["id"] + ".mp4")
        if sh.get("cap"):
            sh["cap_png"] = os.path.join(OUT, f"cap_{sh['id']}.png"); render_caption(sh["cap_png"], sh["cap"])

    # ---------------- ffmpeg graph ----------------
    inputs, fc = [], []
    def add(*args): inputs.extend(args); return (len([a for a in inputs if a == "-i"]) - 1)
    # video chain
    vlabels = []
    for i, sh in enumerate(shots):
        last = i == len(shots) - 1
        need = sh["L"] + (0 if last else XF)
        idx = add("-i", sh["path"])
        src = dur(sh["path"]) if sh.get("kind") != "code" else need
        slow = max(1.0, need / src) if src < need else 1.0     # stretch a short clip instead of cutting to black
        fc.append(f"[{idx}:v]fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,setpts={slow:.4f}*PTS,trim=0:{need:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        vlabels.append(f"[v{i}]"); sh["idx"] = idx; sh["slow"] = slow
    cur = vlabels[0]; off = 0.0
    for i in range(1, len(shots)):
        off += shots[i-1]["L"]
        fc.append(f"{cur}{vlabels[i]}xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); cur = f"[x{i}]"
    # film look: gentle curve, desaturate, grain, vignette, 2.39:1 letterbox
    LOOK = ("eq=contrast=1.06:saturation=0.8:gamma=1.02,curves=master='0/0.03 0.25/0.22 0.75/0.78 1/0.97',"
            "noise=c0s=16:c0f=t+u:c1s=5:c1f=t+u:c2s=5:c2f=t+u,vignette=angle=PI/4.5,crop=1920:804:0:138,pad=1920:1080:0:138:black")
    fc.append(f"{cur}{LOOK}[look]"); cur = "[look]"
    # captions
    for sh in shots:
        if not sh.get("cap_png"): continue
        D = sh["L"] - 1.0; S = sh["start"] + 0.6
        idx = add("-loop", "1", "-t", f"{D:.3f}", "-i", sh["cap_png"])
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.8:alpha=1,fade=t=out:st={D-0.8:.3f}:d=0.8:alpha=1,setpts=PTS+{S:.3f}/TB[c{idx}]")
        fc.append(f"{cur}[c{idx}]overlay=eof_action=pass[o{idx}]"); cur = f"[o{idx}]"
    fc.append(f"{cur}fade=t=out:st={total-1.5:.3f}:d=1.5[vout]")

    # audio: narration
    alab = []
    vo = []
    for s in segs:
        idx = add("-i", s["path"]); fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(s['start']*1000)}:all=1[n{idx}]"); vo.append(f"[n{idx}]")
    fc.append("".join(vo) + f"amix=inputs={len(vo)}:normalize=0,asplit=2[voice][voice_sc]")
    # music, ducked under the voice
    mp = os.path.join(A, "music.mp3")
    if os.path.exists(mp):
        idx = add("-stream_loop", "-1", "-i", mp)
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},afade=t=in:d=4,afade=t=out:st={total-7:.3f}:d=7,volume=0.55[m0]")
        fc.append("[m0][voice_sc]sidechaincompress=threshold=0.04:ratio=5:attack=120:release=1400:makeup=1[music]")
        alab.append("[music]")
    else:
        fc.append("[voice_sc]anullsink"); print("no music.mp3; mixing without score")
    alab.append("[voice]")
    # ambience from each generated clip
    for i, sh in enumerate(shots):
        if sh.get("kind") == "code": continue
        last = i == len(shots) - 1; need = sh["L"] + (0 if last else XF)
        fc.append(f"[{sh['idx']}:a]aformat=sample_rates=48000:channel_layouts=stereo,atempo={1/sh['slow']:.4f},atrim=0:{need:.3f},afade=t=in:d={XF},afade=t=out:st={max(0, need-XF):.3f}:d={XF},volume=0.22,adelay={int(sh['start']*1000)}:all=1[amb{i}]")
        alab.append(f"[amb{i}]")
    # sound effects placed on the timeline
    by_id = {sh["id"]: sh for sh in shots}
    seg_at = {s["id"]: s for s in segs}
    def at(shot_id, plus=0.0): return by_id[shot_id]["start"] + plus if shot_id in by_id else None
    cues = [
        ("wind",  0.5, 0.35, 48.0),                      # (sfx, start, volume, max length)
        ("drum",  seg_at["s2"]["start"] - 0.3, 0.8, 6),
        ("drum",  at("v05", 3.0), 0.5, 6),
        ("fire",  at("v17"), 0.45, 10),
        ("fire",  at("v19"), 0.5, 10),
        ("wind",  at("v20"), 0.3, 20),
        ("bell",  seg_at["s6"]["start"] + seg_at["s6"]["ndur"] - 1.0, 0.6, 6),
        ("crowd", at("v23"), 0.5, 10),
        ("rise",  at("v26"), 0.7, 8),
    ]
    for j, (sid, st, vol, mx) in enumerate(cues):
        p = os.path.join(A, f"sfx_{sid}.mp3")
        if st is None or not os.path.exists(p): continue
        idx = add("-stream_loop", "2" if sid == "wind" else "0", "-i", p)
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{mx},afade=t=in:d=1.5,afade=t=out:st={mx-2.5:.3f}:d=2.5,volume={vol},adelay={int(st*1000)}:all=1[s{j}]")
        alab.append(f"[s{j}]")
    fc.append("".join(alab) + f"amix=inputs={len(alab)}:normalize=0,alimiter=limit=0.95,afade=t=out:st={total-2.5:.3f}:d=2.5,atrim=0:{total:.3f}[aout]")

    final = os.path.join(OUT, "the_longest_night.mp4")
    graph = os.path.join(OUT, "graph.txt"); open(graph, "w").write(";\n".join(fc))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats"] + inputs + ["-filter_complex_script", graph, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", final]
    json.dump(dict(total=total, segments=[{k: v for k, v in s.items() if k != "text"} for s in segs],
                   shots=[{k: v for k, v in sh.items() if k not in ("prompt",)} for sh in shots]), open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
    print("encoding...", flush=True)
    subprocess.run(cmd, check=True)
    print("wrote", final, f"{os.path.getsize(final)/1e6:.1f} MB, {total:.1f}s")

if __name__ == "__main__": main()
