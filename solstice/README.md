# The Longest Night — a 3-minute solstice art film (proof of concept)

Made for the AI Cafe holiday film festival. Directed by Philip Shane.

Watch: `out/the_longest_night.mp4` (1080p, 24 fps, 2.39:1 letterbox, 3:00).

## How it is made

Everything is generated or drawn from `film.py`, which holds the narration, the shot list with prompts,
the music prompt and the sound-effect list. Change words there, then re-run the two scripts.

| Element | How | Model (all through fal.ai, one API key) |
|---|---|---|
| B-roll, 25 shots × 8 s | text-to-video, 720p, upscaled | Seedance 2.0 Fast (`bytedance/seedance-2.0/fast/text-to-video`) |
| Narration, 7 takes | text-to-speech, voice "George" | ElevenLabs Eleven v3 (`fal-ai/elevenlabs/tts/eleven-v3`) |
| Score, 3 min instrumental | text-to-music | ElevenLabs Music v2.5 (`elevenlabs/music/v2.5`) |
| Wind, drum, fire, crowd, bell, riser | text-to-sound-effect | ElevenLabs Sound Effects v2 |
| Clip ambience | Seedance's own synchronized audio, mixed low | (comes with each clip) |
| Title card, Earth-tilt diagram, end card, captions | drawn in Python (Pillow) | none |

`gen.py` sends every job to fal in parallel and saves results in `assets/` (it skips files that already exist,
so re-running only generates what is missing). `build.py` lays the shots on a 180-second timeline driven by the
narration lengths, crossfades them, applies the film look (grain, softer curve, desaturation, vignette,
letterbox), overlays captions, and mixes voice, music (ducked under the voice), ambience and effects.

```bash
export FAL_KEY=...          # your fal.ai key
python3 gen.py              # ~10 minutes; costs real money (roughly a dollar or two for the whole film)
python3 build.py            # ~4 minutes, no network needed
```

To redo one shot: delete `assets/vNN.mp4`, edit its prompt in `film.py`, run `python3 gen.py vNN`, then `build.py`.
Prompts can include timed beats ("0-3s: ..., 3-8s: ...") and Seedance follows them reasonably well.

## Notes for the next version

- The shots were generated before the style prompt was changed to the documentary/35mm wording now in `film.py`;
  regenerating selected shots will bring them closer to that look.
- The "ancient" feel of the cards is deliberate but slight: ivory ink, paper grain, a woodcut sun, hatched night side.
- Historical claims are kept simple and are broadly accepted (Newgrange c. 3200 BC and its 17-minute beam, Nabta Playa
  c. 5000 BC, Wurdi Youang solstice alignments, Fajada Butte sun dagger, Karnak axis, Machu Picchu's Torreón window).
