import os, sys, math, json, subprocess, wave
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from script import SCENES, SOURCES

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
VOICE = os.path.join(ROOT, "..", "voice", "en_US-lessac-medium.onnx")
W, H, FPS = 1920, 1080, 30
FONT_DIR = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(FONT_DIR + name, size)
F_TITLE = lambda s: font("InterDisplay-Bold.otf", s)
F_BODY  = lambda s: font("Inter-Regular.otf", s)
F_MED   = lambda s: font("Inter-Medium.otf", s)
F_SEMI  = lambda s: font("Inter-SemiBold.otf", s)
F_IT    = lambda s: font("Inter-Italic.otf", s)
F_SERIF = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf", s)

BG = (11, 15, 26); TEXT = (236, 239, 244); MUTED = (138, 147, 166)
GOLD = (242, 193, 78); TEAL = (79, 209, 197); RED = (240, 110, 110); PANEL = (20, 26, 42)

def ease(t):  # smoothstep clamp
    t = max(0.0, min(1.0, t)); return t*t*(3-2*t)

def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if fnt.getlength(test) <= maxw: cur = test
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def background():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # subtle dot grid
    for x in range(60, W, 60):
        for y in range(60, H, 60):
            d.point((x, y), fill=(26, 32, 50))
    # soft radial glow top-left
    glow = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((-400, -500, 900, 700), fill=(22, 30, 52))
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    im = Image.fromarray(np.clip(np.asarray(im).astype(np.int16) + np.asarray(glow).astype(np.int16) - 11, 0, 255).astype(np.uint8))
    return im

BGIMG = None
def bg(): 
    global BGIMG
    if BGIMG is None: BGIMG = background()
    return BGIMG.copy()

def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def composite(base, lyr, alpha):
    if alpha <= 0: return base
    if alpha < 1:
        a = lyr.split()[3].point(lambda v: int(v * alpha))
        lyr = lyr.copy(); lyr.putalpha(a)
    base.alpha_composite(lyr); return base

def text_layer(text, fnt, xy, fill=TEXT, maxw=None, spacing=1.25, anchor="la"):
    L = layer(); d = ImageDraw.Draw(L)
    x, y = xy
    lines = wrap(text, fnt, maxw) if maxw else [text]
    lh = int(fnt.size * spacing)
    for i, ln in enumerate(lines):
        d.text((x, y + i*lh), ln, font=fnt, fill=fill + (255,), anchor=anchor)
    return L, len(lines) * lh

def header(title, color=GOLD):
    L = layer(); d = ImageDraw.Draw(L)
    d.rounded_rectangle((120, 96, 132, 150), radius=6, fill=color + (255,))
    d.text((156, 92), title, font=F_TITLE(54), fill=TEXT + (255,))
    return L

def footer_layer(idx, total):
    L = layer(); d = ImageDraw.Draw(L)
    d.text((120, H-70), "722 Proofs in a Night  ·  a short explainer", font=F_MED(24), fill=MUTED + (255,))
    d.text((W-120, H-70), f"{idx+1} / {total}", font=F_MED(24), fill=MUTED + (255,), anchor="ra")
    return L

# ---------- scene renderers: each returns function f(t, dur) -> RGBA image ----------

def scene_title(sc):
    big = sc.get("big", True)
    tf = F_TITLE(112 if len(sc["title"]) < 24 else 84)
    tl, th = text_layer(sc["title"], tf, (W//2, 400), maxw=1500, anchor="ma")
    sl, sh = text_layer(sc["sub"], F_BODY(40), (W//2, 400 + th + 30), fill=MUTED, maxw=1300, anchor="ma")
    rule = layer(); ImageDraw.Draw(rule).rounded_rectangle((W//2-60, 350, W//2+60, 358), radius=4, fill=GOLD + (255,))
    def f(t, dur):
        im = bg().convert("RGBA")
        composite(im, rule, ease(t/0.8))
        composite(im, tl, ease((t-0.3)/1.0))
        composite(im, sl, ease((t-1.2)/1.0))
        return im
    return f

def scene_stats(sc):
    hdr = header(sc["title"]); items = []
    n = len(sc["stats"]); boxw = 360; gap = 40
    total = n*boxw + (n-1)*gap; x0 = (W - total)//2
    for i, (num, lab) in enumerate(sc["stats"]):
        L = layer(); d = ImageDraw.Draw(L)
        x = x0 + i*(boxw+gap); y = 380
        d.rounded_rectangle((x, y, x+boxw, y+300), radius=24, fill=PANEL + (255,), outline=(40, 50, 76, 255), width=2)
        d.text((x+boxw//2, y+90), num, font=F_TITLE(84 if len(num) < 6 else 64), fill=GOLD + (255,), anchor="mm")
        d.text((x+boxw//2, y+200), lab, font=F_MED(30), fill=TEXT + (255,), anchor="mm")
        items.append(L)
    cap, _ = text_layer("Source: openai/math repository README, October 6 2026", F_IT(26), (W//2, 760), fill=MUTED, anchor="ma")
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        for i, L in enumerate(items):
            a = ease((t - 0.8 - i*0.5)/0.6)
            if a > 0:
                dy = int((1-a)*30)
                composite(im, L.transform(L.size, Image.AFFINE, (1,0,0,0,1,-dy)), a)
        composite(im, cap, ease((t-3.2)/0.8))
        return im
    return f

def scene_bullets(sc):
    hdr = header(sc["title"]); items = []; y = 230
    fnt = F_BODY(40); maxw = 1500
    for b in sc["bullets"]:
        L = layer(); d = ImageDraw.Draw(L)
        d.ellipse((156, y+14, 176, y+34), fill=TEAL + (255,))
        lines = wrap(b, fnt, maxw)
        for j, ln in enumerate(lines): d.text((210, y + j*52), ln, font=fnt, fill=TEXT + (255,))
        items.append(L); y += 52*len(lines) + 46
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        n = len(items); start, end = 0.08*dur + 1.0, 0.78*dur
        for i, L in enumerate(items):
            t_i = start + (end-start) * i/max(1, n-1)
            a = ease((t - t_i)/0.6)
            if a > 0:
                dx = int((1-a)*-40)
                composite(im, L.transform(L.size, Image.AFFINE, (1,0,-dx,0,1,0)), a)
        return im
    return f

def scene_quotes(sc):
    hdr = header(sc["title"]); items = []; y = 240
    qf = F_SERIF(46); af = F_MED(28)
    for q, a in sc["quotes"]:
        L = layer(); d = ImageDraw.Draw(L)
        lines = wrap(q, qf, 1480)
        d.rounded_rectangle((156, y, 164, y + 58*len(lines) + 44), radius=4, fill=GOLD + (255,))
        for j, ln in enumerate(lines): d.text((200, y + j*58), ln, font=qf, fill=TEXT + (255,))
        d.text((200, y + 58*len(lines) + 10), "— " + a, font=af, fill=MUTED + (255,))
        items.append(L); y += 58*len(lines) + 44 + 60
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        n = len(items); start, end = 0.06*dur + 1.0, 0.70*dur
        for i, L in enumerate(items):
            t_i = start + (end-start) * i/max(1, n-1)
            composite(im, L, ease((t - t_i)/0.8))
        return im
    return f

def is_prime(n):
    if n < 2: return False
    for p in range(2, int(n**0.5)+1):
        if n % p == 0: return False
    return True

def scene_primes(sc):
    hdr = header(sc["title"])
    # grid of 1..100 (10x10)
    cell = 64; gx0, gy0 = 180, 250
    grid = layer(); d = ImageDraw.Draw(grid)
    nf = F_MED(26)
    for n in range(1, 101):
        r, c = (n-1)//10, (n-1)%10
        x, y = gx0 + c*cell, gy0 + r*cell
        d.rounded_rectangle((x, y, x+cell-8, y+cell-8), radius=8, fill=PANEL + (255,))
        d.text((x+(cell-8)//2, y+(cell-8)//2), str(n), font=nf, fill=MUTED + (255,), anchor="mm")
    primes = [n for n in range(1, 101) if is_prime(n)]
    plys = []
    for n in primes:
        r, c = (n-1)//10, (n-1)%10
        x, y = gx0 + c*cell, gy0 + r*cell
        L = layer(); dd = ImageDraw.Draw(L)
        dd.rounded_rectangle((x, y, x+cell-8, y+cell-8), radius=8, fill=GOLD + (255,))
        dd.text((x+(cell-8)//2, y+(cell-8)//2), str(n), font=nf, fill=BG + (255,), anchor="mm")
        plys.append(L)
    # right side: long number line 1..1000 with primes as ticks, and the formula
    right = layer(); d = ImageDraw.Draw(right)
    lx0, lx1, ly = 960, 1800, 560
    d.line((lx0, ly, lx1, ly), fill=MUTED + (255,), width=3)
    for n in range(2, 1001):
        if is_prime(n):
            x = lx0 + (lx1-lx0)*(n-1)/999
            d.line((x, ly-28, x, ly+28), fill=GOLD + (200,), width=2)
    d.text((lx0, ly+48), "1", font=F_MED(26), fill=MUTED + (255,))
    d.text((lx1, ly+48), "1,000", font=F_MED(26), fill=MUTED + (255,), anchor="ra")
    d.text(((lx0+lx1)//2, ly-90), "Primes up to 1,000: dense at first, then thinning out", font=F_MED(30), fill=TEXT + (255,), anchor="mm")
    zeta = layer(); d = ImageDraw.Draw(zeta)
    d.rounded_rectangle((960, 700, 1800, 900), radius=24, fill=PANEL + (255,), outline=(40,50,76,255), width=2)
    d.text((1380, 760), "ζ(s) = 1 + 1/2ˢ + 1/3ˢ + 1/4ˢ + …", font=F_SERIF(52), fill=TEXT + (255,), anchor="mm")
    d.text((1380, 840), "The Riemann zeta function. Its zeros encode the rhythm of the primes.", font=F_BODY(26), fill=MUTED + (255,), anchor="mm")
    caption = layer(); d = ImageDraw.Draw(caption)
    d.text((gx0, gy0 + 10*cell + 20), "The first 100 numbers. Gold = prime.", font=F_MED(28), fill=MUTED + (255,))
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        composite(im, grid, ease((t-0.5)/0.8)); composite(im, caption, ease((t-0.5)/0.8))
        # primes light up between 12% and 45% of scene
        t0, t1 = 0.12*dur, 0.45*dur
        for i, L in enumerate(plys):
            ti = t0 + (t1-t0)*i/len(plys)
            composite(im, L, ease((t-ti)/0.35))
        composite(im, right, ease((t-0.48*dur)/1.0))
        composite(im, zeta, ease((t-0.66*dur)/1.0))
        return im
    return f

ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321, 56.446248, 59.347044, 60.831779, 65.112544]

def scene_strip(sc):
    hdr = header(sc["title"])
    # strip geometry: Re from 0 to 1 maps x in [560, 1360]; Im from 0 to 70 maps y from 900 to 230
    X0, X1, Y0, Y1 = 400, 1100, 900, 230
    def xr(re): return X0 + (X1-X0)*re
    base = layer(); d = ImageDraw.Draw(base)
    d.rectangle((X0, Y1, X1, Y0), fill=(18, 24, 40, 255), outline=(50, 60, 90, 255), width=2)
    d.text((xr(0), Y0+16), "0", font=F_MED(28), fill=MUTED + (255,), anchor="ma")
    d.text((xr(1), Y0+16), "1", font=F_MED(28), fill=MUTED + (255,), anchor="ma")
    d.text((xr(0.5), Y0+16), "½", font=F_MED(28), fill=TEAL + (255,), anchor="ma")
    d.text((xr(0.5), Y1-70), "The critical strip", font=F_SEMI(32), fill=TEXT + (255,), anchor="ma")
    # dashed center line
    for y in range(Y1, Y0, 24): d.line((xr(0.5), y, xr(0.5), y+12), fill=TEAL + (255,), width=3)
    center_lbl = layer(); d = ImageDraw.Draw(center_lbl)
    d.text((X0-40, 300), "Riemann's guess (1859):\nall zeros sit on this line", font=F_MED(28), fill=TEAL + (255,), anchor="ra", align="right")
    zl = []
    for im_part in ZEROS:
        L = layer(); dd = ImageDraw.Draw(L)
        y = Y0 - (Y0-Y1)*im_part/70.0
        dd.ellipse((xr(0.5)-9, y-9, xr(0.5)+9, y+9), fill=GOLD + (255,))
        zl.append(L)
    zeros_lbl = layer(); d = ImageDraw.Draw(zeros_lbl)
    d.text((X0-40, 420), "● the known zeros\n(billions checked;\nall on the line so far)", font=F_MED(28), fill=GOLD + (255,), anchor="ra", align="right")
    # old region: Re >= 1 (a thin band at edge), new regions 7/8 and 11/12
    def region(re_from, color, label, sub, lab_y):
        L = layer(); dd = ImageDraw.Draw(L)
        dd.rectangle((xr(re_from), Y1, X1, Y0), fill=color + (90,))
        dd.line((xr(re_from), Y1, xr(re_from), Y0), fill=color + (255,), width=4)
        dd.text((X1 + 40, lab_y), label, font=F_SEMI(32), fill=color + (255,))
        dd.text((X1 + 40, lab_y + 44), sub, font=F_BODY(26), fill=MUTED + (255,))
        return L
    old = region(0.995, RED, "Before: zero-free only at the edge (Re = 1)", "de la Vallée Poussin, 1896 — essentially unmoved since", 420)
    old_bar = layer(); d = ImageDraw.Draw(old_bar); d.line((xr(1), Y1, xr(1), Y0), fill=RED + (255,), width=6)
    new1112 = region(11/12, (120, 190, 255), "Oct 5 manuscript: no zeros past 11/12", "an alternative, human-edited write-up", 560)
    new78 = region(7/8, GOLD, "Claimed, Oct 2026: no zeros past 7/8", "the \"quasi-Riemann hypothesis\". Lean-checked.", 700)
    gap = layer(); d = ImageDraw.Draw(gap)
    d.text((xr(0.6875), Y0 - 60), "still unknown", font=F_IT(28), fill=MUTED + (255,), anchor="mm")
    arrows = layer(); d = ImageDraw.Draw(arrows)
    d.text((X1+40, 850), "Lower boundary = closer to Riemann.\n½ is the prize. 7/8 is the claim.", font=F_BODY(26), fill=MUTED + (255,))
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        composite(im, base, ease((t-0.4)/0.8))
        composite(im, center_lbl, ease((t-1.0)/0.8))
        for i, L in enumerate(zl): composite(im, L, ease((t-1.4-i*0.12)/0.4))
        composite(im, zeros_lbl, ease((t-2.0)/0.8))
        composite(im, old, ease((t-0.20*dur)/1.0)); composite(im, old_bar, ease((t-0.20*dur)/1.0))
        # animate the 7/8 region sliding in from the right edge
        a = ease((t-0.40*dur)/2.0)
        if a > 0:
            re_now = 1 - (1-7/8)*a
            L = layer(); dd = ImageDraw.Draw(L)
            dd.rectangle((xr(re_now), Y1, X1, Y0), fill=GOLD + (90,))
            dd.line((xr(re_now), Y1, xr(re_now), Y0), fill=GOLD + (255,), width=4)
            composite(im, L, 1.0)
            if a >= 1:
                lab = layer(); dd = ImageDraw.Draw(lab)
                dd.text((xr(7/8), Y0+16), "7/8", font=F_SEMI(28), fill=GOLD + (255,), anchor="ma")
                dd.text((X1 + 40, 700), "Claimed, Oct 2026: no zeros past 7/8", font=F_SEMI(32), fill=GOLD + (255,))
                dd.text((X1 + 40, 744), "the \"quasi-Riemann hypothesis\". Lean-checked.", font=F_BODY(26), fill=MUTED + (255,))
                composite(im, lab, ease((t-0.40*dur-2.0)/0.6))
        composite(im, new1112, ease((t-0.52*dur)/0.8))
        composite(im, gap, ease((t-0.60*dur)/0.8))
        composite(im, arrows, ease((t-0.66*dur)/0.8))
        return im
    return f

def scene_sources(sc):
    hdr = header("Sources", color=TEAL); items = []; y = 240
    for s in SOURCES:
        L, h = text_layer("· " + s, F_BODY(34), (160, y), fill=TEXT); items.append(L); y += 60
    note, _ = text_layer("Narration and visuals generated with AI tools in October 2026 from the public reporting listed above. Claims are as reported; most results are not yet peer reviewed.", F_IT(26), (160, y+40), fill=MUTED, maxw=1500)
    def f(t, dur):
        im = bg().convert("RGBA"); composite(im, hdr, ease(t/0.6))
        for i, L in enumerate(items): composite(im, L, ease((t-0.6-i*0.3)/0.6))
        composite(im, note, ease((t-3.0)/0.8))
        return im
    return f

RENDERERS = dict(title=scene_title, stats=scene_stats, bullets=scene_bullets, quotes=scene_quotes,
                 primes=scene_primes, strip=scene_strip, sources=scene_sources)

# ---------- audio ----------
def synth(scene):
    wavp = os.path.join(OUT, f"{scene['id']}.wav")
    if not os.path.exists(wavp):
        txt = " ".join(scene["narration"].split())
        subprocess.run([sys.executable, "-m", "piper", "-m", VOICE, "-f", wavp, "--length-scale", "1.08", "--sentence-silence", "0.45"],
                       input=txt.encode(), check=True, capture_output=True)
    with wave.open(wavp) as w: dur = w.getnframes()/w.getframerate()
    return wavp, dur

def render_scene(args):
    idx, total, scene, dur = args
    f = RENDERERS[scene["kind"]](scene)
    foot = footer_layer(idx, total)
    nframes = int(round(dur*FPS))
    outp = os.path.join(OUT, f"{scene['id']}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", outp], stdin=subprocess.PIPE)
    FADE = 0.6
    for i in range(nframes):
        t = i/FPS
        im = f(t, dur)
        if idx > 0 or True: composite(im, foot, 1.0)
        rgb = np.asarray(im.convert("RGB"))
        k = min(1.0, t/FADE, (dur-t)/FADE)
        if k < 1.0: rgb = (rgb.astype(np.float32)*max(k,0)).astype(np.uint8)
        p.stdin.write(rgb.tobytes())
    p.stdin.close(); p.wait()
    return outp

def main():
    scenes = SCENES + [dict(id="sources", kind="sources", narration="Sources are listed here. Thanks for watching.")]
    plan = []
    for i, sc in enumerate(scenes):
        wavp, adur = synth(sc)
        lead = 1.2 if i == 0 else 0.9
        dur = lead + adur + 1.4
        plan.append((i, len(scenes), sc, dur, wavp, adur, lead))
        print(f"{sc['id']:>12}: narration {adur:6.1f}s  scene {dur:6.1f}s", flush=True)
    print(f"total ≈ {sum(p[3] for p in plan)/60:.1f} min", flush=True)
    with ProcessPoolExecutor(max_workers=4) as ex:
        vids = list(ex.map(render_scene, [(p[0], p[1], p[2], p[3]) for p in plan]))
    # build narration track: silence lead + wav + tail, per scene, concatenated
    SR = 22050
    chunks = []
    for (i, n, sc, dur, wavp, adur, lead) in plan:
        with wave.open(wavp) as w: data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
        seg = np.zeros(int(round(dur*SR)), dtype=np.float32)
        s = int(lead*SR); seg[s:s+len(data)] = data[:len(seg)-s]
        chunks.append(seg)
    voice = np.concatenate(chunks)
    # gentle ambient pad: detuned sines + slow LFO, very quiet
    T = len(voice)/SR; t = np.arange(len(voice))/SR
    pad = np.zeros_like(voice)
    for fq, amp in [(55, .5), (82.41, .35), (110, .3), (164.81, .2), (220, .12)]:
        pad += amp*np.sin(2*np.pi*fq*t + 0.3*np.sin(2*np.pi*0.05*t))
    pad *= (0.5 + 0.5*np.sin(2*np.pi*0.02*t)) * 0.035
    # fade pad in/out
    fade = int(3*SR); env = np.ones_like(pad); env[:fade] = np.linspace(0,1,fade); env[-fade:] = np.linspace(1,0,fade)
    mix = np.clip(voice*0.95 + pad*env, -1, 1)
    audio_p = os.path.join(OUT, "mix.wav")
    with wave.open(audio_p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
    with open(os.path.join(OUT, "concat.txt"), "w") as fh:
        for v in vids: fh.write(f"file '{v}'\n")
    final = os.path.join(OUT, "722_proofs_in_a_night.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "concat.txt"),
                    "-i", audio_p, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", final], check=True)
    # subtitles (SRT): split narration into sentences, spread proportionally over the narration audio
    import re
    def ts(x): 
        h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
    cue = 1; t0 = 0.0; lines = []
    for (i, n, sc, dur, wavp, adur, lead) in plan:
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', " ".join(sc["narration"].split())) if s.strip()]
        chars = sum(len(s) for s in sents); cur = t0 + lead
        for s in sents:
            d = adur*len(s)/chars
            lines.append(f"{cue}\n{ts(cur)} --> {ts(cur+d-0.05)}\n{s}\n"); cue += 1; cur += d
        t0 += dur
    with open(os.path.join(OUT, "722_proofs_in_a_night.srt"), "w") as fh: fh.write("\n".join(lines))
    print("done:", final)

if __name__ == "__main__": main()
