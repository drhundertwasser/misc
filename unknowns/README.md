# Unknowns — an animated tour of 100 open questions in science

Source material: "What Are the Biggest Questions in Science Today? 100 Scientists Weigh In"
(The New York Times, Oct. 5, 2026). We use only the questions and the scientists' names, with credit.

## Plan

1. **Style frames** (done) — one still per visual style, each on a different question
   from a different corner of the list. Chosen: 15, comic book.
2. **Sample animation** (done) — eleven questions, one per category, as an animated comic.
   See `comic/README.md`. Video: `comic/out/unknowns-sample.mp4`.
3. (Optional) The full set.

## Folder layout

```
unknowns/
  README.md                 this file
  comic/                    the animated comic (player, scenes, cast, MP4 export)
  styleframes/
    frames/*.html           one self-contained 1600x900 frame per style (SVG + CSS, Google Fonts)
    render.js               Playwright script: renders every frame to out/*.png + a contact sheet
    out/*.png               rendered stills
    out/contact-sheet.png   all frames on one page
```

## Rendering

```
cd unknowns/styleframes
NODE_PATH=/opt/node-tools/node_modules node render.js        # all frames + contact sheet
NODE_PATH=/opt/node-tools/node_modules node render.js 07     # just frames whose name contains "07"
```

Any frame can also be opened directly in a browser; each one is a plain HTML file.

## Style frames

| # | Style | Question | Scientist | Category |
|---|-------|----------|-----------|----------|
| 01 | Paper cutout | 99 Are we alone in the universe? | Robert Hazen | Cosmos |
| 02 | Bold ink line, one accent | 37 Why are humans the only species with a chin? | Daniel Lieberman | Human evolution |
| 03 | Warm mid-century doodle (Anthropic-style A) | 6 What is curiosity? | Victor Ambros | Mind |
| 03b | Warm hands + 2x2 grid (Anthropic-style B) | 58 How do humans create genuinely new concepts? | Alison Gopnik | Mind |
| 04 | Mid-century travel poster | 70 Where are blue whale babies born? | Helen Scales | Animals / ocean |
| 05 | Blueprint | 90 How did the ancient Egyptians build the Great Pyramid? | Mark Lehner | Ancient history |
| 06 | 8-bit pixel art | 36 How do ants produce collective behavior? | Deborah Gordon | Animals |
| 07 | Neon synthwave | 40 What is dark matter? | Ina Sarcevic | Physics |
| 08 | Watercolor | 28 How does a forest canopy create its own climate? | Nalini Nadkarni | Ecology |
| 09 | Risograph two-color | 21 Why do we sleep? | Katalin Kariko | Biology |
| 10 | Crayon picture book | 13 What can dogs learn through smell? | Alexandra Horowitz | Animals / mind |
| 11 | Bauhaus geometric | 10 What is the form of human thought? | Evelina Fedorenko | Brain |
| 12 | Chalkboard | 62 What physics starts and stops earthquakes? | Vashan Wright | Earth |
| 13 | Isometric diorama | 76 Can stem cells grow replacement organs? | Paul Knoepfler | Medicine |
| 14 | Victorian engraving | 88 Who were the Sea Peoples? | Eric H. Cline | Ancient history |
| 15 | Comic book | 95 Can humans survive space radiation and settle off Earth? | Lindy Elkins-Tanton | Future / space |
| 16 | Flat vector, big-limbed | 92 How sensitive are ice sheets to warming? | Sarah Aarons | Climate |
| 17 | Ukiyo-e woodblock | 26 Will climate change raise or lower ocean productivity? | Daniel Sigman | Ocean / climate |

Scientists are drawn as generic, varied figures rather than likenesses of the named people.
