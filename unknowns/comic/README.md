# Unknowns — comic book sample issue

An animated comic in which a different scientist investigates one open question from each
corner of the list. Eleven questions, a cover and an end card, about 81 seconds.

## Watch it

Open `index.html` in a browser (double-click it, or `npx http-server` from this folder).
Space plays and pauses. Left and right arrows step half a second. Shift + arrows jump a scene.
The rendered video is `out/unknowns-sample.mp4`.

## Files

```
comic/
  index.html      player page
  app.js          timeline: cover + scenes + end card; play/pause/scrub; window.__seek(t) for capture
  scenes.js       the eleven scenes: background drawing + per-scene animation
  characters.js   figure(opts): builds a comic-style scientist from skin, hair, outfit, hat, glasses, wheelchair...
  cast.js         the eleven scientists' looks (generic figures, not likenesses)
  lib.js          easing, Ben-Day dots, caption boxes, speech bubbles, SFX lettering, credit strip
  cast.html       a sheet showing the whole cast (handy when tweaking looks)
  export.js       records the animation to MP4 (Playwright + ffmpeg)
  shot.js         screenshot helper: node shot.js index.html out.png 12.5
  out/            rendered video
```

## Editing

Everything is time-driven: each scene's `update(t, P)` sets positions from the clock, so
scrubbing is exact and the video export is deterministic.

- Change a question's wording: edit `bubble.lines` for that scene in `scenes.js`.
- Change how a scientist looks: edit their entry in `cast.js`, open `cast.html` to check.
- Change timing: `SCENE_D` in `app.js` (seconds per scene) and the `t` values on each SFX.
- Add a scene: copy one of the `S.push({...})` blocks in `scenes.js`.

## Rendering the video

```
cd unknowns/comic
NODE_PATH=/opt/node-tools/node_modules node export.js out/unknowns-sample.mp4 30
```

## Scenes

| # | Category | Question | Scientist |
|---|----------|----------|-----------|
| 99 | Cosmos | Are we alone in the universe? | Robert Hazen |
| 40 | Physics | What is dark matter? | Ina Sarcevic |
| 37 | Human origins | Why are humans the only species with a chin? | Daniel Lieberman |
| 21 | The brain | Why do we sleep? | Katalin Kariko |
| 13 | Animals | What can dogs learn through smell? | Alexandra Horowitz |
| 62 | Earth | What physics decides when earthquakes start and stop? | Vashan Wright |
| 70 | Oceans | Where are blue whale babies born? | Helen Scales |
| 76 | Medicine | Can stem cells grow replacement organs? | Paul Knoepfler |
| 90 | Ancient history | How did the ancient Egyptians build the Great Pyramid? | Mark Lehner |
| 92 | Climate | How sensitive are ice sheets to warming? | Sarah Aarons |
| 95 | The future | Can humans survive space radiation and settle off Earth? | Lindy Elkins-Tanton |
