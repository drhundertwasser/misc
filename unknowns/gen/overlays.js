// Lettering layout per generated panel: where the caption, bubble, sound effects and credit go.
// Coordinates are in the comic's 1600x900 space. Bubble.tail is the point the tail points at.
// Check a layout with overlay.html?scene=<id>&t=3 composited over out/<NN>-<id>-plate.png.
window.OVERLAYS = {
  hazen: {
    caption: 'COSMOS · UNKNOWN #99',
    bubble: { x: 860, y: 50, w: 520, h: 150, lines: ['Are we alone', 'in the universe?'], tail: [1120, 430] },
    sfx: [{ id: 'blip', t: 2.4, x: 960, y: 560, text: 'BLIP?', color: '#8fd3ff', rot: -10, size: 84 }],
    credit: ['Robert Hazen', 'staff scientist · Carnegie Institution for Science'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  },
  sarcevic: {
    caption: 'PHYSICS · UNKNOWN #40',
    bubble: { x: 400, y: 40, w: 560, h: 160, lines: ['What is', 'dark matter?'], tail: [480, 380] },
    sfx: [{ id: 'nothing', t: 2.7, x: 1160, y: 480, text: '...NOTHING?', color: '#b58cff', rot: -6, size: 64 }],
    credit: ['Ina Sarcevic', 'astrophysicist · University of Arizona'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  },
  lieberman: {
    caption: 'HUMAN ORIGINS · UNKNOWN #37',
    bubble: { x: 560, y: 30, w: 700, h: 160, lines: ['Why are humans the only', 'species with a chin?'], tail: [455, 300] },
    sfx: [{ id: 'hmm', t: 2.4, x: 1000, y: 640, text: 'HMM?', color: '#ff7b2e', rot: -8, size: 90 }],
    credit: ['Daniel Lieberman', 'evolutionary biologist · Harvard University'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  },
  kariko: {
    caption: 'THE BRAIN · UNKNOWN #21',
    bubble: { x: 440, y: 40, w: 560, h: 150, lines: ['Why do we sleep?'], tail: [1200, 330] },
    sfx: [{ id: 'zzz', t: 1.8, x: 300, y: 300, text: 'ZZZ', color: '#b3c6ff', rot: -12, size: 100 }],
    credit: ['Katalin Kariko', 'biochemist · University of Pennsylvania'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  },
  horowitz: {
    caption: 'ANIMALS · UNKNOWN #13',
    bubble: { x: 520, y: 40, w: 760, h: 200, size: 30, lines: ['What kind of information, about people,', 'places and other dogs,', 'can dogs acquire through smell?'], tail: [470, 330] },
    sfx: [{ id: 'sniff', t: 1.5, x: 1100, y: 560, text: 'SNIFF SNIFF', color: '#ffe14d', rot: -4, size: 54 }],
    credit: ['Alexandra Horowitz', 'cognitive scientist · Dog Cognition Lab, Barnard College'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  }
};
