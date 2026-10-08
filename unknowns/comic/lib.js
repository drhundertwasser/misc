// Shared helpers for the comic: easing, SVG string builders, comic furniture (captions, bubbles, SFX).
window.U = (() => {
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const prog = (t, t0, t1) => clamp((t - t0) / (t1 - t0), 0, 1);
  const easeOut = p => 1 - Math.pow(1 - p, 3);
  const easeIn = p => p * p * p;
  const easeInOut = p => (p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
  const pop = p => { if (p <= 0) return 0; if (p >= 1) return 1; const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');

  // Ben-Day dot pattern definitions. Call once per scene with the colors you need.
  const dots = (id, color, size = 12, r = 2.8) =>
    `<pattern id="${id}" width="${size}" height="${size}" patternUnits="userSpaceOnUse"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" fill="${color}"/></pattern>`;

  const INK = '#111';
  const OUT = `stroke="${INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"`;
  const OUT5 = `stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;

  // Yellow caption box (Bangers). Width is estimated from the text length.
  function caption(id, x, y, text, { size = 32, fill = '#ffe14d', color = INK } = {}) {
    const w = Math.round(text.length * size * 0.47 + 40), h = Math.round(size * 1.65);
    return `<g data-id="${id}" transform="translate(${x} ${y})"><g data-part="box"><rect x="0" y="0" width="${w}" height="${h}" fill="${fill}" ${OUT}/>` +
      `<text x="20" y="${Math.round(h * 0.72)}" font-family="Bangers" font-size="${size}" fill="${color}" letter-spacing="1">${esc(text)}</text></g></g>`;
  }

  // White speech bubble with a tail toward (tx,ty). Lines are centered. The group pivot is the tail tip
  // so the bubble can pop out from the speaker's mouth.
  function bubble(id, x, y, w, h, tx, ty, lines, { size = 34, font = 'Comic Neue', weight = 700 } = {}) {
    const cx = x + w / 2;
    // tail base: two points on the bubble edge closest to the tail tip
    let tail;
    if (tx < x || tx > x + w) { const bxs = tx < x ? x : x + w, bys = clamp(ty, y + 40, y + h - 40); tail = `M${bxs} ${bys - 22} L${tx} ${ty} L${bxs} ${bys + 22}`; }
    else { const bx = clamp(tx, x + 40, x + w - 40), by = ty > y + h ? y + h : y; tail = `M${bx - 22} ${by} L${tx} ${ty} L${bx + 22} ${by}`; }
    const lh = size * 1.22, ty0 = y + h / 2 - ((lines.length - 1) * lh) / 2 + size * 0.36;
    const txt = lines.map((l, i) => `<tspan x="${cx}" y="${Math.round(ty0 + i * lh)}">${esc(l)}</tspan>`).join('');
    return `<g data-id="${id}" data-pivot="${tx} ${ty}" transform="translate(${tx} ${ty}) scale(0) translate(${-tx} ${-ty})">` +
      `<path d="${tail}" fill="#fff" ${OUT}/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="26" fill="#fff" ${OUT}/>` +
      `<path d="${tail}" fill="#fff" stroke="none"/><rect x="${x + 4}" y="${y + 4}" width="${w - 8}" height="${h - 8}" rx="22" fill="#fff" stroke="none"/>` +
      `<text font-family="${font}" font-weight="${weight}" font-size="${size}" fill="${INK}" text-anchor="middle">${txt}</text></g>`;
  }

  // Sound-effect lettering. Pivot at (x,y) so it can pop.
  function sfx(id, x, y, text, { color = '#ffe14d', rot = -8, size = 90, stroke = 7 } = {}) {
    return `<g data-id="${id}" data-pivot="${x} ${y}" transform="translate(${x} ${y}) scale(0) translate(${-x} ${-y})">` +
      `<text x="${x}" y="${y}" font-family="Bangers" font-size="${size}" fill="${color}" stroke="${INK}" stroke-width="${stroke}" paint-order="stroke" stroke-linejoin="round" transform="rotate(${rot} ${x} ${y})" text-anchor="middle">${esc(text)}</text></g>`;
  }

  // Scale a group about its data-pivot (used by bubble/sfx pops).
  function setPop(el, s) {
    const [px, py] = el.getAttribute('data-pivot').split(' ').map(Number);
    el.setAttribute('transform', `translate(${px} ${py}) scale(${s}) translate(${-px} ${-py})`);
  }

  // Panel frame + credit strip, shared by every scene.
  function frame() {
    return `<rect x="30" y="30" width="1540" height="840" fill="none" stroke="${INK}" stroke-width="10"/>`;
  }
  function credit(id, name, role) {
    return `<g data-id="${id}" transform="translate(0 120)"><rect x="30" y="796" width="1540" height="74" fill="${INK}"/>` +
      `<text x="60" y="846" font-family="Bangers" font-size="34" fill="#ffe14d" letter-spacing="1">${esc(name.toUpperCase())}</text>` +
      `<text x="${60 + name.length * 19 + 30}" y="844" font-family="Comic Neue" font-weight="700" font-size="24" fill="#fff">${esc(role.toUpperCase())}</text></g>`;
  }

  // Query helpers: collect every data-id / data-part element under a root into a map.
  function collect(root) {
    const m = {};
    root.querySelectorAll('[data-id]').forEach(e => { m[e.getAttribute('data-id')] = e; });
    root.querySelectorAll('.fig').forEach(f => {
      const n = f.getAttribute('data-name');
      m[n] = f;
      f.querySelectorAll('[data-part]').forEach(p => { m[n + '.' + p.getAttribute('data-part')] = p; });
    });
    return m;
  }

  return { clamp, lerp, prog, easeOut, easeIn, easeInOut, pop, esc, dots, INK, OUT, OUT5, caption, bubble, sfx, setPop, frame, credit, collect };
})();
