// Comic-style scientist builder. figure(opts) returns an SVG string: a <g class="fig"> with
// animatable sub-parts tagged data-part (head, armL, armR, legL, legR, body, prop).
// Local coordinates: feet on y=0, figure faces the viewer, about 360px tall at scale 1.
window.figure = function figure(o) {
  const U = window.U, INK = U.INK, OUT = U.OUT;
  const {
    name = 'fig', x = 0, y = 0, scale = 1, facing = 1,
    skin = '#c68642', hair = 'short', hairColor = '#222', outfit = 'tshirt', outfitColor = '#2a7fe0',
    pants = '#1f2a44', shoes = '#333', glasses = false, beard = false, wheelchair = false,
    hat = null, hatColor = '#ffe14d', headphones = false, age = 'adult', mouth = 'smile', eyes = 'open', prop = ''
  } = o;

  const shoulderY = -236, neckY = -252, headY = -300, R = 44;
  const legs = wheelchair ? wheelchairLegs() : standingLegs();

  function standingLegs() {
    return `<g data-part="legL"><path d="M-28 -120 L-30 -12" stroke="${pants}" stroke-width="34" stroke-linecap="round"/><path d="M-28 -120 L-30 -12" ${OUT} fill="none" stroke-width="46" style="mix-blend-mode:normal" opacity="0"/>` +
      `<ellipse cx="-34" cy="-6" rx="38" ry="15" fill="${shoes}" ${OUT}/></g>` +
      `<g data-part="legR"><path d="M28 -120 L30 -12" stroke="${pants}" stroke-width="34" stroke-linecap="round"/><ellipse cx="34" cy="-6" rx="38" ry="15" fill="${shoes}" ${OUT}/></g>` +
      `<path d="M-28 -120 L-30 -12 M28 -120 L30 -12" stroke="${INK}" stroke-width="46" stroke-linecap="round" fill="none" opacity="0"/>`;
  }
  function wheelchairLegs() {
    return `<g data-part="chair">` +
      `<circle cx="-30" cy="-70" r="72" fill="#dfe6f3" ${OUT}/><circle cx="-30" cy="-70" r="26" fill="#fff" ${OUT}/>` +
      `<path d="M-30 -142 L-30 2 M-102 -70 L42 -70 M-81 -121 L21 -19 M-81 -19 L21 -121" stroke="${INK}" stroke-width="6" fill="none"/>` +
      `<circle cx="136" cy="-20" r="24" fill="#dfe6f3" ${OUT}/>` +
      `<path d="M-60 -140 L-60 -220 M-60 -140 L60 -140 L100 -70 L136 -44" stroke="${INK}" stroke-width="10" fill="none" stroke-linecap="round"/></g>` +
      `<g data-part="legR"><path d="M10 -130 L88 -126 L88 -30" stroke="${pants}" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="96" cy="-20" rx="30" ry="13" fill="${shoes}" ${OUT}/></g>` +
      `<g data-part="legL"><path d="M-10 -130 L66 -130 L66 -24" stroke="${pants}" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="74" cy="-12" rx="32" ry="14" fill="${shoes}" ${OUT}/></g>`;
  }

  // torso by outfit
  const torsoPath = `M-66 ${shoulderY - 14} C-44 ${shoulderY - 40} 44 ${shoulderY - 40} 66 ${shoulderY - 14} L74 -110 L-74 -110 Z`;
  let body = '';
  if (outfit === 'labcoat') {
    body = `<path d="${torsoPath}" fill="#f4f4f4" ${OUT}/><path d="M0 ${shoulderY - 20} L0 -110" stroke="${INK}" stroke-width="4"/>` +
      `<path d="M-18 ${shoulderY - 30} L-40 ${shoulderY + 20} L-6 ${shoulderY + 10}Z M18 ${shoulderY - 30} L40 ${shoulderY + 20} L6 ${shoulderY + 10}Z" fill="${outfitColor}" ${U.OUT5}/>` +
      `<rect x="28" y="-190" width="30" height="30" fill="none" stroke="${INK}" stroke-width="4"/>`;
  } else if (outfit === 'parka') {
    body = `<path d="${torsoPath}" fill="${outfitColor}" ${OUT}/><path d="M-50 ${shoulderY - 10} C-40 ${shoulderY - 50} 40 ${shoulderY - 50} 50 ${shoulderY - 10}" fill="none" stroke="#fff" stroke-width="22"/><path d="M-50 ${shoulderY - 10} C-40 ${shoulderY - 50} 40 ${shoulderY - 50} 50 ${shoulderY - 10}" fill="none" stroke="${INK}" stroke-width="5"/>` +
      `<path d="M0 ${shoulderY - 10} L0 -110" stroke="${INK}" stroke-width="4" stroke-dasharray="8 8"/>`;
  } else if (outfit === 'vest') {
    body = `<path d="${torsoPath}" fill="${outfitColor}" ${OUT}/><path d="M-66 ${shoulderY - 14} L-60 -110 L-22 -110 L-18 ${shoulderY - 26}Z M66 ${shoulderY - 14} L60 -110 L22 -110 L18 ${shoulderY - 26}Z" fill="#c9a86a" ${U.OUT5}/>` +
      `<rect x="-56" y="-180" width="26" height="22" fill="none" stroke="${INK}" stroke-width="4"/><rect x="30" y="-180" width="26" height="22" fill="none" stroke="${INK}" stroke-width="4"/>`;
  } else if (outfit === 'sweater') {
    body = `<path d="${torsoPath}" fill="${outfitColor}" ${OUT}/><path d="M-30 ${shoulderY - 28} C-15 ${shoulderY - 12} 15 ${shoulderY - 12} 30 ${shoulderY - 28}" fill="none" stroke="${INK}" stroke-width="5"/>` +
      `<path d="M-60 -150 L60 -150 M-62 -135 L62 -135" stroke="${INK}" stroke-width="3" opacity=".5"/>`;
  } else if (outfit === 'spacesuit') {
    body = `<path d="${torsoPath}" fill="#f4f4f4" ${OUT}/><rect x="-30" y="-205" width="60" height="44" rx="6" fill="${outfitColor}" ${U.OUT5}/><circle cx="-14" cy="-190" r="6" fill="#ff3b3b"/><circle cx="14" cy="-190" r="6" fill="#ffe14d"/>`;
  } else {
    body = `<path d="${torsoPath}" fill="${outfitColor}" ${OUT}/>`;
  }

  const sleeve = outfit === 'labcoat' || outfit === 'spacesuit' ? '#f4f4f4' : outfitColor;
  const armSvg = (side, part) => {
    const sx = side * 62, sy = shoulderY;
    const d = `M${sx} ${sy} C${sx + side * 30} ${sy + 40} ${sx + side * 36} ${sy + 80} ${sx + side * 26} ${sy + 112}`;
    return `<g data-part="${part}" data-pivot="${sx} ${sy}"><path d="${d}" fill="none" stroke="${INK}" stroke-width="42" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${sleeve}" stroke-width="30" stroke-linecap="round"/>` +
      `<g data-part="${part}Hand" transform="translate(${sx + side * 26} ${sy + 112})"><circle r="19" fill="${skin}" ${OUT}/>${part === 'armR' && prop ? prop : ''}</g></g>`;
  };

  // head
  let hairBack = '', hairFront = '';
  const hc = hairColor;
  switch (hair) {
    case 'short': hairFront = `<path d="M${-R + 2} ${headY - 6} C${-R} ${headY - 52} ${R} ${headY - 52} ${R - 2} ${headY - 6} C${R * .6} ${headY - 30} ${-R * .6} ${headY - 30} ${-R + 2} ${headY - 6}Z" fill="${hc}" ${OUT}/>`; break;
    case 'bun': hairBack = `<circle cx="${-R * .7}" cy="${headY - 30}" r="20" fill="${hc}" ${OUT}/>`; hairFront = `<path d="M${-R + 2} ${headY - 4} C${-R} ${headY - 50} ${R} ${headY - 50} ${R - 2} ${headY - 4} C${R * .5} ${headY - 24} ${-R * .5} ${headY - 24} ${-R + 2} ${headY - 4}Z" fill="${hc}" ${OUT}/>`; break;
    case 'curly': hairBack = [[-38, -36], [-14, -48], [14, -48], [38, -36], [-48, -12], [48, -12]].map(([dx, dy]) => `<circle cx="${dx}" cy="${headY + dy}" r="18" fill="${hc}" ${OUT}/>`).join(''); break;
    case 'afro': hairBack = `<circle cx="0" cy="${headY - 10}" r="${R + 22}" fill="${hc}" ${OUT}/>`; break;
    case 'locs': hairBack = [-40, -24, -8, 8, 24, 40].map(dx => `<path d="M${dx} ${headY - 30} L${dx * 1.3} ${headY + 60}" stroke="${INK}" stroke-width="16" stroke-linecap="round"/><path d="M${dx} ${headY - 30} L${dx * 1.3} ${headY + 60}" stroke="${hc}" stroke-width="9" stroke-linecap="round"/>`).join('');
      hairFront = `<path d="M${-R + 2} ${headY - 6} C${-R} ${headY - 52} ${R} ${headY - 52} ${R - 2} ${headY - 6} C${R * .6} ${headY - 30} ${-R * .6} ${headY - 30} ${-R + 2} ${headY - 6}Z" fill="${hc}" ${OUT}/>`; break;
    case 'ponytail': hairBack = `<path d="M${R - 6} ${headY - 20} C${R + 40} ${headY - 10} ${R + 30} ${headY + 60} ${R - 10} ${headY + 80}" fill="none" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="M${R - 6} ${headY - 20} C${R + 40} ${headY - 10} ${R + 30} ${headY + 60} ${R - 10} ${headY + 80}" fill="none" stroke="${hc}" stroke-width="18" stroke-linecap="round"/>`;
      hairFront = `<path d="M${-R + 2} ${headY - 4} C${-R} ${headY - 50} ${R} ${headY - 50} ${R - 2} ${headY - 4} C${R * .5} ${headY - 24} ${-R * .5} ${headY - 24} ${-R + 2} ${headY - 4}Z" fill="${hc}" ${OUT}/>`; break;
    case 'bob': hairBack = `<path d="M${-R - 6} ${headY + 30} L${-R - 6} ${headY - 10} C${-R} ${headY - 56} ${R} ${headY - 56} ${R + 6} ${headY - 10} L${R + 6} ${headY + 30}Z" fill="${hc}" ${OUT}/>`;
      hairFront = `<path d="M${-R - 2} ${headY - 2} C${-R} ${headY - 52} ${R} ${headY - 52} ${R + 2} ${headY - 2} C${R * .5} ${headY - 26} ${-R * .4} ${headY - 20} ${-R - 2} ${headY - 2}Z" fill="${hc}" ${OUT}/>`; break;
    case 'long': hairBack = `<path d="M${-R - 8} ${headY + 70} L${-R - 8} ${headY - 10} C${-R} ${headY - 56} ${R} ${headY - 56} ${R + 8} ${headY - 10} L${R + 8} ${headY + 70}Z" fill="${hc}" ${OUT}/>`;
      hairFront = `<path d="M${-R - 2} ${headY - 2} C${-R} ${headY - 52} ${R} ${headY - 52} ${R + 2} ${headY - 2} C${R * .5} ${headY - 26} ${-R * .4} ${headY - 20} ${-R - 2} ${headY - 2}Z" fill="${hc}" ${OUT}/>`; break;
    case 'hijab': hairBack = `<path d="M${-R - 14} ${headY + 20} C${-R - 20} ${headY - 50} ${R + 20} ${headY - 50} ${R + 14} ${headY + 20} L${R + 30} ${shoulderY + 10} L${-R - 30} ${shoulderY + 10}Z" fill="${hc}" ${OUT}/>`;
      hairFront = `<path d="M${-R - 2} ${headY + 10} C${-R - 6} ${headY - 46} ${R + 6} ${headY - 46} ${R + 2} ${headY + 10}" fill="none" stroke="${hc}" stroke-width="18"/><path d="M${-R - 2} ${headY + 10} C${-R - 6} ${headY - 46} ${R + 6} ${headY - 46} ${R + 2} ${headY + 10}" fill="none" stroke="${INK}" stroke-width="4"/>`; break;
    case 'bald': default: hairFront = ''; break;
  }
  if (age === 'senior' && hair !== 'bald' && hair !== 'hijab') { hairBack = hairBack.replace(new RegExp(hc, 'g'), '#d8d8d0'); hairFront = hairFront.replace(new RegExp(hc, 'g'), '#d8d8d0'); }

  let hatSvg = '';
  if (hat === 'hardhat') hatSvg = `<path d="M${-R - 4} ${headY - 14} C${-R} ${headY - 70} ${R} ${headY - 70} ${R + 4} ${headY - 14} L${R + 16} ${headY - 10} L${-R - 16} ${headY - 10}Z" fill="${hatColor}" ${OUT}/>`;
  if (hat === 'fieldhat') hatSvg = `<path d="M${-R + 4} ${headY - 28} C${-R} ${headY - 80} ${R} ${headY - 80} ${R - 4} ${headY - 28}Z" fill="${hatColor}" ${OUT}/><path d="M${-R - 34} ${headY - 24} C${-R} ${headY - 40} ${R} ${headY - 40} ${R + 34} ${headY - 24} C${R} ${headY - 12} ${-R} ${headY - 12} ${-R - 34} ${headY - 24}Z" fill="${hatColor}" ${OUT}/>`;
  if (hat === 'beanie') hatSvg = `<path d="M${-R - 2} ${headY - 2} C${-R} ${headY - 64} ${R} ${headY - 64} ${R + 2} ${headY - 2}Z" fill="${hatColor}" ${OUT}/><rect x="${-R - 4}" y="${headY - 14}" width="${2 * R + 8}" height="18" rx="6" fill="${hatColor}" ${OUT}/>`;
  if (hat === 'helmet') hatSvg = `<circle cx="0" cy="${headY}" r="${R + 30}" fill="none" ${OUT}/><circle cx="0" cy="${headY}" r="${R + 30}" fill="#fff" opacity=".18"/><path d="M${-R - 10} ${headY - 30} C${-R} ${headY - 60} ${R - 10} ${headY - 60} ${R + 10} ${headY - 40}" fill="none" stroke="#fff" stroke-width="6" opacity=".8"/>`;

  const eyeSvg = eyes === 'closed'
    ? `<path d="M-26 ${headY - 2} q10 8 20 0 M6 ${headY - 2} q10 8 20 0" fill="none" stroke="${INK}" stroke-width="4"/>`
    : `<ellipse cx="-16" cy="${headY - 4}" rx="10" ry="13" fill="#fff" ${U.OUT5} stroke-width="4"/><ellipse cx="16" cy="${headY - 4}" rx="10" ry="13" fill="#fff" ${U.OUT5} stroke-width="4"/>` +
    `<g data-part="pupils"><circle cx="-14" cy="${headY - 2}" r="5" fill="${INK}"/><circle cx="18" cy="${headY - 2}" r="5" fill="${INK}"/></g>`;
  const browSvg = `<g data-part="brows"><path d="M-28 ${headY - 24} q12 -8 24 0 M4 ${headY - 24} q12 -8 24 0" fill="none" stroke="${INK}" stroke-width="4"/></g>`;
  const mouthSvg = mouth === 'open' ? `<ellipse cx="0" cy="${headY + 24}" rx="12" ry="9" fill="${INK}"/>` :
    mouth === 'hmm' ? `<path d="M-14 ${headY + 24} q14 -6 28 2" fill="none" stroke="${INK}" stroke-width="4"/>` :
      `<path d="M-16 ${headY + 20} q16 14 32 0" fill="none" stroke="${INK}" stroke-width="4"/>`;
  const glassSvg = glasses ? `<circle cx="-16" cy="${headY - 4}" r="17" fill="none" stroke="${INK}" stroke-width="4"/><circle cx="16" cy="${headY - 4}" r="17" fill="none" stroke="${INK}" stroke-width="4"/><path d="M-1 ${headY - 6} L1 ${headY - 6} M-33 ${headY - 8} L-46 ${headY - 12} M33 ${headY - 8} L46 ${headY - 12}" stroke="${INK}" stroke-width="4"/>` : '';
  const beardSvg = beard ? `<path d="M-40 ${headY + 4} C-44 ${headY + 50} 44 ${headY + 50} 40 ${headY + 4} C30 ${headY + 36} -30 ${headY + 36} -40 ${headY + 4}Z" fill="${age === 'senior' ? '#d8d8d0' : hairColor}" ${OUT}/><path d="M-16 ${headY + 20} q16 14 32 0" fill="none" stroke="#fff" stroke-width="3"/>` : '';
  const hpSvg = headphones ? `<path d="M${-R - 8} ${headY} C${-R - 10} ${headY - 70} ${R + 10} ${headY - 70} ${R + 8} ${headY}" fill="none" stroke="${INK}" stroke-width="10"/><rect x="${-R - 20}" y="${headY - 16}" width="22" height="36" rx="8" fill="#ff3b3b" ${OUT}/><rect x="${R - 2}" y="${headY - 16}" width="22" height="36" rx="8" fill="#ff3b3b" ${OUT}/>` : '';

  const head = `<g data-part="head" data-pivot="0 ${neckY}">` +
    `<rect x="-16" y="${neckY - 12}" width="32" height="26" fill="${skin}" ${OUT}/>` +
    hairBack +
    `<circle cx="0" cy="${headY}" r="${R}" fill="${skin}" ${OUT}/>` +
    `<path d="M${-R + 6} ${headY + 8} q4 10 10 10 M${R - 6} ${headY + 8} q-4 10 -10 10" fill="none" stroke="${INK}" stroke-width="3" opacity=".5"/>` +
    eyeSvg + browSvg + mouthSvg + glassSvg + beardSvg + hairFront + hatSvg + hpSvg + `</g>`;

  return `<g class="fig" data-name="${name}" transform="translate(${x} ${y}) scale(${scale * facing} ${scale})">` +
    (wheelchair ? legs : legs) + armSvg(-1, 'armL') + `<g data-part="body">${body}</g>` + head + armSvg(1, 'armR') + `</g>`;
};

// Rotate an arm/head part around its pivot (degrees).
window.setPart = function (el, deg, dx = 0, dy = 0) {
  if (!el) return;
  const [px, py] = el.getAttribute('data-pivot').split(' ').map(Number);
  el.setAttribute('transform', `translate(${dx} ${dy}) rotate(${deg} ${px} ${py})`);
};
