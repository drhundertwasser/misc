# "The Longest Night" v2 — script, shot list, and audio plan for a 3-minute solstice art film.
# One sunrise, watched across seven thousand years. Edit the words here; gen.py makes assets; build.py cuts the film.

DIRECTOR = "Philip Shane"
VOICE = "George"   # ElevenLabs stock voice (warm storyteller). Try "Brian" for a deeper American read.

# Narration. Each entry is one take. 'gap' is the relative weight of the silence BEFORE it; build.py scales gaps to hit 3:00.
SEGMENTS = [
 dict(id="s1", gap=10, text="""Once a year, the night is longer than any other.
Then the sun comes back.
People have waited for this morning for a very long time."""),
 dict(id="s2", gap=7, text="""Goseck, Germany. Seven thousand years ago.
A ring of wooden posts, with a gate cut toward the midwinter sunrise."""),
 dict(id="s3", gap=7, text="""Newgrange, Ireland. Five thousand years old.
Its passage points at the sunrise of the shortest day.
For seventeen minutes, light reaches the back wall."""),
 dict(id="s4", gap=7, text="""Karnak, Egypt. The great temple's axis points at the same sunrise."""),
 dict(id="s5", gap=6, text="""Alexandria. Greek astronomers measured the sun's wandering path.
It is tilted to the sky's equator by about twenty-four degrees.
They had the angle. Not yet the reason."""),
 dict(id="s6", gap=7, text="""Arizona. For centuries, Hopi sun watchers have tracked where the sun rises along the horizon.
When it reaches its southern limit, the winter ceremonies begin."""),
 dict(id="s7", gap=6, text="""Fifteen forty-three. Copernicus.
The Earth circles the sun, and its axis is tilted. That tilt is the whole story.
In December, the north leans away: a low sun, and short days."""),
 dict(id="s8", gap=6, text="""Seventeen twenty-eight. James Bradley, measuring starlight, finds the proof that the Earth really moves."""),
 dict(id="s9", gap=7, text="""Today we know exactly why it happens.
We still come to watch."""),
 dict(id="s10", gap=6, text="""The light is already on its way."""),
]

# Shots. Each belongs to a segment and plays, in order, during that segment's slot.
# kind="gen" is Seedance text-to-video; kind="code" is drawn by build.py (card="angle" | "orbit").
# 'sun' describes the stage of the one continuous sunrise, written into every prompt.
STYLE = ("Documentary footage in the style of a National Geographic film, shot on 35mm motion picture film with visible fine grain, "
         "anamorphic lens, natural available light, atmospheric haze, slightly soft and imperfect, real-world textures, muted "
         "desaturated palette with warm sunlight, slow steady camera move. Not CGI, not a video game, not a 3D render, no glossy "
         "surfaces, no text, no captions, no watermark, no logos.")
SUN = {
 0: "It is deep pre-dawn: the sky is dark blue, only a faint band of light on the eastern horizon.",
 1: "It is the minutes before sunrise: the eastern horizon glows orange, the sun not yet visible.",
 2: "The very first sliver of the sun is just breaking the horizon, a thin blazing edge.",
 3: "The sun is half risen, a semicircle of gold sitting on the horizon, long shadows reaching toward the camera.",
 4: "The full disc of the sun has just cleared the horizon, low and golden, long shadows.",
 5: "The sun is a little above the horizon now, warm and bright, the sky turning pale blue.",
 6: "The sun is climbing, bright white-gold, flooding everything with light.",
}
SHOTS = [
 dict(id="t00", seg="s1", kind="code", card="title"),
 dict(id="w01", seg="s1", sun=0, cap=None, prompt="A vast frozen plain in deep winter, frost and thin snow, mist drifting low, no people, extremely slow dolly forward toward the east."),
 dict(id="w02", seg="s2", sun=0, cap="Goseck", prompt="A large circular enclosure of tall wooden posts in a frosty field in central Europe, neolithic, seen from a low angle, a gap in the ring facing the faint pre-dawn light, slow aerial drift."),
 dict(id="w03", seg="s2", sun=1, cap=None, prompt="A small group of neolithic people in furs and hides standing inside a ring of wooden posts, seen from behind, looking out through a gap in the posts toward the glowing eastern horizon, breath visible, locked camera."),
 dict(id="w04", seg="s3", sun=2, cap="Newgrange", prompt="Newgrange, a huge ancient grass-covered stone mound with a white quartz facade in Ireland, frost on the grass, a few people in wool cloaks waiting at the entrance seen from a distance, slow push in."),
 dict(id="v05", seg="s3", sun=2, cap=None, prompt="(reused from v1) Inside a neolithic stone passage, a beam of golden sunrise light creeping along the stone floor."),
 dict(id="w06", seg="s4", sun=3, cap="Karnak", prompt="Looking down the long central axis of the temple of Karnak in ancient Egypt, colossal columns, two priests in white linen walking slowly away from camera down the axis, mist, slow push in."),
 dict(id="w07", seg="s5", sun=3, cap="Alexandria", prompt="A tall stone gnomon casting a long shadow across a marble courtyard in Hellenistic Alexandria, a scholar in a tunic kneeling to mark the shadow's end with a line, the harbor and lighthouse far behind, slow pan."),
 dict(id="c08", seg="s5", kind="code", card="angle"),
 dict(id="w09", seg="s6", sun=4, cap="Hopi mesas, Arizona", prompt="A lone Hopi sun watcher wrapped in a blanket standing at the edge of a sandstone mesa in Arizona, seen from behind and far away, watching the sun on the horizon over a distant notched ridge, cold desert air, slow push in."),
 dict(id="w10", seg="s6", sun=4, cap=None, prompt="Adobe stone rooftops of a Hopi mesa-top village at sunrise, thin smoke rising from chimneys, a few figures in blankets on the roofs facing the sun, long shadows, slow crane move."),
 dict(id="w11", seg="s7", sun=4, cap="Frombork, 1543", prompt="A sixteenth-century astronomer in dark robes at a tower window in a brick cathedral, seen from behind, a wooden astronomical instrument beside him, morning sun streaming in, dust in the air, slow push in."),
 dict(id="c12", seg="s7", kind="code", card="orbit"),
 dict(id="w13", seg="s8", sun=5, cap="England, 1728", prompt="An eighteenth-century astronomer in a long coat beside a very long brass telescope mounted on a chimney in a quiet garden at morning, seen from a distance, mist, slow drift."),
 dict(id="w14", seg="s9", sun=5, cap="Stonehenge, today", prompt="A modern crowd of thousands at Stonehenge at dawn on the winter solstice, seen from behind, winter coats and hats, breath in the cold, the sun just above the horizon between the stones, many raised phones, documentary handheld feel."),
 dict(id="w15", seg="s9", sun=5, cap=None, prompt="A family of four seen from far behind on a snowy hilltop, watching the low winter sun above a wide valley, a small town below with lights, very slow push in."),
 dict(id="w16", seg="s10", sun=6, cap=None, prompt="Frozen plain at sunrise, the camera facing the sun. 0-4s: the bright low sun over sparkling frost, lens flare. 4-8s: the light grows until the whole image washes out to pure white."),
 dict(id="t17", seg="s10", kind="code", card="end"),
]
for sh in SHOTS:
    if sh.get("kind", "gen") == "gen" and "sun" in sh and not sh["prompt"].startswith("("):
        sh["prompt"] = sh["prompt"] + " " + SUN[sh["sun"]]

MUSIC_PROMPT = ("Slow, haunting, uplifting cinematic score for an art documentary about the winter solstice. "
                "Sparse piano, low string drones, distant wordless choir, a soft frame drum pulse that enters halfway, "
                "building to a warm, hopeful, luminous crescendo at the end, then resolving gently. Instrumental only. 3 minutes.")

SFX = [
 dict(id="wind",  text="Cold wind blowing steadily over ancient stones on an open plain, distant, low, haunting", seconds=20, loop=True),
 dict(id="drum",  text="A single deep ceremonial drum hit with a long cathedral reverb tail", seconds=4),
 dict(id="fire",  text="A log fire crackling in a stone hearth, close, warm", seconds=10),
 dict(id="crowd", text="A quiet crowd murmuring outdoors at dawn in the cold, occasional gasp of awe, birdsong", seconds=10),
 dict(id="bell",  text="A single distant church bell tolling once, reverberant, winter morning", seconds=6),
 dict(id="rise",  text="A slow luminous rising swell, like a sunrise, soft shimmering cinematic riser", seconds=8),
]
