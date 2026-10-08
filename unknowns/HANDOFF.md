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

## Results of the fal.ai test (Oct 8, 2026)

Both runs worked with Seedream 4 (`FAL_KEY` is set in the environment). Outputs in `gen/out/`:

- `01-hazen-edit.png` — image-to-image from `comic/out/frame-01.png`. Same layout, much nicer character
  (expressive face, inked line weights, halftone sky). Text survived almost intact; the caption box reads
  "UNKHOWN" instead of "UNKNOWN", which proves the point that lettering should stay as code.
- `01-hazen-t2i.png` — text-to-image from the prompt only. Richer scene (big dish on a tower, hills, telescope,
  credit strip) and all text spelled correctly this time, but the composition no longer matches our frame.
- `01-hazen-compare.png` — the three stacked with labels (A original, B edit, C text-to-image) for review.

## Next step

1. Owner picks a direction: **B** (edit our frames, keep layout) or **C** (let the model compose, prompt per scene).
2. Either way, strip the lettering from the frame before sending it to the model (render scenes with a
   `--no-text` flag in the comic renderer) and lay caption, bubble, SFX and credit strip back on top in code,
   because the model misspells text (see "UNKHOWN").
3. Repeat for the other ten scenes; keep a consistent seed and style wording so the cast looks like one artist.
4. Then try an image-to-video model on fal (e.g. Kling or Seedance image-to-video) on one finished panel for
   a 3–5 s clip, to decide whether motion comes from the model or stays as our code animation.

## Gotchas

- Playwright is global: prefix node commands that use it with `NODE_PATH=/opt/node-tools/node_modules`.
- Google Fonts load over the network; the renderers wait for `document.fonts.ready`.
- `fal.js` has no dependencies; it uses Node's built-in fetch. Fal is reachable through the proxy.
- Commit rendered outputs the owner needs to see (they open files from the repo in the app).
