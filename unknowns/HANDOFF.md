# HANDOFF — Unknowns project

Start a new session on branch `claude/brave-wozniak-7nlfcp` and paste:

> Read unknowns/HANDOFF.md and continue from "Next step".

## What this is

An animated short in which a different scientist investigates one question from the NYT's
"100 Unanswered Questions" list (Oct. 5, 2026). The owner is a novice coder; explain steps plainly.

## Decisions so far

- Style: **comic book** (style frame 15 of 18). Thick ink outlines, Ben-Day dots, yellow caption boxes,
  white speech bubbles, Bangers lettering, black credit strip.
- Sample, not all 100: eleven questions, one per category (cosmos, physics, human origins, brain,
  animals, earth, oceans, medicine, ancient history, climate, future).
- Scientists are drawn as generic, varied figures with credit in text, not likenesses of the named people.
- Everything is drawn in code (SVG) so far. Agreed next step: lift image quality by handing frames to an
  image model on fal.ai (Seedream 4 first), then possibly image-to-video.

## What exists

- `styleframes/` — 18 style stills + renderer. Done.
- `comic/` — the animated sample: player (`index.html`), scenes, cast builder, MP4 export.
  Video at `comic/out/unknowns-sample.mp4` (81 s). Done and reviewed.
- `gen/` — fal.ai client (`fal.js`), prompts for frame 1 (Hazen, "Are we alone in the universe?"),
  and the reference frame `comic/out/frame-01.png`. Written and tested without a key (exits cleanly).

## Results so far (Oct 8, 2026)

**Owner chose direction C**: let the image model compose each scene from a prompt, then animate it.

The pipeline that works (all in `gen/`, each step tested on scene 1, Hazen):

1. `fal.js --prompt prompts/01-hazen-notext.txt` → a text-free "plate" (`out/01-hazen-plate.png`). The prompt
   says "absolutely no text" and "exactly two hands" (the first try drew three hands).
2. `fal-video.js --model seedance --fixed --image out/01-hazen-plate.png --prompt prompts/01-hazen-motion.txt`
   → 5 s, 1080p, 24 fps clip with the camera locked (`out/01-hazen-plate-seedance.mp4`). `--model kling` is the
   alternative; both take ~1–2 min.
3. `NODE_PATH=/opt/node-tools/node_modules node compose.js --video <clip> --scene hazen --out <final.mp4>`
   → lays the code-drawn lettering from `overlay.html` + `overlays.js` (caption, bubble, SFX, credit strip,
   cream margin) over the clip frame by frame. Lettering reuses `comic/lib.js`, so it matches the sample issue.

Finals: `out/01-hazen-final-seedance.mp4` and `out/01-hazen-final-kling.mp4`. Earlier experiments kept for
reference: `01-hazen-edit.png` (image-to-image, misspelled "UNKHOWN"), `01-hazen-t2i.png` (panel C with baked-in
text), `01-hazen-seedance.mp4` / `01-hazen-kling.mp4` (animating C directly: text drifted or decayed, which is
why lettering now lives in code).

## Five side-by-sides (Oct 8, 2026)

Scenes 1–5 (Hazen, Sarcevic, Lieberman, Kariko, Horowitz) each exist as `gen/out/NN-<id>-sidebyside.mp4`:
Seedance on the left, Kling on the right, same text-free plate and same code lettering. Per scene the files are
`NN-<id>-plate.png` (chosen plate), `NN-<id>-notext-{1,2}.png` (both candidates), `NN-<id>-plate-{seedance,kling}.mp4`
(raw motion), `NN-<id>-final-{seedance,kling}.mp4` (lettered). Layouts for all five are in `gen/overlays.js`;
`gen/still.js` previews a layout on a plate; `gen/sidebyside.sh` builds the comparison.

Observations: both models keep the camera still and the style intact. Seedance tends to give bigger, more
deliberate character acting (turning, lowering the skull); Kling is calmer and keeps props closer to the plate.
Seedance sometimes exaggerates effects (scene 2's particles grow into magenta blobs). Lettering never breaks
because it is drawn in code.

## Next step

1. Owner picks Seedance or Kling (or per scene). Then generate the remaining six scenes (wright, and scenes 7–11
   from `comic/scenes.js`) the same way: notext prompt → pick of 2 → motion → `overlays.js` entry → compose.
2. Cut all eleven finals together with the cover and "to be continued" cards, compare against
   `comic/out/unknowns-sample.mp4`.
3. Optional polish: per-scene timing so the SFX pops when the action happens; a short crossfade between panels.

## Gotchas

- Playwright is global: prefix node commands that use it with `NODE_PATH=/opt/node-tools/node_modules`.
- Google Fonts load over the network; the renderers wait for `document.fonts.ready`.
- `fal.js` has no dependencies; it uses Node's built-in fetch. Fal is reachable through the proxy.
- Commit rendered outputs the owner needs to see (they open files from the repo in the app).
