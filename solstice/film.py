# "The Longest Night" v3 — two scenes, faces lit by the sunrise behind the camera. Spielberg handheld-documentary mode.
# Edit words and prompts here; gen.py makes assets; build.py cuts the film.

DIRECTOR = "Philip Shane"
VOICE = "George"

# Cheapest Seedance tier: 2.0 Mini at 480p (~$0.07 per second). The 'draft' flag only exists on Seedance 2.5, at 3x the price.
VIDEO = dict(model="bytedance/seedance-2.0/mini/text-to-video", resolution="480p", duration="10")

SEGMENTS = [
 dict(id="s1", gap=9, hold=55, text="""Ireland. Five thousand years ago.
The longest night is ending.
They have come to see whether the sun will return."""),
 dict(id="s2", gap=5, hold=55, text="""England. This morning."""),
 dict(id="s3", gap=3, hold=8, text="""It always comes back."""),
]

# Film look asked for in every prompt. Scene palettes differ: Newgrange cold teal and amber, Stonehenge grey-violet and pink-gold.
STYLE = ("Shot like a Spielberg handheld documentary sequence: 35mm motion picture film, visible fine grain, subtle handheld movement, "
         "natural light only, shallow depth of field, muted desaturated colors, soft halation, real skin texture, real fabric texture, "
         "photorealistic, nothing glossy, not CGI, not a video game, not a 3D render. No text, no captions, no watermark, no logos.")
NEWGRANGE_PEOPLE = ("The people are Neolithic Irish farmers of 3200 BC: black hair, brown eyes, olive southern-European complexions, weathered skin. "
                    "They wear tanned leather and deer-hide garments, fur capes, woven plant-fibre cloaks, leather foot wrappings, bone pins. "
                    "No wool, no metal, no dyed cloth. ")
NEWGRANGE_PLACE = ("The setting is Newgrange in the Boyne valley, Ireland, on the winter solstice morning, deep frost on the grass, hard cold, breath visible. "
                   "Behind the people stands the great mound: a huge dome of earth and loose stones with grass on top, ringed by big grey kerbstones, "
                   "white quartz and dark rounded cobbles scattered on the ground at its foot, a low dark passage entrance with a carved spiral stone lying in front of it. "
                   "The sun is rising behind the camera; the camera looks at the people's faces. ")
STONEHENGE_PLACE = ("The setting is Stonehenge on the morning of the winter solstice today: thousands of people standing inside and around the circle of giant "
                    "lichen-covered sarsen stones, frost on the grass, grey-violet sky turning pink, breath visible, hard cold. People wear puffer jackets, wool "
                    "hats, scarves, gloves; a few wear white druid robes; some hold phones. The sun is rising behind the camera; the camera looks at their faces. ")
LIGHT = ("Timing: 0-4s the faces are in cold blue shadow, waiting. 4-6s the first warm golden sunlight sweeps across their faces from the front, from behind the camera. "
         "6-10s the faces are fully lit by low golden light; they squint slightly; the expressions are subtle, solemn, spiritual, quietly moved, like people "
         "seeing something sacred just past the camera. No smiling, no exaggerated expressions.")

SHOTS = [
 dict(id="t00", seg="s1", kind="code", card="title"),
 # --- Newgrange, c. 3200 BC
 dict(id="n01", seg="s1", cap="Newgrange", pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Handheld wide shot in cold blue pre-dawn light: about forty people stand on frosted grass in front of the great mound, facing the camera, silent, breath rising; families with children, an elder at the front. The sky behind the mound is still dark; faint light on the people's faces from the brightening sky behind the camera."),
 dict(id="n02", seg="s1", cap=None, pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Handheld medium shot of one family: a mother holding a small child wrapped in fur on her hip, a father with his hand on an older boy's shoulder, all looking past the camera toward the horizon, breath visible, cold blue light, waiting in silence. " + LIGHT),
 dict(id="n03", seg="s1", cap=None, pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Handheld medium close-up of an old man at the front of the crowd: deeply lined weathered face, grey-streaked black hair, a long healed scar across one cheek, a fur cape at his shoulders, eyes fixed past the camera. " + LIGHT),
 dict(id="n04", seg="s1", cap=None, pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Handheld medium close-up of a girl of about six, black hair, wrapped in a deer-hide cloak, one hand gripping her mother's cloak, looking past the camera, breath visible. " + LIGHT.replace("quietly moved", "a mix of awe and a little fear")),
 dict(id="n05", seg="s1", cap=None, pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Slow handheld pan across many faces in the crowd as the golden sunrise light sweeps over them from the front, one after another, the great mound and its kerbstones behind them catching the light, a scatter of white quartz glowing at its foot. Solemn, still, breath in the air."),
 dict(id="n06", seg="s1", cap=None, pre=NEWGRANGE_PLACE+NEWGRANGE_PEOPLE,
      prompt="Inside the stone passage, handheld, looking back toward the entrance from the chamber: a thin blade of golden sunlight enters through a slot above the door and creeps along the stone floor toward the camera; two people kneel beside it, their faces lit from below by the reflected light, silent. 0-5s the beam is short; 5-10s it reaches the chamber."),
 dict(id="b06", seg="s2", kind="code", card="black"),
 # --- Stonehenge, today
 dict(id="h07", seg="s2", cap="Stonehenge", pre=STONEHENGE_PLACE,
      prompt="Handheld medium-wide shot, camera low among the front rows, grey-violet pre-dawn light: about twenty people in winter coats and wool hats face the camera, silent, breath rising, a few phone screens glowing, two people in white robes among them; the giant lichen-covered stones are directly behind their shoulders. The sun is behind the camera and never visible; the sky behind the stones stays dim violet. More faces fill the frame than sky."),
 dict(id="h08", seg="s2", cap=None, pre=STONEHENGE_PLACE,
      prompt="Handheld medium shot of a family: a father with a toddler on his shoulders in a knitted hat, a mother beside him with a teenage daughter, all in puffer jackets and scarves, looking past the camera, breath visible, waiting. " + LIGHT),
 dict(id="h09", seg="s2", cap=None, pre=STONEHENGE_PLACE,
      prompt="Handheld medium close-up of an old woman in a wool coat and hat, white hair, deeply lined face, leaning on a walking stick, eyes fixed past the camera, breath visible. " + LIGHT),
 dict(id="h10", seg="s2", cap=None, pre=STONEHENGE_PLACE,
      prompt="Handheld medium close-up of a boy of about eight in a knitted hat and scarf, cheeks red with cold, holding his mother's gloved hand, looking past the camera. " + LIGHT.replace("quietly moved", "a mix of awe and a little fear")),
 dict(id="h11", seg="s2", cap=None, pre=STONEHENGE_PLACE,
      prompt="Slow handheld pan across many faces in the crowd as the golden sunrise light sweeps over them from the front, one after another; a man in a white robe closes his eyes; phones rise; the lichen-covered stones behind them turn warm. Breath in the air, quiet."),
 dict(id="h12", seg="s3", cap=None, pre=STONEHENGE_PLACE,
      prompt="Handheld medium-wide shot, camera low among the front rows: several rows of faces lit by low golden sunlight coming from behind the camera, a man in a white robe at the front with eyes closed, a few arms rising, a soft cheer, drums beginning, breath glowing in the light; the fronts of the great stones glow warm behind them. The sun is behind the camera and never visible in the frame. More faces fill the frame than sky. Slow push in."),
 dict(id="t13", seg="s3", kind="code", card="end"),
]
for sh in SHOTS:
    if sh.get("kind", "gen") == "gen": sh["prompt"] = sh.get("pre", "") + sh["prompt"] + " " + STYLE

MUSIC_PROMPT = ("Slow, haunting, uplifting cinematic score for an art documentary about the winter solstice. "
                "Sparse piano, low string drones, distant wordless choir, a soft frame drum pulse that enters halfway, "
                "building to a warm, hopeful, luminous crescendo at the end, then resolving gently. Instrumental only. 3 minutes.")

SFX = [
 dict(id="wind",  text="Cold wind blowing steadily over ancient stones on an open plain, distant, low, haunting", seconds=20, loop=True),
 dict(id="drum",  text="A single deep ceremonial drum hit with a long cathedral reverb tail", seconds=4),
 dict(id="crowd", text="A quiet crowd murmuring outdoors at dawn in the cold, occasional gasp of awe, birdsong", seconds=10),
 dict(id="cheer", text="A large outdoor crowd cheering and whooping softly as the sun rises, drums starting, distant, cold morning air", seconds=10),
 dict(id="rise",  text="A slow luminous rising swell, like a sunrise, soft shimmering cinematic riser", seconds=8),
]

# Colour grade per scene (ffmpeg filters applied to each clip before the shared film look)
GRADE = {
 "s1": "colorbalance=rs=-0.06:gs=0.01:bs=0.09:rm=-0.02:bm=0.03:rh=0.07:gh=0.03:bh=-0.05",   # Newgrange: teal shadows, amber light
 "s2": "colorbalance=rs=0.02:gs=-0.02:bs=0.07:rh=0.09:gh=0.02:bh=-0.01",                    # Stonehenge: violet shadows, pink-gold light
 "s3": "colorbalance=rs=0.02:gs=-0.02:bs=0.07:rh=0.09:gh=0.02:bh=-0.01",
}
# Light leaks: (shot id, start offset s, end offset s, strength). Timed to the moment the light hits the faces.
LEAKS = [("n02", 3.5, 7.5, 0.5), ("n03", 3.5, 7.5, 0.6), ("n04", 3.5, 7.5, 0.5), ("n05", 0.0, 4.0, 0.45),
         ("h08", 3.5, 7.5, 0.5), ("h09", 3.5, 7.5, 0.6), ("h10", 3.5, 7.5, 0.5), ("h11", 0.0, 4.0, 0.45), ("h12", 0.0, 3.0, 0.7)]
# Sound cues: (sfx id, shot id or absolute seconds, offset s, volume, max length s)
CUES = [("wind", 0.5, 0, 0.35, 48.0), ("drum", "n03", 4.0, 0.6, 6), ("rise", "n05", -1.0, 0.5, 8),
        ("crowd", "h07", 0.0, 0.45, 10), ("drum", "h09", 4.0, 0.5, 6), ("cheer", "h12", 0.5, 0.6, 10), ("rise", "h11", -1.0, 0.5, 8)]
