# "The Longest Night" — script, shot list, and audio plan for a 3-minute solstice art film.
# Edit the words here. gen.py generates the assets; build.py cuts the film.

DIRECTOR = "Philip Shane"   # shown on the end card as "Directed by ..."
VOICE = "George"   # ElevenLabs stock voice (warm storyteller). Try "Brian" for a deeper American read.

# Narration segments. Each is spoken as one take so the pacing inside a segment stays natural.
# 'gap' is the silence (seconds) we want BEFORE the segment starts; build.py stretches gaps to hit 3:00.
SEGMENTS = [
 dict(id="s1", gap=9.0, text="""Once a year, the night is longer than any other.
The sun rises late, stays low, and sets early.
People have been watching this for a very long time."""),

 dict(id="s2", gap=4.0, text="""Newgrange, Ireland. Five thousand years old. Older than the pyramids.
Its passage points at one thing: sunrise on the shortest day.
For seventeen minutes, light reaches the back wall."""),

 dict(id="s3", gap=3.0, text="""Stonehenge frames the midwinter sunset.
In the Sahara, a ring of stones at Nabta Playa is older still.
In Australia, the Wadawurrung set out boulders that mark where the sun sets on the shortest day... and the longest."""),

 dict(id="s4", gap=3.0, text="""In New Mexico, a dagger of light crosses a carved spiral.
In Egypt, the solstice sun rose through the gate of Karnak.
In the Andes, a window in a stone tower catches the June dawn. Their midwinter."""),

 dict(id="s5", gap=3.0, text="""In Iran, families stay up all night. Pomegranates, and poetry.
In China and Korea, Dongzhi: dumplings, red bean porridge.
In Japan, a yuzu bath, and a sun goddess who hid in a cave.
In Pakistan, the Kalash light fires for Chaomos.
In Aotearoa, the Pleiades rise before dawn. Matariki.
And in the North: the Yule log."""),

 dict(id="s6", gap=4.0, text="""None of these people met.
They shared one sky, and one question.
Will the light come back?"""),

 dict(id="s7", gap=4.0, text="""It does. Every year.
The Earth is tilted twenty-three and a half degrees. That tilt is the whole story.
So this year, on the longest night, step outside.
You are standing with everyone who ever watched for the sun.
It is already on its way."""),
]

# Shots. Each belongs to a segment and plays, in order, during that segment's slot (gap + narration).
# kind="gen" is Seedance text-to-video; kind="code" is drawn by build.py. 'cap' is the on-screen caption.
STYLE = ("Documentary footage in the style of a National Geographic film, shot on 35mm motion picture film with visible fine grain, "
         "anamorphic lens, natural available light, atmospheric haze, slightly soft and imperfect, real-world textures, muted "
         "desaturated palette with warm sunlight, slow steady camera move. Not CGI, not a video game, not a 3D render, no glossy "
         "surfaces, no text, no captions, no watermark, no logos.")
SHOTS = [
 # intro
 dict(id="t00", seg="s1", kind="code", cap=None, title=True),
 dict(id="v01", seg="s1", cap=None, prompt="Frozen meadow at dawn in deep winter, frost on every blade of grass, mist drifting, the sun just below the horizon turning the sky pale gold, extremely slow dolly forward."),
 dict(id="v02", seg="s1", cap=None, prompt="A low pale winter sun hanging just above a cold grey sea, long path of light on the water, slow drifting sea mist, gentle swell, gulls far away, slow pan."),
 dict(id="v03", seg="s1", cap=None, prompt="A lone distant figure in a wool cloak standing on a snowy hilltop at sunrise, seen from far behind, tiny against an enormous sky, breath visible, very slow push in."),
 # Newgrange
 dict(id="v04", seg="s2", cap="Newgrange, Ireland · about 3200 BC", prompt="Newgrange, a huge ancient grass-covered stone mound with a white quartz facade in Ireland, frost on the grass, pale dawn light, slow aerial drift toward the entrance."),
 dict(id="v05", seg="s2", cap=None, prompt="Inside a neolithic stone passage tomb, rough megalithic walls, a narrow beam of golden sunrise light creeping slowly along the stone floor toward the back chamber, dust in the air, locked-off camera, the light slowly advancing."),
 dict(id="v06", seg="s2", cap=None, prompt="Extreme close-up of ancient carved triple spirals on a weathered grey megalith, a thin line of warm sunlight slowly crossing the carvings, lichen and frost, macro lens, very slow movement."),
 # Stonehenge, Nabta Playa, Wurdi Youang
 dict(id="v07", seg="s3", cap="Stonehenge, England · about 2500 BC", prompt="Stonehenge at midwinter sunset. 0-3s: the low sun hangs just above the horizon beside a giant stone trilithon, long shadows across frosty grass. 3-8s: the camera dollies slowly sideways until the sun sits exactly in the gap between two standing stones and flares. Dramatic cold sky."),
 dict(id="v08", seg="s3", cap="Nabta Playa, Sahara · about 5000 BC", prompt="A small circle of upright weathered sandstone slabs on a flat sandy plain in the Sahara desert at dusk, deep orange sky, a herd of long-horned cattle passing far away in silhouette, slow low tracking shot."),
 dict(id="v09", seg="s3", cap="Wurdi Youang, Australia · Wadawurrung Country", prompt="An egg-shaped arrangement of about one hundred low basalt boulders in dry golden grassland in Victoria, Australia, the sun setting on the horizon in line with the stones, eucalyptus trees in the distance, warm dusty light, slow aerial orbit."),
 # Chaco, Karnak, Machu Picchu
 dict(id="v10", seg="s4", cap="Fajada Butte, Chaco Canyon · about 1000 AD", prompt="Close-up of a spiral petroglyph carved into a sandstone cliff face in a New Mexico desert canyon, three leaning rock slabs beside it, locked camera. 0-8s: a thin dagger-shaped sliver of sunlight slides slowly and steadily across the spiral from top to bottom, passing through its center."),
 dict(id="v11", seg="s4", cap="Karnak, Egypt · about 2000 BC", prompt="Looking down the long central axis of the temple of Karnak at dawn, colossal columns and mist. 0-2s: the gateway at the far end is dark blue. 2-8s: the sun rises exactly inside the great stone gateway, light spills down the axis toward the camera, slow push in."),
 dict(id="v12", seg="s4", cap="Machu Picchu, Peru · about 1450 AD", prompt="Machu Picchu at dawn, clouds drifting through green Andean peaks, a beam of sunrise light passing through a trapezoid window in a curved Inca stone tower, warm light on perfectly fitted stones, slow crane move."),
 # Yalda, Dongzhi, Toji, Amaterasu, Chaomos, Matariki, Yule
 dict(id="v13", seg="s5", cap="Shab-e Yalda · Iran", prompt="A candlelit Persian table on a winter night, halved pomegranates, watermelon, nuts, an open book of poetry, hands of a family reaching for fruit, warm lamplight, intimate, slow pan, no faces visible."),
 dict(id="v14", seg="s5", cap="Dongzhi · China and Korea", prompt="Steam rising from a bamboo steamer of dumplings beside a bowl of red bean porridge in a warm kitchen, a frosted window behind with snow falling outside at night, lantern light, close-up, slow, atmospheric."),
 dict(id="v15", seg="s5", cap="Tōji · Japan", prompt="A traditional Japanese wooden outdoor hot spring bath at night, yellow yuzu fruits floating on the steaming water, snow falling softly onto bamboo and stone lanterns, warm lantern glow, slow push in, no people."),
 dict(id="v16", seg="s5", cap="Amaterasu · Japan", prompt="A dark cave mouth in a misty Japanese forest, mythic, painterly. 0-3s: the cave is sealed by a huge boulder, the forest is dim and blue. 3-6s: the boulder slowly rolls aside. 6-8s: blinding golden light bursts out of the cave and floods the forest, slow and majestic."),
 dict(id="v17", seg="s5", cap="Chaomos · Kalash people, Pakistan", prompt="A great bonfire at night in a snowy mountain village in the Hindu Kush, wooden houses on a steep slope, people in colorful embroidered clothes dancing in a circle around the flames, seen from a distance, sparks rising to the stars, slow drift."),
 dict(id="v18", seg="s5", cap="Matariki · Aotearoa New Zealand", prompt="The Pleiades star cluster rising above a dark New Zealand sea horizon just before dawn in midwinter, cold deep blue sky turning pale, waves on black rocks, a few people in silhouette watching from the shore, slow tilt up."),
 dict(id="v19", seg="s5", cap="Yule · Scandinavia", prompt="A huge log burning in a stone hearth inside a dark wooden longhouse, sparks rising, snow falling outside the open door, faint green northern lights in the sky beyond, slow push toward the fire."),
 # same sky
 dict(id="v20", seg="s6", cap=None, prompt="Time-lapse of star trails circling the pole star above ancient standing stones on a winter night, Milky Way, frost glittering, silent and vast."),
 dict(id="v21", seg="s6", cap=None, prompt="A child's face lit by firelight, looking up at the night sky with wonder, breath visible in the cold, stars reflected in their eyes, slow push in, painterly, cinematic."),
 # the light returns
 dict(id="t22", seg="s7", kind="code", cap=None, tilt=True),
 dict(id="v23", seg="s7", cap="Stonehenge · 21 December, this year", prompt="A modern crowd gathered at Stonehenge at dawn on the winter solstice, people in winter coats, breath in the cold air, documentary handheld feel. 0-4s: the crowd waits in blue pre-dawn light, looking toward the stones. 4-8s: the first sunlight breaks over the stones, warm flare, people raise their phones and arms."),
 dict(id="v24", seg="s7", cap=None, prompt="A busy winter night market street in East Asia with paper lanterns and falling snow, people walking with warm breath, festive lights, slow dolly, cinematic bokeh."),
 dict(id="v25", seg="s7", cap=None, prompt="The Earth seen from space, majestic and slow. 0-4s: the night side glitters with city lights, a thin blue line of dawn on the limb. 4-8s: the sun rises over the curve of the Earth, a brilliant point of light with a soft flare, the terminator sweeping slowly across the oceans."),
 dict(id="v26", seg="s7", cap=None, prompt="A frozen landscape at the moment of sunrise. 0-3s: the horizon glows, frost sparkling, the sky pale. 3-6s: the sun breaks over the horizon, golden light floods the frame with lens flare. 6-8s: the light grows until the whole image washes out to pure white."),
 dict(id="t27", seg="s7", kind="code", cap=None, end=True),
]

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
