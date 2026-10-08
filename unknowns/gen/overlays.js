// Lettering layout per generated panel: where the caption, bubble, sound effects and credit go.
// Coordinates are in the comic's 1600x900 space. Bubble.tail is the point the tail points at.
window.OVERLAYS = {
  hazen: {
    caption: 'COSMOS · UNKNOWN #99',
    bubble: { x: 860, y: 50, w: 520, h: 150, lines: ['Are we alone', 'in the universe?'], tail: [1120, 430] },
    sfx: [{ id: 'blip', t: 2.4, x: 960, y: 560, text: 'BLIP?', color: '#8fd3ff', rot: -10, size: 84 }],
    credit: ['Robert Hazen', 'staff scientist · Carnegie Institution for Science'],
    timing: { cap: 0, cred: .3, bub: 1.0 }
  }
};
