# Still-frame tests: gritty, realistic faces for the "sun behind the camera" shots. Usage: python3 stills.py
import os, sys, json, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fal_client as fal
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "stills"); os.makedirs(OUT, exist_ok=True)
lock = threading.Lock()
def log(m):
    with lock: print(time.strftime("%H:%M:%S"), m, flush=True)

LOOK = ("Still frame from a Spielberg film shot by Janusz Kaminski on 35mm Kodak film stock: heavy natural grain, soft halation around the highlights, "
        "slightly desaturated muted colors, shallow depth of field, handheld documentary framing, low golden sunrise light coming from behind the camera "
        "onto the faces, cold blue shadows. Real human skin with pores, wind-burn, chapped lips, dirt, broken capillaries; unwashed hair; no makeup; "
        "nothing clean, nothing glossy, not a catalogue costume, not CGI, not a render, not a painting. No text.")
SHOTS = {
 "n03_elder": ("Medium close-up of an old Neolithic Irish man, about sixty, standing at the front of a silent crowd outside the Newgrange mound in Ireland "
               "around 3200 BC on the winter solstice morning. Black hair gone grey, long and matted; brown eyes; olive weathered skin; a long old healed scar "
               "across one cheek; a missing tooth; a cape of smoke-stained deer hide and fur tied with a bone pin. Breath visible in hard frost. He gazes just past "
               "the camera, solemn and quietly moved, as the first sunlight touches his face. Behind him, out of focus: the great mound of earth and loose stone, "
               "big grey kerbstones, white quartz scattered on frosted grass, other people in hides. "),
 "n02_family": ("Medium shot of a Neolithic Irish family outside the Newgrange mound in Ireland around 3200 BC on the winter solstice morning: a mother with "
                "black hair holding a small child wrapped in fur on her hip, a father with a weathered olive face and his hand on an older boy's shoulder. "
                "Clothes of tanned hide, fur and woven plant fibre, dirty and worn, no wool, no metal, no dye. Breath visible in hard frost. All three look just past "
                "the camera, solemn, as the first golden sunlight touches their faces. Behind them, out of focus: the mound, big grey kerbstones, frosted grass. "),
 "h09_woman": ("Medium close-up of a very old English woman, about eighty-five, at the winter solstice sunrise at Stonehenge today: white hair under a wool hat, "
               "deeply lined face, watery eyes, thin lips, an old waxed coat and a hand-knitted scarf, leaning on a walking stick, breath visible in the frost. "
               "She gazes just past the camera, solemn and quietly moved, as the first golden sunlight touches her face. Behind her, out of focus: a dense crowd "
               "in winter coats and hats, a figure in a white robe, and the giant lichen-covered sarsen stones against a grey-violet dawn sky. "),
}
MODELS = {
 "gpt25": ("openai/gpt-image-2.5/flare/text-to-image", lambda p: dict(prompt=p, quality="high", image_size="landscape_16_9", output_format="jpeg", num_images=1)),
 "sd5":   ("bytedance/seedream/v5/text-to-image",      lambda p: dict(prompt=p, image_size="landscape_16_9", output_format="jpeg", num_images=1)),
}
def job(shot, model, k):
    p = os.path.join(OUT, f"{shot}_{model}_{k}.jpg")
    if os.path.exists(p): return p
    mid, mk = MODELS[model]
    try: res = fal.run(mid, mk(SHOTS[shot] + LOOK), log)
    except Exception as e:
        if model == "sd5":   # fall back to the flash variant if the full model refuses the request
            res = fal.run("bytedance/seedream/v5/flash/text-to-image", mk(SHOTS[shot] + LOOK), log)
        else: raise
    url = fal.first_url(res)
    if not url: raise RuntimeError(f"no image url: {json.dumps(res)[:300]}")
    fal.download(url, p); json.dump({k_: v for k_, v in res.items() if k_ != "images"}, open(p + ".json", "w")); return p

if __name__ == "__main__":
    jobs = [(s, m, k) for s in SHOTS for m in MODELS for k in (1, 2)]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(job, *j): j for j in jobs}
        for f in as_completed(futs):
            try: log(f"DONE {futs[f]} -> {os.path.basename(f.result())}")
            except Exception as e: log(f"FAILED {futs[f]}: {str(e)[:300]}")
    # contact sheet: rows = shots, columns = gpt25 x2, sd5 x2
    from PIL import Image, ImageDraw, ImageFont
    cw, ch = 640, 360; cols = [(m, k) for m in MODELS for k in (1, 2)]
    sheet = Image.new("RGB", (cw*4, (ch+34)*len(SHOTS)), (0, 0, 0)); d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 22)
    for r, s in enumerate(SHOTS):
        for c, (m, k) in enumerate(cols):
            p = os.path.join(OUT, f"{s}_{m}_{k}.jpg")
            if os.path.exists(p):
                im = Image.open(p).convert("RGB"); im.thumbnail((cw, ch)); sheet.paste(im, (c*cw + (cw-im.width)//2, r*(ch+34) + 34))
            d.text((c*cw + 8, r*(ch+34) + 6), f"{s}  ·  {'GPT Image 2.5' if m=='gpt25' else 'Seedream 5'}  #{k}", font=f, fill=(230, 230, 230))
    sheet.save(os.path.join(OUT, "contact.jpg"), quality=88); print("contact sheet:", os.path.join(OUT, "contact.jpg"))
