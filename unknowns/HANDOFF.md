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

## Next step

1. Confirm the key is present: `echo ${FAL_KEY:+set}` should print `set`. If not, it must be added as an
   **environment variable** named `FAL_KEY` in the cloud environment settings (not a "Network secret":
   Fal needs the header `Authorization: Key …`, which the secret types can't produce).
2. Run the image-to-image test, which keeps our composition and text:
   `cd unknowns/gen && node fal.js --prompt prompts/01-hazen-edit.txt --image ../comic/out/frame-01.png --out out/01-hazen-edit.png`
3. Also run text-to-image for comparison:
   `node fal.js --prompt prompts/01-hazen.txt --out out/01-hazen-t2i.png`
4. Send both images to the owner, side by side with the original frame, and ask which direction to take.
5. Likely follow-up: let the model draw the picture and keep lettering (caption, bubble, credit) as code
   laid over it, because image models misspell text. Then try an image-to-video clip on fal.

## Gotchas

- Playwright is global: prefix node commands that use it with `NODE_PATH=/opt/node-tools/node_modules`.
- Google Fonts load over the network; the renderers wait for `document.fonts.ready`.
- `fal.js` has no dependencies; it uses Node's built-in fetch. Fal is reachable through the proxy.
- Commit rendered outputs the owner needs to see (they open files from the repo in the app).
