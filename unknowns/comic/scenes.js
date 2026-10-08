// Scene definitions. Each scene: id, caption, figure placement, background SVG, bubble, SFX list,
// credit, and an update(t, P) that animates parts. t is local seconds (0..D). P is the part map.
window.SCENES = (() => {
  const { dots, INK, OUT, OUT5, prog, lerp, easeOut, easeInOut, pop, clamp } = U;
  const sp = window.setPart;
  const sky = (id, c1, c2, dotColor, h = 560) =>
    `<linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/></linearGradient>${dots(id + '-d', dotColor)}` +
    `<rect x="30" y="30" width="1540" height="840" fill="url(#${id}-sky)"/><rect x="30" y="30" width="1540" height="${h}" fill="url(#${id}-d)"/>`;
  // mouth position of a figure placed at (x,y,scale): used as the bubble tail target
  const mouth = (x, y, s) => [x, y - 276 * s];
  const wob = (t, f, a) => Math.sin(t * f * Math.PI * 2) * a;

  const S = [];

  // 1 ─ COSMOS · 99 · Robert Hazen ────────────────────────────────────────────────
  S.push({
    id: 'hazen', caption: 'COSMOS · UNKNOWN #99', credit: ['Robert Hazen', 'staff scientist · Carnegie Institution for Science'],
    fig: { who: 'hazen', x: 470, y: 790, s: .95 },
    bubble: { x: 70, y: 150, w: 620, h: 160, lines: ['Are we alone', 'in the universe?'] },
    sfx: [{ id: 'blip', t: 2.45, x: 1210, y: 330, text: 'BLIP?', color: '#8fd3ff', rot: -10, size: 96 }],
    svg() {
      let stars = ''; for (let i = 0; i < 26; i++) { const x = 60 + ((i * 137) % 1480), y = 60 + ((i * 251) % 380); stars += `<circle data-id="st${i}" cx="${x}" cy="${y}" r="${3 + (i % 3)}" fill="#fff"/>`; }
      return sky('hz', '#0b1a3a', '#24396c', '#2f4a80') + stars +
        `<circle cx="1380" cy="150" r="60" fill="#fff3c4" ${OUT}/><circle cx="1402" cy="132" r="52" fill="#0b1a3a" stroke="none"/><circle cx="1380" cy="150" r="60" fill="none" ${OUT}/>` +
        `<path d="M30 640 Q400 560 800 630 T1570 640 V870 H30Z" fill="#1f5d5a" ${OUT}/><path d="M30 740 Q500 680 1000 740 T1570 760 V870 H30Z" fill="#2f8a73" ${OUT}/>` +
        // dish on a mast
        `<rect x="1180" y="520" width="34" height="240" fill="#c9cfd6" ${OUT}/><rect x="1120" y="750" width="154" height="30" rx="8" fill="#aab2bc" ${OUT}/>` +
        `<g data-id="dish" data-pivot="1197 520"><g transform="translate(1197 520) rotate(-30)"><path d="M-170 0 A170 170 0 0 1 170 0 L170 44 A190 190 0 0 0 -170 44Z" fill="#f4f1ea" ${OUT}/><path d="M0 0 L0 -160" stroke="${INK}" stroke-width="12"/><circle cx="0" cy="-165" r="20" fill="#ff9d5c" ${OUT}/></g></g>` +
        // console
        `<rect x="640" y="600" width="380" height="180" rx="10" fill="#3b4a6b" ${OUT}/><rect x="670" y="625" width="320" height="110" rx="6" fill="#0b1a3a" ${OUT5}/>` +
        `<path d="M690 680 H980" stroke="#5bd1a5" stroke-width="4"/><g data-id="spike" data-pivot="840 680"><path d="M800 680 L815 650 L830 715 L845 640 L860 705 L875 680" fill="none" stroke="#5bd1a5" stroke-width="6" stroke-linejoin="round"/></g>` +
        `<rect x="700" y="745" width="60" height="18" fill="#ff3b3b" ${OUT5} stroke-width="3"/><rect x="780" y="745" width="60" height="18" fill="#ffe14d" ${OUT5} stroke-width="3"/>`;
    },
    update(t, P) {
      P.dish.setAttribute('transform', `rotate(${wob(t, .12, 10)} 1197 520)`);
      for (let i = 0; i < 26; i++) P['st' + i].setAttribute('opacity', .5 + .5 * Math.sin(t * 3 + i));
      const hit = pop(prog(t, 2.4, 2.75)); U.setPop(P.spike, hit);
      sp(P['hazen.head'], -10 * hit + wob(t, .6, 2));
      sp(P['hazen.armR'], -95 * pop(prog(t, 2.6, 3.1)));
      sp(P['hazen.armL'], wob(t, .8, 4));
      P['hazen.body'].setAttribute('transform', `translate(0 ${wob(t, 1.2, 2)})`);
    }
  });

  // 2 ─ PHYSICS · 40 · Ina Sarcevic ───────────────────────────────────────────────
  S.push({
    id: 'sarcevic', caption: 'PHYSICS · UNKNOWN #40', credit: ['Ina Sarcevic', 'astrophysicist · University of Arizona'],
    fig: { who: 'sarcevic', x: 430, y: 800, s: .95 },
    bubble: { x: 70, y: 150, w: 560, h: 160, lines: ['What is', 'dark matter?'] },
    sfx: [{ id: 'nothing', t: 2.7, x: 1130, y: 190, text: '...NOTHING?', color: '#b58cff', rot: -6, size: 70 }],
    svg() {
      let parts = ''; for (let i = 0; i < 9; i++) { const x = 760 + ((i * 97) % 760); parts += `<g data-id="p${i}"><circle cx="${x}" cy="0" r="18" fill="none" stroke="#b58cff" stroke-width="4" stroke-dasharray="6 6"/><text x="${x}" y="7" text-anchor="middle" font-family="Bangers" font-size="22" fill="#b58cff">?</text></g>`; }
      return sky('sv', '#2b2b3a', '#3a3a4a', '#262633', 840) +
        `<path d="M30 30 L30 870 L160 870 L120 700 L170 520 L110 360 L150 200 L100 30Z" fill="#4a4a5c" ${OUT}/><path d="M1570 30 L1570 870 L1440 870 L1480 700 L1430 520 L1490 360 L1450 200 L1500 30Z" fill="#4a4a5c" ${OUT}/>` +
        `<rect x="30" y="790" width="1540" height="80" fill="#5a5a6e" ${OUT}/>` +
        // detector tank
        `<rect x="760" y="300" width="560" height="440" rx="30" fill="#aab8c8" ${OUT}/><rect x="820" y="360" width="440" height="320" rx="20" fill="#1b2d5a" ${OUT}/>` +
        `<rect x="840" y="380" width="400" height="280" rx="14" fill="#2f4ec2" opacity=".7"/><path d="M840 420 H1240" stroke="#8fd3ff" stroke-width="6"/>` +
        `<rect x="900" y="250" width="280" height="50" rx="8" fill="#ffe14d" ${OUT}/><text x="1040" y="287" text-anchor="middle" font-family="Bangers" font-size="30" fill="${INK}">DETECTOR · 1 KM DOWN</text>` +
        `<rect x="1330" y="500" width="160" height="90" rx="8" fill="#111" ${OUT}/><text data-id="hits" x="1410" y="562" text-anchor="middle" font-family="Bangers" font-size="44" fill="#5bd1a5">0 HITS</text>` +
        `<path d="M1320 400 L1360 400 L1360 500" stroke="${INK}" stroke-width="10" fill="none"/>` +
        parts;
    },
    update(t, P) {
      for (let i = 0; i < 9; i++) { const y = (t * 260 + i * 140) % 1000; P['p' + i].setAttribute('transform', `translate(0 ${y - 60})`); P['p' + i].setAttribute('opacity', y > 40 && y < 880 ? 1 : 0); }
      const sh = pop(prog(t, 2.5, 2.9));
      sp(P['sarcevic.armL'], 48 * sh); sp(P['sarcevic.armR'], -48 * sh);
      sp(P['sarcevic.head'], 9 * sh + wob(t, .5, 2));
      P.hits.textContent = t > 4.5 ? 'STILL 0' : '0 HITS';
    }
  });

  // 3 ─ HUMAN ORIGINS · 37 · Daniel Lieberman ─────────────────────────────────────
  S.push({
    id: 'lieberman', caption: 'HUMAN ORIGINS · UNKNOWN #37', credit: ['Daniel Lieberman', 'evolutionary biologist · Harvard University'],
    fig: { who: 'lieberman', x: 560, y: 800, s: .95, mouth: 'hmm', prop: skullProp() },
    bubble: { x: 70, y: 150, w: 700, h: 160, lines: ['Why are humans the only', 'species with a chin?'] },
    sfx: [{ id: 'hmm', t: 2.4, x: 900, y: 330, text: 'HMM?', color: '#ff7b2e', rot: -8, size: 100 }],
    svg() {
      return sky('lb', '#f3e6c8', '#e8d6b0', '#dcc89c', 840) +
        `<rect x="30" y="760" width="1540" height="110" fill="#8b5a2b" ${OUT}/>` +
        `<rect x="900" y="200" width="600" height="26" fill="#c9a86a" ${OUT}/><rect x="900" y="420" width="600" height="26" fill="#c9a86a" ${OUT}/>` +
        [960, 1120, 1280, 1400].map((x, i) => miniSkull(x, 160 + (i % 2) * 220 - (i % 2) * 0, .8)).join('') +
        `<rect x="1000" y="640" width="440" height="120" rx="8" fill="#5b6b8c" ${OUT}/><rect x="1020" y="600" width="400" height="40" fill="#8aa3b8" ${OUT}/>` +
        `<g data-id="ring" data-pivot="560 560"><circle cx="560" cy="560" r="58" fill="none" stroke="#e63946" stroke-width="8" stroke-dasharray="4 14"/><path d="M620 560 L720 560" stroke="#e63946" stroke-width="7" stroke-dasharray="14 12"/></g>`;
    },
    update(t, P) {
      sp(P['lieberman.armR'], -105 * pop(prog(t, .5, 1.1)));
      sp(P['lieberman.head'], 6 * pop(prog(t, 2.2, 2.6)) + wob(t, .5, 2));
      sp(P['lieberman.armL'], -20 * easeInOut(prog(t, 3.2, 3.8)));
      U.setPop(P.ring, pop(prog(t, 2.2, 2.6)));
    }
  });
  function skullProp() { return `<g transform="translate(0 -40) scale(.9)"><path d="M-34 0 C-34 -50 34 -50 34 0 L30 20 L18 24 L18 40 L-18 40 L-18 24 L-30 20Z" fill="#f4f1ea" ${OUT5}/><circle cx="-13" cy="-8" r="9" fill="${INK}"/><circle cx="13" cy="-8" r="9" fill="${INK}"/><path d="M-4 10 L0 4 L4 10Z" fill="${INK}"/><path d="M-12 26 V38 M-4 26 V40 M4 26 V40 M12 26 V38" stroke="${INK}" stroke-width="3"/></g>`; }
  function miniSkull(x, y, s) { return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-34 0 C-34 -50 34 -50 34 0 L30 20 L18 24 L18 40 L-18 40 L-18 24 L-30 20Z" fill="#f4f1ea" ${OUT5}/><circle cx="-13" cy="-8" r="9" fill="${INK}"/><circle cx="13" cy="-8" r="9" fill="${INK}"/><path d="M-12 26 V38 M-4 26 V40 M4 26 V40 M12 26 V38" stroke="${INK}" stroke-width="3"/></g>`; }

  // 4 ─ THE BRAIN · 21 · Katalin Kariko ───────────────────────────────────────────
  S.push({
    id: 'kariko', caption: 'THE BRAIN · UNKNOWN #21', credit: ['Katalin Kariko', 'biochemist · University of Pennsylvania'],
    fig: { who: 'kariko', x: 1180, y: 800, s: .95, prop: clipboardProp() },
    bubble: { x: 780, y: 140, w: 560, h: 150, lines: ['Why do we sleep?'], tail: [1180, 520] },
    sfx: [{ id: 'zzz', t: 1.8, x: 560, y: 300, text: 'ZZZ', color: '#b3c6ff', rot: -12, size: 110 }],
    svg() {
      const eeg = []; for (let x = 0; x <= 1200; x += 20) eeg.push(`${x} ${[0, -18, 26, -40, 12, -8, 30, -22, 6][(x / 20) % 9]}`);
      return sky('kk', '#cdbdf0', '#b8a6e6', '#a893dd', 840) +
        `<rect x="30" y="760" width="1540" height="110" fill="#6c5ce7" ${OUT}/>` +
        // bed
        `<rect x="120" y="560" width="620" height="60" fill="#5b6b8c" ${OUT}/><rect x="120" y="620" width="26" height="140" fill="#5b6b8c" ${OUT}/><rect x="714" y="620" width="26" height="140" fill="#5b6b8c" ${OUT}/><rect x="120" y="420" width="26" height="150" fill="#5b6b8c" ${OUT}/>` +
        `<rect x="150" y="470" width="190" height="90" rx="30" fill="#fff" ${OUT}/>` +
        `<path d="M150 560 C300 500 560 500 740 560 L740 600 L150 600Z" fill="#ff6b8a" ${OUT}/>` +
        `<circle cx="250" cy="500" r="42" fill="#8d5524" ${OUT}/><path d="M212 490 C215 450 285 450 288 490 C270 478 230 478 212 490Z" fill="#222" ${OUT}/><path d="M232 505 q8 7 16 0 M254 505 q8 7 16 0" fill="none" stroke="${INK}" stroke-width="4"/><path d="M240 522 q10 6 20 0" fill="none" stroke="${INK}" stroke-width="3"/>` +
        `<path d="M280 480 C400 300 700 300 900 420" stroke="${INK}" stroke-width="4" fill="none" stroke-dasharray="10 8"/>` +
        // monitor
        `<rect x="820" y="330" width="320" height="220" rx="10" fill="#1b2d5a" ${OUT}/><rect x="840" y="350" width="280" height="180" fill="#0b1a3a"/><clipPath id="kk-clip"><rect x="840" y="350" width="280" height="180"/></clipPath>` +
        `<g clip-path="url(#kk-clip)"><g data-id="eeg" transform="translate(840 440)"><path d="M${eeg.join(' L')}" fill="none" stroke="#5bd1a5" stroke-width="4" stroke-linejoin="round"/></g></g>` +
        `<rect x="960" y="550" width="40" height="60" fill="#1b2d5a" ${OUT}/><rect x="900" y="610" width="160" height="16" fill="#1b2d5a" ${OUT}/>` +
        [0, 1, 2].map(i => `<text data-id="z${i}" x="${330 + i * 50}" y="440" font-family="Bangers" font-size="${44 + i * 14}" fill="#fff" stroke="${INK}" stroke-width="5" paint-order="stroke">z</text>`).join('');
    },
    update(t, P) {
      P.eeg.setAttribute('transform', `translate(${840 - ((t * 180) % 360)} 440)`);
      for (let i = 0; i < 3; i++) { const ph = (t * .5 + i * .33) % 1; P['z' + i].setAttribute('transform', `translate(${ph * 60} ${-ph * 160})`); P['z' + i].setAttribute('opacity', 1 - ph); }
      sp(P['kariko.armR'], -30 + wob(t, 2.5, 6));
      sp(P['kariko.head'], -4 + wob(t, .4, 3));
      sp(P['kariko.armL'], wob(t, .5, 3));
    }
  });
  function clipboardProp() { return `<g transform="translate(6 -30) rotate(10)"><rect x="-28" y="-40" width="56" height="76" rx="4" fill="#c9a86a" ${OUT5}/><rect x="-22" y="-34" width="44" height="64" fill="#fff"/><path d="M-14 -16 H14 M-14 -4 H14 M-14 8 H8" stroke="${INK}" stroke-width="3"/><rect x="-10" y="-46" width="20" height="12" rx="3" fill="#555"/></g>`; }

  // 5 ─ ANIMALS · 13 · Alexandra Horowitz ─────────────────────────────────────────
  S.push({
    id: 'horowitz', caption: 'ANIMALS · UNKNOWN #13', credit: ['Alexandra Horowitz', 'cognitive scientist · Dog Cognition Lab, Barnard College'],
    fig: { who: 'horowitz', x: 380, y: 790, s: .95, prop: notebookProp() },
    bubble: { x: 60, y: 140, w: 760, h: 200, size: 30, lines: ['What kind of information, about people,', 'places and other dogs,', 'can dogs acquire through smell?'] },
    sfx: [{ id: 'sniff', t: 1.5, x: 1090, y: 672, text: 'SNIFF SNIFF', color: '#ffe14d', rot: -4, size: 54 }],
    svg() {
      return sky('hw', '#9ad7ff', '#d8f0ff', '#7cc4f5', 560) +
        `<circle cx="1400" cy="150" r="70" fill="#ffe14d" ${OUT}/>` +
        `<path d="M30 760 Q400 720 800 760 T1570 760 V870 H30Z" fill="#3aa655" ${OUT}/>` +
        `<rect x="30" y="700" width="1540" height="70" fill="#5bbf6a"/><path d="M30 700 H1570" stroke="${INK}" stroke-width="7"/>` +
        // tree
        `<rect x="1430" y="420" width="50" height="300" fill="#8b5a2b" ${OUT}/><circle cx="1455" cy="400" r="120" fill="#2f8a4b" ${OUT}/>` +
        // hydrant
        `<rect x="1230" y="560" width="70" height="160" rx="16" fill="#e63946" ${OUT}/><circle cx="1265" cy="550" r="30" fill="#e63946" ${OUT}/><rect x="1200" y="615" width="130" height="30" rx="10" fill="#e63946" ${OUT}/>` +
        // scent wisps
        [0, 1, 2].map(i => `<path data-id="w${i}" d="M${1230 + i * 30} 520 c-20 -40 20 -60 0 -100 c-15 -30 15 -50 0 -80" fill="none" stroke="#9b59b6" stroke-width="7" stroke-dasharray="2 14" stroke-linecap="round"/>`).join('') +
        // dog
        `<g data-id="dog" transform="translate(900 700)">` +
        `<g data-id="tail" data-pivot="-140 -60"><path d="M-140 -60 C-190 -100 -200 -150 -170 -170" fill="none" stroke="${INK}" stroke-width="28"/><path d="M-140 -60 C-190 -100 -200 -150 -170 -170" fill="none" stroke="#8b5a2b" stroke-width="16"/></g>` +
        `<ellipse cx="-40" cy="-80" rx="150" ry="70" fill="#8b5a2b" ${OUT}/>` +
        `<path d="M-140 -30 L-150 20 M-80 -20 L-80 20 M20 -20 L20 20 M80 -30 L90 20" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="M-140 -30 L-150 20 M-80 -20 L-80 20 M20 -20 L20 20 M80 -30 L90 20" stroke="#8b5a2b" stroke-width="18" stroke-linecap="round"/>` +
        `<g data-id="doghead" data-pivot="110 -110"><circle cx="150" cy="-120" r="60" fill="#8b5a2b" ${OUT}/><path d="M190 -112 L265 -90 L250 -62 L185 -72Z" fill="#8b5a2b" ${OUT}/><circle cx="268" cy="-86" r="13" fill="${INK}"/>` +
        `<path d="M110 -150 C70 -120 80 -60 120 -60" stroke="${INK}" stroke-width="36" fill="none" stroke-linecap="round"/><path d="M110 -150 C70 -120 80 -60 120 -60" stroke="#6b3f2a" stroke-width="24" fill="none" stroke-linecap="round"/>` +
        `<ellipse cx="165" cy="-130" rx="9" ry="12" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="167" cy="-128" r="4" fill="${INK}"/><path d="M200 -70 q14 10 28 -2" stroke="${INK}" stroke-width="4" fill="none"/></g></g>` +
        // thought cloud
        `<g data-id="cloud" data-pivot="1120 560"><circle cx="1110" cy="545" r="10" fill="#fff" ${OUT5}/><circle cx="1130" cy="505" r="16" fill="#fff" ${OUT5}/>` +
        `<path d="M1010 420 c-50 -70 50 -130 100 -80 c40 -70 160 -60 160 10 c70 0 80 90 10 100 c-10 60 -110 70 -140 20 c-60 40 -150 0 -130 -50z" fill="#fff" ${OUT}/>` +
        `<g data-id="ic0" data-pivot="1060 410"><path d="M1040 420 l40 -20" stroke="#8b5a2b" stroke-width="8"/><circle cx="1036" cy="412" r="10" fill="#8b5a2b" ${OUT5} stroke-width="3"/><circle cx="1044" cy="426" r="10" fill="#8b5a2b" ${OUT5} stroke-width="3"/><circle cx="1076" cy="392" r="10" fill="#8b5a2b" ${OUT5} stroke-width="3"/><circle cx="1084" cy="406" r="10" fill="#8b5a2b" ${OUT5} stroke-width="3"/></g>` +
        `<g data-id="ic1" data-pivot="1150 410"><circle cx="1150" cy="412" r="26" fill="#aaa" ${OUT5}/><path d="M1130 392 l-8 -22 l20 10 M1170 392 l8 -22 l-20 10" fill="#aaa" ${OUT5}/><circle cx="1140" cy="408" r="3" fill="${INK}"/><circle cx="1160" cy="408" r="3" fill="${INK}"/></g>` +
        `<g data-id="ic2" data-pivot="1235 415"><ellipse cx="1230" cy="420" rx="30" ry="18" fill="#ff7b2e" ${OUT5}/><circle cx="1258" cy="406" r="13" fill="#ff7b2e" ${OUT5}/><circle cx="1262" cy="404" r="3" fill="${INK}"/></g></g>`;
    },
    update(t, P) {
      for (let i = 0; i < 3; i++) { const ph = (t * .4 + i * .33) % 1; P['w' + i].setAttribute('transform', `translate(0 ${-ph * 120})`); P['w' + i].setAttribute('opacity', 1 - ph); }
      sp(P.doghead, 8 * Math.sin(t * 14) * (t < 4 ? 1 : .3) + 10);
      sp(P.tail, wob(t, 3, 18));
      P.dog.setAttribute('transform', `translate(${900 + wob(t, .3, 10)} 700)`);
      U.setPop(P.cloud, pop(prog(t, 2.0, 2.4)));
      U.setPop(P.ic0, pop(prog(t, 2.3, 2.6))); U.setPop(P.ic1, pop(prog(t, 2.7, 3.0))); U.setPop(P.ic2, pop(prog(t, 3.1, 3.4)));
      sp(P['horowitz.armR'], -20 + wob(t, 2, 5)); sp(P['horowitz.head'], 6 + wob(t, .5, 3));
      P['horowitz.pupils'].setAttribute('transform', `translate(${4 * pop(prog(t, 1.3, 1.7))} 0)`);
    }
  });
  function notebookProp() { return `<g transform="translate(4 -26) rotate(-8)"><rect x="-26" y="-34" width="52" height="68" rx="4" fill="#ffe14d" ${OUT5}/><path d="M-14 -16 H14 M-14 -4 H14 M-14 8 H6" stroke="${INK}" stroke-width="3"/></g>`; }

  // 6 ─ EARTH · 62 · Vashan Wright ────────────────────────────────────────────────
  S.push({
    id: 'wright', caption: 'EARTH · UNKNOWN #62', credit: ['Vashan Wright', 'geophysicist · UC San Diego'], bubbleT: 3.7,
    fig: { who: 'wright', x: 440, y: 790, s: .95, prop: hammerProp() },
    bubble: { x: 70, y: 150, w: 720, h: 160, lines: ['What physics decides when', 'earthquakes start and stop?'] },
    sfx: [{ id: 'rumble', t: 2.05, x: 1000, y: 250, text: 'RUMMBLE', color: '#ff7b2e', rot: -5, size: 120 }],
    svg() {
      return `<g data-id="world">` + sky('wr', '#f7b267', '#f4845f', '#f79d65', 500) +
        `<circle cx="1300" cy="170" r="80" fill="#ffe14d" ${OUT}/>` +
        `<path d="M30 520 L500 380 L900 470 L1250 360 L1570 450 V870 H30Z" fill="#c8502d" ${OUT}/>` +
        `<path d="M30 640 H760 L800 600 H1570 V870 H30Z" fill="#d9a066" ${OUT}/><path d="M30 700 H740 M30 760 H720 M820 660 H1570 M800 720 H1570" stroke="${INK}" stroke-width="4" opacity=".5"/>` +
        `<path d="M760 640 L800 600 L820 870 L780 870Z" fill="#a8432a" ${OUT}/>` +
        `<g data-id="crack"><path data-id="crackp" d="M790 640 L830 690 L800 740 L850 800 L820 870" fill="none" stroke="${INK}" stroke-width="9" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></g>` +
        // seismograph on a table
        `<rect x="960" y="560" width="360" height="24" fill="#8b5a2b" ${OUT}/><rect x="990" y="584" width="24" height="120" fill="#8b5a2b" ${OUT}/><rect x="1266" y="584" width="24" height="120" fill="#8b5a2b" ${OUT}/>` +
        `<rect x="990" y="440" width="300" height="120" rx="8" fill="#dfe6f3" ${OUT}/><rect x="1010" y="460" width="260" height="80" fill="#fff" ${OUT5}/>` +
        `<path data-id="trace" d="M1020 500 h40 l3 -6 l3 6 h30 l4 -10 l4 10 h20 l6 -40 l6 70 l6 -90 l6 110 l6 -80 l6 60 l6 -40 l6 30 l6 -20 l6 14 l6 -10 l30 0 l3 -6 l3 6 h40" fill="none" stroke="#e63946" stroke-width="4" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>` +
        `<g data-id="pen" data-pivot="1140 430"><path d="M1140 430 L1140 500" stroke="${INK}" stroke-width="8"/><circle cx="1140" cy="430" r="10" fill="#e63946" ${OUT5}/></g>` +
        `</g>`;
    },
    update(t, P) {
      const q = prog(t, 2.0, 3.6), env = q > 0 && q < 1 ? Math.sin(q * Math.PI) : 0;
      const jx = env * 22 * Math.sin(t * 60), jy = env * 14 * Math.sin(t * 73 + 1);
      P.world.setAttribute('transform', `translate(${jx} ${jy})`);
      P.crackp.setAttribute('stroke-dashoffset', 1 - easeOut(prog(t, 2.1, 3.2)));
      P.trace.setAttribute('stroke-dashoffset', 1 - prog(t, 1.2, 4.2));
      sp(P.pen, 0, jx * 1.5, 0);
      sp(P['wright.armL'], 50 * env + wob(t, .6, 3)); sp(P['wright.armR'], -60 * env - 10);
      sp(P['wright.head'], -8 * env + wob(t, .5, 2), jx * .4, 0);
      P['wright.body'].setAttribute('transform', `translate(${jx * .3} 0)`);
      P['wright.brows'].setAttribute('transform', `translate(0 ${-8 * env})`);
    }
  });
  function hammerProp() { return `<g transform="translate(0 -10) rotate(20)"><path d="M0 0 L0 70" stroke="#8b5a2b" stroke-width="12" stroke-linecap="round"/><path d="M0 0 L0 70" stroke="${INK}" stroke-width="18" stroke-linecap="round" opacity="0"/><rect x="-30" y="-16" width="60" height="26" rx="6" fill="#555" ${OUT5}/></g>`; }

  // 7 ─ OCEANS · 70 · Helen Scales ────────────────────────────────────────────────
  S.push({
    id: 'scales', caption: 'OCEANS · UNKNOWN #70', credit: ['Helen Scales', 'marine biologist'],
    fig: { who: 'scales', x: 0, y: 0, s: .62, prop: binocProp(), inBoat: true },
    bubble: { x: 720, y: 100, w: 620, h: 160, lines: ['Where are blue whale', 'babies born?'] },
    sfx: [{ id: 'pff', t: 2.65, x: 1180, y: 330, text: 'PFFFFF!', color: '#8fd3ff', rot: -8, size: 84 }],
    svg() {
      return sky('sc', '#ffd98a', '#ffe9b8', '#ffc85c', 420) +
        `<circle cx="1330" cy="180" r="90" fill="#ff7b2e" ${OUT}/>` +
        `<path d="M30 440 C200 410 300 470 500 440 S900 410 1100 440 S1450 470 1570 440 V870 H30Z" fill="#1e8a8a" ${OUT}/>` +
        `<rect x="30" y="470" width="1540" height="400" fill="url(#sc-d2)"/>` +
        `<defs>${dots('sc-d2', '#1a7777', 16, 3.5)}</defs>` +
        `<g data-id="whale">` +
        `<path d="M-460 0 C-400 -100 -100 -140 250 -120 C450 -110 550 -80 630 -60 L720 -100 L700 -10 L730 60 L630 20 C500 70 200 100 -100 80 C-280 70 -400 60 -460 0Z" fill="#1d2f4b" ${OUT}/>` +
        `<circle cx="-230" cy="-40" r="12" fill="#fff" ${OUT5}/><path d="M-130 -50 Q-90 -80 -30 -60" fill="none" stroke="#8fd3ff" stroke-width="8"/><path d="M0 40 C40 0 120 0 160 40" fill="none" stroke="${INK}" stroke-width="12"/>` +
        `<g data-id="spout" data-pivot="-200 -120"><path d="M-200 -120 C-230 -200 -270 -220 -300 -260 M-200 -120 C-200 -220 -200 -240 -200 -280 M-200 -120 C-170 -200 -130 -220 -100 -260" fill="none" stroke="#8fd3ff" stroke-width="14" stroke-linecap="round"/><circle cx="-310" cy="-275" r="12" fill="#8fd3ff"/><circle cx="-200" cy="-300" r="14" fill="#8fd3ff"/><circle cx="-90" cy="-275" r="12" fill="#8fd3ff"/></g>` +
        `<g data-id="calf" data-pivot="150 150"><path d="M0 160 C20 110 150 100 240 130 C280 140 300 150 320 140 L340 110 L350 170 L320 190 C240 210 80 210 0 160Z" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="14 12"/><text x="160" y="178" text-anchor="middle" font-family="Bangers" font-size="60" fill="#ffe14d" stroke="${INK}" stroke-width="4" paint-order="stroke">?</text></g>` +
        `</g>` +
        `<g data-id="boat"><path d="M300 440 L620 440 L580 520 L340 520Z" fill="#d85a3a" ${OUT}/><rect x="400" y="380" width="110" height="60" fill="#1d2f4b" ${OUT}/><rect x="415" y="392" width="28" height="22" fill="#fff"/><path d="M470 250 L470 380" stroke="${INK}" stroke-width="10"/><path d="M470 250 L530 310 L470 300Z" fill="#ffe14d" ${OUT5}/>` +
        `<g data-id="figslot" transform="translate(550 440)"></g></g>` +
        `<path d="M700 300 q15 -14 30 0 q15 -14 30 0 M800 340 q12 -11 24 0 q12 -11 24 0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    },
    update(t, P) {
      const wx = 100 + t * 170, wy = 700 + wob(t, .25, 12);
      P.whale.setAttribute('transform', `translate(${wx} ${wy})`);
      U.setPop(P.spout, pop(prog(t, 2.5, 2.9)) * (1 - prog(t, 3.8, 4.4)));
      U.setPop(P.calf, pop(prog(t, 3.6, 4.0)));
      P.boat.setAttribute('transform', `translate(0 ${wob(t, .5, 8)}) rotate(${wob(t, .5, 2)} 460 480)`);
      sp(P['scales.armR'], 128 + wob(t, .7, 3)); sp(P['scales.head'], wob(t, .7, 4));
      sp(P['scales.armL'], -128 - wob(t, .7, 3));
    }
  });
  function binocProp() { return `<g transform="translate(-6 -16)"><rect x="-30" y="-16" width="26" height="30" rx="6" fill="#222" ${OUT5}/><rect x="4" y="-16" width="26" height="30" rx="6" fill="#222" ${OUT5}/><rect x="-6" y="-8" width="12" height="12" fill="#222"/></g>`; }

  // 8 ─ MEDICINE · 76 · Paul Knoepfler ────────────────────────────────────────────
  S.push({
    id: 'knoepfler', caption: 'MEDICINE · UNKNOWN #76', credit: ['Paul Knoepfler', 'cell biologist · University of California, Davis'],
    fig: { who: 'knoepfler', x: 440, y: 800, s: .95, prop: tabletProp() },
    bubble: { x: 70, y: 150, w: 780, h: 160, size: 32, lines: ['Can stem cells grow new organs', 'to replace old or diseased ones?'] },
    sfx: [{ id: 'th1', t: 2.2, x: 1250, y: 190, text: 'THUMP', color: '#ff6b8a', rot: -8, size: 90 }, { id: 'th2', t: 3.0, x: 1400, y: 440, text: 'THUMP', color: '#ff6b8a', rot: 6, size: 70 }],
    svg() {
      return sky('kn', '#c9f0e4', '#aee6d4', '#9bd9c6', 840) +
        `<rect x="30" y="760" width="1540" height="110" fill="#5b8c7a" ${OUT}/>` +
        `<rect x="760" y="580" width="700" height="190" rx="10" fill="#fff" ${OUT}/><rect x="780" y="300" width="660" height="22" fill="#8aa3b8" ${OUT}/>` +
        [820, 900, 980, 1060, 1300, 1380].map((x, i) => `<rect x="${x}" y="${240 + (i % 2) * 10}" width="40" height="${60 - (i % 2) * 10}" rx="6" fill="${['#8fd3c7', '#ffb3c6', '#ffe08a', '#b3c6ff'][i % 4]}" ${OUT5}/>`).join('') +
        // bioreactor
        `<rect x="1000" y="330" width="240" height="250" rx="30" fill="#cfe6ff" ${OUT}/><rect x="1020" y="400" width="200" height="160" rx="20" fill="#ffc2d1" ${OUT5}/>` +
        `<rect x="990" y="310" width="260" height="40" rx="10" fill="#8aa3b8" ${OUT}/>` +
        `<g data-id="heart" data-pivot="1120 480"><path d="M1120 530 C1060 490 1070 420 1120 445 C1170 420 1180 490 1120 530Z" fill="#ff4d6d" ${OUT}/><path d="M1112 452 c-10 10 -6 26 2 34 M1128 456 c8 12 4 26 -4 34" fill="none" stroke="#b3001b" stroke-width="3"/></g>` +
        [0, 1, 2, 3].map(i => `<circle data-id="bub${i}" cx="${1040 + i * 50}" cy="540" r="${4 + i}" fill="#fff" opacity=".9"/>`).join('') +
        `<path d="M1240 420 C1300 400 1350 480 1380 560" fill="none" stroke="#8fd3c7" stroke-width="10"/><rect x="1340" y="520" width="90" height="60" rx="8" fill="#b3c6ff" ${OUT}/>` +
        `<rect x="800" y="440" width="140" height="110" rx="8" fill="#1b2d5a" ${OUT}/><path data-id="ecg" d="M815 500 h30 l6 -20 l6 40 l6 -50 l6 30 h30 l6 -10 l6 10 h20" fill="none" stroke="#5bd1a5" stroke-width="4"/><rect x="855" y="550" width="30" height="30" fill="#1b2d5a" ${OUT5}/>`;
    },
    update(t, P) {
      const period = .8, ph = ((t - 1.4) % period + period) % period, beat = t > 1.4 ? Math.max(0, 1 - ph / .25) : 0;
      U.setPop(P.heart, 1 + .2 * beat);
      for (let i = 0; i < 4; i++) { const p = (t * .35 + i * .25) % 1; P['bub' + i].setAttribute('transform', `translate(0 ${-p * 120})`); P['bub' + i].setAttribute('opacity', 1 - p); }
      sp(P['knoepfler.armR'], -60 + wob(t, .5, 5)); sp(P['knoepfler.head'], 6 * beat + wob(t, .5, 2));
      P.ecg.setAttribute('transform', `translate(${-((t * 60) % 40)} 0)`);
    }
  });
  function tabletProp() { return `<g transform="translate(4 -26) rotate(-10)"><rect x="-30" y="-40" width="60" height="80" rx="6" fill="#222" ${OUT5}/><rect x="-24" y="-32" width="48" height="64" fill="#8fd3ff"/><path d="M-16 0 l8 -10 l8 14 l8 -18 l8 14" fill="none" stroke="#ff4d6d" stroke-width="3"/></g>`; }

  // 9 ─ ANCIENT HISTORY · 90 · Mark Lehner ────────────────────────────────────────
  S.push({
    id: 'lehner', caption: 'ANCIENT HISTORY · UNKNOWN #90', credit: ['Mark Lehner', 'archaeologist · Ancient Egypt Research Associates'],
    fig: { who: 'lehner', x: 380, y: 800, s: .95, prop: planProp() },
    bubble: { x: 60, y: 150, w: 720, h: 160, size: 32, lines: ['How did the ancient Egyptians', 'build the Great Pyramid?'] },
    sfx: [{ id: 'nope1', t: 2.3, x: 980, y: 300, text: 'NOPE', color: '#e63946', rot: -8, size: 90 }, { id: 'nope2', t: 3.5, x: 1240, y: 240, text: 'NOPE!', color: '#e63946', rot: 6, size: 90 }],
    svg() {
      let courses = ''; for (let y = 400; y < 760; y += 36) { const w = (y - 340) / 420 * 560; courses += `<path d="M${1150 - w / 2} ${y} H${1150 + w / 2}" stroke="${INK}" stroke-width="3" opacity=".5"/>`; }
      return sky('lh', '#ffe9a8', '#ffd166', '#ffdc7a', 500) +
        `<circle cx="1420" cy="160" r="80" fill="#ff7b2e" ${OUT}/>` +
        `<rect x="30" y="760" width="1540" height="110" fill="#e3a92c" ${OUT}/><path d="M30 760 Q400 720 800 760 T1570 760" fill="#f1c35c" stroke="none"/>` +
        `<path d="M1150 340 L1480 760 L820 760Z" fill="#d9a066" ${OUT}/><path d="M1150 340 L1480 760 L1150 760Z" fill="#b8793f" stroke="none"/><path d="M1150 340 L1480 760 L820 760Z" fill="none" ${OUT}/>` + courses +
        `<g data-id="rampA" data-pivot="820 760"><path d="M560 760 L1150 360" stroke="#fff" stroke-width="8" stroke-dasharray="18 12" fill="none"/></g>` +
        `<g data-id="xA" data-pivot="880 560"><path d="M840 520 L920 600 M920 520 L840 600" stroke="#e63946" stroke-width="12"/></g>` +
        `<g data-id="rampB" data-pivot="1150 760"><path d="M840 740 L1440 700 L870 650 L1400 600 L920 560 L1350 520 L980 480 L1300 440 L1040 400 L1250 380" stroke="#fff" stroke-width="7" stroke-dasharray="8 8" fill="none"/></g>` +
        `<g data-id="xB" data-pivot="1150 560"><path d="M1110 520 L1190 600 M1190 520 L1110 600" stroke="#e63946" stroke-width="12"/></g>` +
        `<g data-id="rampC" data-pivot="1150 650"><path d="M880 720 L1420 690 L900 660 L1380 630 L930 600" stroke="#9ad1ff" stroke-width="7" stroke-dasharray="14 8" fill="none"/></g>` +
        `<g data-id="qC" data-pivot="1150 660"><text x="1150" y="700" text-anchor="middle" font-family="Bangers" font-size="120" fill="#ffe14d" stroke="${INK}" stroke-width="7" paint-order="stroke">?</text></g>` +
        `<path d="M700 760 l20 -30 l20 30 M750 760 l15 -22 l15 22" fill="none" stroke="#2f8a4b" stroke-width="6"/>`;
    },
    update(t, P) {
      U.setPop(P.rampA, pop(prog(t, 1.6, 2.0))); U.setPop(P.xA, pop(prog(t, 2.25, 2.55)));
      U.setPop(P.rampB, pop(prog(t, 2.8, 3.2))); U.setPop(P.xB, pop(prog(t, 3.45, 3.75)));
      U.setPop(P.rampC, pop(prog(t, 4.0, 4.4))); U.setPop(P.qC, pop(prog(t, 4.5, 4.9)));
      sp(P['lehner.armR'], -40 - 30 * pop(prog(t, 1.4, 1.9)));
      sp(P['lehner.armL'], -150 * pop(prog(t, 4.4, 5.0)) + wob(t, .5, 3));
      sp(P['lehner.head'], -6 * pop(prog(t, 4.4, 5.0)) + wob(t, .5, 2));
    }
  });
  function planProp() { return `<g transform="translate(0 -20) rotate(-30)"><rect x="-50" y="-16" width="100" height="32" rx="14" fill="#f4f1ea" ${OUT5}/><path d="M-30 -16 V16 M30 -16 V16" stroke="${INK}" stroke-width="3"/></g>`; }

  // 10 ─ CLIMATE · 92 · Sarah Aarons ──────────────────────────────────────────────
  S.push({
    id: 'aarons', caption: 'CLIMATE · UNKNOWN #92', credit: ['Sarah Aarons', 'geochemist · Columbia University'],
    fig: { who: 'aarons', x: 520, y: 800, s: .95 },
    bubble: { x: 70, y: 140, w: 740, h: 200, size: 30, lines: ['How sensitive are the ice sheets', 'to global warming, and what will', 'it mean for sea levels?'] },
    sfx: [{ id: 'crk', t: 1.2, x: 760, y: 300, text: 'CRRRK', color: '#9ccfe8', rot: -10, size: 80 }],
    svg() {
      return sky('aa', '#bfe3ff', '#e9f6ff', '#a9d6f5', 480) +
        `<circle cx="1330" cy="160" r="70" fill="#ffe14d" ${OUT}/>` +
        `<path d="M1000 520 C1100 500 1300 540 1570 520 V870 H1000Z" fill="#2f6fed" ${OUT}/>` +
        [0, 1, 2].map(i => `<path data-id="sl${i}" d="M1010 ${600 + i * 50} C1100 ${580 + i * 50} 1300 ${620 + i * 50} 1570 ${600 + i * 50}" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="14 12" opacity="${1 - i * .3}"/>`).join('') +
        `<text data-id="slt" x="1300" y="580" font-family="Bangers" font-size="44" fill="#fff" stroke="${INK}" stroke-width="5" paint-order="stroke">+ ? m</text>` +
        `<path d="M1380 530 L1420 440 L1570 450 V560Z" fill="#8b5a2b" ${OUT}/><path d="M1470 440 L1470 400 L1500 372 L1530 400 L1530 440Z" fill="#ff7a45" ${OUT5}/>` +
        `<path d="M30 500 C200 480 400 520 700 490 C800 480 900 500 1000 540 L1010 870 H30Z" fill="#eaf6fb" ${OUT}/>` +
        `<path d="M1000 540 L1010 870 L1060 870 C1050 760 1060 650 1020 540Z" fill="#9ccfe8" ${OUT}/>` +
        `<path d="M30 600 C200 580 400 620 700 590 M30 720 C200 700 400 740 700 710" fill="none" stroke="#bcdcee" stroke-width="8"/>` +
        // tripod + core
        `<path d="M760 300 L660 700 M760 300 L860 700 M760 300 L780 720" stroke="${INK}" stroke-width="14" fill="none"/><path d="M760 300 L760 330" stroke="${INK}" stroke-width="14"/>` +
        `<g data-id="core" transform="translate(760 320)"><path d="M0 0 L0 -60" stroke="${INK}" stroke-width="4"/><rect x="-28" y="0" width="56" height="300" rx="28" fill="#fff" ${OUT}/>` +
        [40, 90, 130, 190, 240].map((y, i) => `<rect x="-24" y="${y}" width="48" height="${[14, 10, 18, 12, 16][i]}" fill="#9ccfe8"/>`).join('') + `</g>` +
        `<path d="M300 420 l40 -14 l40 14 M1100 300 q14 -12 28 0 q14 -12 28 0" fill="none" stroke="${INK}" stroke-width="5"/>`;
    },
    update(t, P) {
      const up = easeOut(prog(t, 1.0, 2.8)), cy = lerp(400, 215, up) + wob(t, .8, 3) * (1 - up);
      P.core.setAttribute('transform', `translate(760 ${cy})`);
      const rise = easeInOut(prog(t, 2.5, 5.5));
      for (let i = 0; i < 3; i++) P['sl' + i].setAttribute('transform', `translate(0 ${-rise * (40 + i * 20)})`);
      P.slt.setAttribute('transform', `translate(0 ${-rise * 60})`);
      const tug = wob(t, 1.5, 6) * (1 - up);
      sp(P['aarons.armR'], -125 + tug); sp(P['aarons.armL'], 15 + wob(t, .5, 3));
      sp(P['aarons.head'], 10 * up + wob(t, .5, 2));
    }
  });

  // 11 ─ THE FUTURE · 95 · Lindy Elkins-Tanton ────────────────────────────────────
  S.push({
    id: 'elkins', caption: 'THE FUTURE · UNKNOWN #95', credit: ['Lindy Elkins-Tanton', 'planetary scientist · UC Berkeley Space Sciences Laboratory'],
    fig: { who: 'elkins', x: 470, y: 800, s: .95, prop: dosiProp() },
    bubble: { x: 70, y: 150, w: 720, h: 160, size: 32, lines: ['Can humans survive space', 'radiation and settle off Earth?'] },
    sfx: [{ id: 'zzak', t: 2.0, x: 1230, y: 150, text: 'ZZAK!', color: '#ffe14d', rot: -8, size: 100 }, { id: 'krak', t: 2.8, x: 900, y: 200, text: 'KRAK', color: '#ff7b2e', rot: 6, size: 70 }],
    svg() {
      return sky('el', '#f7c58a', '#f1a15a', '#f3a35b', 540) +
        `<circle cx="1350" cy="150" r="40" fill="#fff6d5" ${OUT}/><circle cx="1180" cy="110" r="9" fill="#2a7fe0" ${OUT5}/>` +
        `<path d="M30 580 C300 540 500 620 800 580 S1300 540 1570 600 V870 H30Z" fill="#c8502d" ${OUT}/>` +
        `<g fill="#a8432a" ${OUT5}><path d="M900 740 l60 -40 l80 20 l20 50 l-150 10z"/><path d="M1250 720 l50 -50 l90 10 l30 60 l-160 20z"/></g>` +
        `<path d="M1000 580 a90 60 0 0 1 180 0z" fill="#e8e8e8" ${OUT5}/><rect x="1075" y="540" width="30" height="40" fill="#e8e8e8" ${OUT5}/><path d="M1040 540 l0 -40 M1140 540 l0 -60" stroke="${INK}" stroke-width="5"/>` +
        [[1100, 60], [1300, 260], [860, 100]].map(([x, y], i) => `<g data-id="ray${i}" data-pivot="${x} ${y}"><path d="M${x} ${y} l-30 120 l40 -20 l-60 150 l90 -110 l-40 10 l50 -130z" fill="#ffe14d" ${OUT5}/></g>`).join('');
    },
    update(t, P) {
      const r = [prog(t, 1.2, 1.5), prog(t, 2.0, 2.3), prog(t, 2.8, 3.1)];
      r.forEach((p, i) => U.setPop(P['ray' + i], pop(p) * (1 - prog(t, 1.9 + i * .8, 2.3 + i * .8))));
      sp(P['elkins.armR'], 38 + wob(t, .6, 2)); sp(P['elkins.armL'], -38 + wob(t, .6, -2));
      const kick = Math.max(0, 1 - ((t - 2.0 + 10) % .8) / .3);
      const needle = -70 + 110 * clamp(t / 4, 0, 1) + wob(t, 7, 6);
      P.needle.setAttribute('transform', `rotate(${needle} 0 20)`);
      sp(P['elkins.head'], wob(t, .5, 3) - 6 * prog(t, 3, 3.5));
    }
  });
  function dosiProp() { return `<g transform="translate(0 -30)"><rect x="-44" y="-30" width="88" height="62" rx="8" fill="#ffe14d" ${OUT5}/><path d="M-30 20 A30 30 0 0 1 30 20Z" fill="#fff" ${OUT5} stroke-width="3"/><path d="M10 -8 A30 30 0 0 1 30 20 L0 20Z" fill="#ff3b3b" stroke="none"/><g data-id="needle"><path d="M0 20 L0 -6" stroke="${INK}" stroke-width="4"/></g><circle cx="0" cy="20" r="4" fill="${INK}"/></g>`; }

  return S;
})();
